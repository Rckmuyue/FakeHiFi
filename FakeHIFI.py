import numpy as np

# Fix numpy warnings
if not hasattr(np, 'float'):
    np.float = float
if not hasattr(np, 'complex'):
    np.complex = complex

import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import os
import argparse
import sys

def generate_fake_high_freq(
    y, sr,
    cutoff_freq=22000,
    target_max_freq=47500,
    transition_width=1500,
    gain=1.5,
    n_fft=8192,
    hop_length=2048
):
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    mag, phase = np.abs(S), np.angle(S)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    cutoff_bin = np.argmax(freqs >= cutoff_freq)
    max_bin = np.argmax(freqs >= target_max_freq)
    if max_bin <= cutoff_bin:
        # Invalid frequency band, return original audio directly
        return y

    high_len = max_bin - cutoff_bin
    if high_len <= 0:
        # Invalid frequency band, return original audio directly
        return y

    decay_envelope = 0.5 * (1 + np.cos(np.linspace(0, np.pi, high_len)))

    start_ref_bin = max(0, cutoff_bin - 5)
    max_mag = np.mean(mag[start_ref_bin:cutoff_bin, :], axis=0) * gain

    fake_high_mag = decay_envelope[:, None] * max_mag[None, :]

    freq_res = freqs[1] - freqs[0]
    trans_bins = int(transition_width / freq_res)
    trans_bins = min(trans_bins, high_len)

    original_segment = mag[cutoff_bin:cutoff_bin + trans_bins, :]
    fake_segment = fake_high_mag[:trans_bins, :]

    weights = 0.5 * (1 - np.cos(np.linspace(0, np.pi, trans_bins)))[:, None]
    blended_segment = original_segment * (1 - weights) + fake_segment * weights

    mag[cutoff_bin:cutoff_bin + trans_bins, :] = blended_segment
    mag[cutoff_bin + trans_bins:max_bin, :] = fake_high_mag[trans_bins:, :]

    S_new = mag * np.exp(1j * phase)
    y_out = librosa.istft(S_new, hop_length=hop_length)

    return y_out

def plot_spectrogram(y, sr, title, filename, n_fft=2048, hop_length=512):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length)), ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format="%+2.0f dB")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def process_audio(
    file_path,
    cutoff_freq,
    target_max_freq,
    transition_width,
    gain,
    output_dir,
    out_sr=None,
    bitdepth='PCM_16',
    n_fft=8192,
    hop_length=2048
):
    y, sr = librosa.load(file_path, sr=None, mono=False)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Ensure sample rate is at least 96000Hz to support high-frequency generation
    desired_sr = max(out_sr or sr, 96000)
    if sr < desired_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=desired_sr)
        sr = desired_sr
    if out_sr is None:
        out_sr = sr

    if y.ndim == 1:
        y_out = generate_fake_high_freq(y, sr, cutoff_freq, target_max_freq, transition_width, gain, n_fft, hop_length)
        if out_sr != sr:
            y_out = librosa.resample(y_out, orig_sr=sr, target_sr=out_sr)
        sf.write(os.path.join(output_dir, base_name + '_fake.wav'), y_out, out_sr, subtype=bitdepth)
        plot_spectrogram(y, sr, "Original Mono", os.path.join(output_dir, base_name + '_original.png'))
        plot_spectrogram(y_out, out_sr, "Modified Mono", os.path.join(output_dir, base_name + '_modified.png'))
    else:
        y_out = []
        for ch in y:
            ch_out = generate_fake_high_freq(ch, sr, cutoff_freq, target_max_freq, transition_width, gain, n_fft, hop_length)
            if out_sr != sr:
                ch_out = librosa.resample(ch_out, orig_sr=sr, target_sr=out_sr)
            y_out.append(ch_out)
        y_out = np.array(y_out)
        sf.write(os.path.join(output_dir, base_name + '_fake.wav'), y_out.T, out_sr, subtype=bitdepth)
        plot_spectrogram(y[0], sr, "Original Ch0", os.path.join(output_dir, base_name + '_original_ch0.png'))
        plot_spectrogram(y_out[0], out_sr, "Modified Ch0", os.path.join(output_dir, base_name + '_modified_ch0.png'))

def get_args():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="FakeHIFI V1.0 by.Muyue")
        parser.add_argument("file", help="Input audio file path (WAV)")
        parser.add_argument("--cutoff", type=int, default=22000, help="Start frequency for generation (Hz)")
        parser.add_argument("--maxfreq", type=int, default=47500, help="Maximum frequency for generation (Hz)")
        parser.add_argument("--transition", type=int, default=1500, help="Transition band width (Hz)")
        parser.add_argument("--gain", type=float, default=1.5, help="Amplitude gain for generated frequencies")
        parser.add_argument("--out", default="output", help="Output directory")
        parser.add_argument("--out_sr", type=int, default=None, help="Output sample rate (Hz), defaults to input sample rate")
        parser.add_argument("--bitdepth", default="PCM_32", help="Output bit depth: PCM_16 / PCM_24 / PCM_32 / FLOAT")
        parser.add_argument("--n_fft", type=int, default=8192, help="STFT window length, higher value means higher frequency resolution")
        parser.add_argument("--hop_length", type=int, default=2048, help="STFT hop length")
        return parser.parse_args()
    else:
        print("FakeHIFI V1.0 by.Muyue")
        print("==============================================")
        print("Interactive Mode: Please enter the following parameters")
        file = input("Input file path: ").strip()
        cutoff = int(input("Start frequency for generation (default 22000): ") or 22000)
        maxfreq = int(input("Maximum frequency for generation (default 47500): ") or 47500)
        transition = int(input("Transition band width Hz (default 1500): ") or 1500)
        gain = float(input("Amplitude gain (default 1.5): ") or 1.5)
        output = input("Output directory (default output): ") or "output"
        out_sr = input("Output sample rate Hz (default original or >=96000): ")
        out_sr = int(out_sr) if out_sr else None
        bitdepth = input("Output bit depth (PCM_16/24/32/FLOAT, default PCM_32): ") or "PCM_32"
        n_fft = int(input("STFT window length n_fft (default 8192): ") or 8192)
        hop_length = int(input("STFT hop length hop_length (default 2048): ") or 2048)

        class Args:
            pass
        args = Args()
        args.file = file
        args.cutoff = cutoff
        args.maxfreq = maxfreq
        args.transition = transition
        args.gain = gain
        args.out = output
        args.out_sr = out_sr
        args.bitdepth = bitdepth
        args.n_fft = n_fft
        args.hop_length = hop_length
        return args

def main():
    args = get_args()
    os.makedirs(args.out, exist_ok=True)
    process_audio(args.file, args.cutoff, args.maxfreq, args.transition, args.gain, args.out, args.out_sr, args.bitdepth, args.n_fft, args.hop_length)

if __name__ == "__main__":
    main()