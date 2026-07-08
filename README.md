<div align="center">

# 🎬 SATube

**Fast • Beautiful • Open Source Media Downloader**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](#)
[![Powered by yt-dlp](https://img.shields.io/badge/Powered_by-yt--dlp-ff69b4.svg)](https://github.com/yt-dlp/yt-dlp)

<pre><code>
╭──────────────────────────────────────╮
│                                      │
│  ███████╗  █████╗ ████████╗██╗   ██╗ │
│  ██╔════╝ ██╔══██╗╚══██╔══╝██║   ██║ │
│  ███████╗ ███████║   ██║   ██║   ██║ │
│  ╚════██║ ██╔══██║   ██║   ██║   ██║ │
│  ███████║ ██║  ██║   ██║   ╚██████╔╝ │
│  ╚══════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝  │
│                                      │
╰──────────────────────────────────────╯
</code></pre>

*A modern, interactive terminal application built for power users.*

</div>

---

## 📖 About SATube

SATube is **not** just another wrapper script. It is a full-fledged, premium Linux CLI application built on top of `yt-dlp` and `FFmpeg`. Designed to be keyboard-friendly, visually stunning, and highly modular, SATube brings the comfort of a GUI directly into your terminal.

## ✨ Features

- **🎨 Beautiful Terminal UI:** Powered by `Rich` and `Questionary`. No messy logs or text tearing.
- **🎥 Advanced Video & Audio:** Download up to 4K resolutions, extract audio (MP3, FLAC, WAV), and select custom formats.
- **🗂️ Queue Manager:** Paste multiple URLs, arrange them, and let SATube download them sequentially in the background.
- **📜 Download History:** Keep track of your downloads, search past files, and manage your media.
- **⚙️ Smart Configuration:** Remembers your favorite download folders, preferred quality, and formats automatically.
- **🖼️ Rich Metadata:** Automatically fetches and embeds thumbnails and metadata into your downloaded files.
- **🔔 Native Notifications:** Get desktop alerts when a download finishes.

---

## 🛠️ Prerequisites

Before installing, ensure your system has the following dependencies:

- **Python 3.12** or newer
- **FFmpeg** (Required for merging video/audio and format conversion)
- **pipx** (Required for safe, isolated Python CLI app installation)

---

## 🚀 Installation

SATube supports **Linux**, **macOS**, and **Windows**.

> **Requirements**
>
> - Python 3.12+
> - FFmpeg
> - pipx (recommended)

---

### 🐧 Linux

The installer automatically detects your distribution (Arch, Debian/Ubuntu, Fedora, etc.) and installs the required dependencies.

```bash
git clone https://github.com/sagarlamon/SATube.git
cd SATube

chmod +x install.sh
./install.sh
```

After installation, verify everything is working:

```bash
satube --version
```

Launch SATube:

```bash
satube
```

---

### 🍎 macOS

Install dependencies:

```bash
brew install ffmpeg pipx
pipx ensurepath
```

Clone and install:

```bash
git clone https://github.com/sagarlamon/SATube.git
cd SATube

pipx install .
```

Verify installation:

```bash
satube --version
```

Launch:

```bash
satube
```

---

### 🪟 Windows

Install FFmpeg:

```powershell
winget install -e --id Gyan.FFmpeg
```

Install pipx:

```powershell
python -m pip install --user pipx
pipx ensurepath
```

Restart PowerShell (or Command Prompt), then install SATube:

```powershell
git clone https://github.com/sagarlamon/SATube.git
cd SATube

pipx install .
```

Verify installation:

```powershell
satube --version
```

Launch:

```powershell
satube
```

---

## 🔄 Updating

If SATube was installed using **pipx**, updating is simple:

```bash
pipx upgrade satube
```

Or update directly from source:

```bash
git pull
pipx install . --force
```

---

## ❌ Uninstall

```bash
pipx uninstall satube
```

## 💻 Usage

SATube is fully interactive. To launch the main dashboard, simply open your terminal and type:

satube

### Dashboard Menu Options

| Option | Description |
| :--- | :--- |
| **Download Video** | Fetches the video, prompts for quality (Best, 1080p, Custom), and downloads it. |
| **Download Audio** | Extracts audio, allowing you to choose format (MP3, FLAC, etc.) and bitrate. |
| **Video Information**| Displays complete metadata (views, duration, description) without downloading. |
| **Available Formats**| Generates a beautiful table of all exact formats/codecs available for a URL. |
| **Queue Manager** | Add multiple URLs, reorder them, and process them in one batch. |
| **Settings** | Set default download paths, toggle metadata embedding, and change UI themes. |

---

## 📂 File Structure & XDG Compliance

SATube respects your system's directory standards (XDG Base Directory Specification):

- **Configuration:** `~/.config/satube/config.json`
- **History & Data:** `~/.local/share/satube/history.json`
- **Background Logs:** `~/.local/share/satube/logs/satube.log`
- **Default Downloads:** `~/Downloads/SATube/` (Can be changed in settings)

---

## 🗺️ Roadmap

**v1.0 (Current)**
- [x] Core Video/Audio Engine
- [x] Rich UI & Dashboard
- [x] Queue & History Managers
- [x] Settings Configuration

**v1.5 (Upcoming)**
- [ ] Full Playlist Support (Range selection)
- [ ] Subtitle Downloading
- [ ] Resume interrupted downloads dynamically

**v2.0 (Future)**
- [ ] In-Terminal YouTube Search
- [ ] Plugin System
- [ ] Download Scheduler

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<div align="center">
<i>Built with ❤️ for the Open Source Community.</i>
</div>
