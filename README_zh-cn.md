#  关于 FakeHiFi

Language：[English](https://github.com/Rckmuyue/FakeHiFi/blob/main/README.md "English") / [中文](https://github.com/Rckmuyue/FakeHiFi/blob/main/README_zh-cn.md "中文")

~~本程序用于修复 MP3 格式的音乐中被切的高频部分~~

实际上，本程序的目的是**讽刺某些音乐平台（如酷某音乐）所谓的“AI 修复”**。

> 提示： 本程序不具备任何真实的高频恢复能力！
>
> 它的“修复”只是人为伪造一段高频，看起来像是修好了而已。

---

## 效果演示

使用音乐：**周深 - 光亮**  
原素材信息：**48KHz / 24bit**

| 某音乐平台（酷某）所谓“修复”效果 | 本程序伪造高频效果 |
|-----------------------------------|----------------------|
| [![酷某修复](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_2.png?raw=true)](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_2.png?raw=true) | [![FakeHiFi 伪造](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_1.png?raw=true)](https://github.com/Rckmuyue/FakeHiFi/blob/main/IMG/demo_picture_1.png?raw=true) |

---

##  使用方法

###  安装依赖

```bash
pip install -r requirements.txt
```

---

### 方法一：交互模式

直接运行主程序，无需写参数，按提示输入：

```bash
python FakeHiFi.py
```

---

### 方法二：命令行参数模式

你可以使用参数方式运行：

```bash
python FakeHiFi.py input.wav --cutoff 22000 --maxfreq 47500 --transition 1500 --gain 1.5 --out output --out_sr 96000 --bitdepth PCM_32 --n_fft 8192 --hop_length 2048
```

#### 参数说明：

| 参数             | 含义                             |
| -------------- | ------------------------------ |
| `file`         | 输入音频文件路径（WAV）                  |
| `--cutoff`     | 伪造起始频率（Hz）默认 22000             |
| `--maxfreq`    | 伪造最高频率（Hz）默认 47500             |
| `--transition` | 交接区宽度（Hz）默认 1500               |
| `--gain`       | 伪造频段的幅度放大倍数，默认 1.5             |
| `--out`        | 输出目录，默认 `output`               |
| `--out_sr`     | 输出采样率，默认保持输入一致                 |
| `--bitdepth`   | 输出位深：PCM\_16 / 24 / 32 / FLOAT |
| `--n_fft`      | STFT 窗长（决定频率分辨率）               |
| `--hop_length` | STFT 跳帧长度                      |

---

## 推荐参数对照表

| 采样率 (Hz) | 推荐 `n_fft` | 频率分辨率 ≈ `sr / n_fft` (Hz) | 推荐 `hop_length` |
| -------- | ---------- | ------------------------- | --------------- |
| 44,100   | 4096       | ≈ 10.77 Hz                | 1024            |
| 48,000   | 4096       | ≈ 11.72 Hz                | 1024            |
| 96,000   | 8192       | ≈ 11.72 Hz                | 2048            |

---


##  声明

> 本项目不用于“还原”或“真实修复”音频。仅用于展示 AI 修复“玄学”操作的讽刺意义。
>
> 作者对任何使用此工具伪造、欺骗、商业用途的行为不承担任何责任。
