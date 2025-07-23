# About FakeHiFi

Language: [English](https://github.com/Rckmuyue/FakeHiFi/main/README.md "English") / [中文](https://github.com/Rckmuyue/FakeHiFi/main/README_zh-cn.md "中文")

~~This program is used to restore the high frequencies cut off in MP3 music files.~~

In fact, this program is **a satire of the so-called “AI restoration” by certain music platforms (like KuGou Music)**.

> Note: This program does **not** have any real high-frequency restoration capabilities!
>
> Its “restoration” is merely artificially faked high-frequency content, just to make it **look** like it was repaired.

---

## Demo Comparison

Music used: **Zhou Shen – The Light**

Original source: **48KHz / 24bit**

| "AI Repair" by Certain Platform (e.g., KuGou)                                                                                                                                     | Fake High-Frequency Effect by This Program                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![KuGou Repair](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_2.png?raw=true)](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_2.png?raw=true) | [![FakeHiFi Fake](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_1.png?raw=true)](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_1.png?raw=true) |

---

## How to Use

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Method 1: Interactive Mode

Run the main program directly and follow the prompts:

```bash
python FakeHiFi.py
```

---

### Method 2: Command Line Mode

You can run it with arguments:

```bash
python FakeHiFi.py input.wav --cutoff 22000 --maxfreq 47500 --transition 1500 --gain 1.5 --out output --out_sr 96000 --bitdepth PCM_32 --n_fft 8192 --hop_length 2048
```

#### Parameter Descriptions:

| Parameter      | Description                                        |
| -------------- | -------------------------------------------------- |
| `file`         | Input audio file path (WAV format)                 |
| `--cutoff`     | Starting frequency for faking (Hz), default: 22000 |
| `--maxfreq`    | Maximum frequency to fake (Hz), default: 47500     |
| `--transition` | Transition band width (Hz), default: 1500          |
| `--gain`       | Gain multiplier for the faked band, default: 1.5   |
| `--out`        | Output directory, default: `output`                |
| `--out_sr`     | Output sample rate, default: same as input         |
| `--bitdepth`   | Output bit depth: PCM\_16 / 24 / 32 / FLOAT        |
| `--n_fft`      | STFT window size (affects frequency resolution)    |
| `--hop_length` | STFT hop length                                    |

---

## Recommended Parameter Table

| Sample Rate (Hz) | Recommended `n_fft` | Frequency Resolution ≈ `sr / n_fft` (Hz) | Recommended `hop_length` |
| ---------------- | ------------------- | ---------------------------------------- | ------------------------ |
| 44,100           | 4096                | ≈ 10.77 Hz                               | 1024                     |
| 48,000           | 4096                | ≈ 11.72 Hz                               | 1024                     |
| 96,000           | 8192                | ≈ 11.72 Hz                               | 2048                     |

---

## Disclaimer

> This project is not intended for “restoring” or “real repair” of audio.
>
> It only serves to mock the metaphysical “AI restoration” practices of some platforms.
>
> The author is **not responsible** for any misuse of this tool for faking, deception, or commercial purposes.


