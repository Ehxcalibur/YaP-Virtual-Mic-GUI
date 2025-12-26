# Void Mic 🎙️

**Void Mic** is a robust, cross-distribution Linux application that creates a high-performance virtual microphone. It allows you to inject audio from local files or web streams (YouTube, etc.) directly into voice chat applications like Discord, Zoom, or OBS, all while maintaining a sleek "Void and Violet" aesthetic.

![Void Mic Banner](https://via.placeholder.com/800x200?text=Void+Mic+Application)

## 🚀 Features

*   **Virtual Audio Injection**: seamlessly routes audio to a virtual input device (`Void-Virtual-Input`).
*   **Universal Compatibility**: Works on Debian/Ubuntu, Fedora, Arch, and openSUSE.
*   **Web & Local Playback**: Powered by `mpv` and `yt-dlp` to play local files or stream directly from YouTube and other sites.
*   **Real-time Monitoring**: Toggle monitoring to hear what you are broadcasting without any echo.
*   **Audio-Only Mode**: Stream audio from videos without opening distracting video popups.
*   **Zero-Config Setup**: Automatic dependency handling and virtual environment creation.
*   **Desktop Integration**: Auto-creates a desktop shortcut for easy access.

## 🛠️ Installation

### Prerequisites
*   A Linux distribution (Debian, Ubuntu, Fedora, Arch, or openSUSE based).
*   `python3` installed on your system.

### Quick Start
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/void-mic.git
    cd void-mic
    ```

2.  **Launch the Application**
    Run the launcher script. It will automatically detect your OS, install necessary system dependencies (ffmpeg, mpv, etc.), and set up a Python virtual environment.
    ```bash
    ./launch.sh
    ```
    *Note: You may be prompted for your sudo password during the initial installation of system dependencies.*

3.  **Create Shortcut**
    On your first run, you will be asked if you want to create a desktop shortcut. Click **YES** for instant access in the future.

## 📖 Usage

### 1. The Interface
*   **Input Field**: Paste a URL (YouTube, Twitch, etc.) or file path.
*   **Browse File**: Select a local audio/video file.
*   **Play/Stop**: Control playback.
*   **Monitor Toggle**: Switch this **ON** to hear the audio through your speakers. Switch **OFF** to only send audio to the virtual mic (silent to you).

### 2. Configure Your Apps
Once Void Mic is running, configure your target application (e.g., Discord):
1.  Go to **User Settings** > **Voice & Video**.
2.  Set **Input Device** to **Void-Virtual-Input** (or "VoidMic").
3.  *Recommended*: Disable "Noise Suppression" and "Echo Cancellation" in Discord for best audio quality.

## 📦 Dependencies
Void Mic leverages powerful open-source tools:
*   [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework.
*   [python-mpv](https://github.com/jaseg/python-mpv) - Libmpv bindings for playback.
*   [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Command-line video downloader for stream extraction.
*   [PipeWire](https://pipewire.org/) / PulseAudio - Audio server backend.

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
*Built with 💜 for the Linux Audio Community.*
