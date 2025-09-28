# 🚀 Gujarati Font Converter

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/badge/Download-.exe-red.svg)](#-quick-download)

A beautiful and powerful tool to convert Unicode Gujarati text to **35+ different non-Unicode Gujarati fonts**. Available as both **ready-to-use executables** and **Python source code**.

## 🎯 Quick Download

**No Python installation required!** Just download and double-click to run:

- 📱 **[Beautiful Gujarati Converter.exe](executables/Beautiful%20Gujarati%20Converter.exe)** *(12.4 MB)*
  - Professional card-based design
  - Clean, modern interface
  
- 🌙 **[Ultra-Modern Gujarati Converter.exe](executables/Ultra-Modern%20Gujarati%20Converter.exe)** *(12.4 MB)*
  - Sleek dark theme
  - Smooth animations and effects

## ✨ Features

- **🎨 Beautiful User Interfaces** - Two stunning GUI designs to choose from
- **📱 35+ Font Support** - Convert to Shree-Guj-0768, Krishna, Akshar, Samyak, and many more
- **🛡️ Smart Protection** - Advanced IP ban prevention with intelligent delays
- **⚡ Real-time Progress** - Live conversion tracking with resume capability
- **📁 File Operations** - Easy load/save functionality with drag-and-drop support
- **💻 Cross-platform** - Works on Windows, Mac, and Linux (source code)

## 🖼️ Screenshots

### Beautiful GUI - Professional Design
*Clean card-based layout with modern styling*

### Ultra-Modern GUI - Dark Theme  
*Sleek dark interface with smooth hover effects*

## 🚀 Getting Started

### Option 1: Download Executable (Recommended)
1. Download your preferred GUI from the links above
2. Double-click the `.exe` file to run
3. Start converting Gujarati text immediately!

### Option 2: Run from Source Code
```bash
# Clone the repository
git clone https://github.com/yourusername/gujarati-font-converter.git
cd gujarati-font-converter

# Install dependencies
pip install -r requirements.txt

# Run Beautiful GUI
python src/beautiful_gujarati_gui.py

# Run Ultra-Modern GUI
python src/ultra_modern_gui.py

# Command Line Usage
python src/multi_font_converter.py "તમારો ટેક્સ્ટ અહીં"
```

## 📖 Usage Guide

### GUI Applications
1. **Launch** any GUI application
2. **Select Font** from dropdown (35+ options available)
3. **Enter Text** directly or load from file
4. **Click Convert** and watch real-time progress
5. **Save Output** or copy to clipboard

### Command Line Interface
```bash
# Basic conversion
python src/multi_font_converter.py "ગુજરાતી ટેક્સ્ટ"

# Use specific font  
python src/multi_font_converter.py "ગુજરાતી ટેક્સ્ટ" --font krishna

# Convert from file
python src/multi_font_converter.py --input input.txt --output converted.txt --font akshar

# List all available fonts
python src/multi_font_converter.py --list-fonts
```

## 📊 Supported Fonts (35+)

<details>
<summary><b>📝 Click to see all supported fonts</b></summary>

| Font Key | Font Name | Font Family |
|----------|-----------|-------------|
| `shree0768` | Shree-Guj-0768 | Shree-Guj-0768, Shree-Guj-0768W |
| `krishna` | Krishna | Krishna, KrishnaWeb |
| `akshar` | Akshar | Akshar, AksharWeb |
| `samyak` | Samyak | Samyak, SamyakWeb |
| `noto` | Noto Sans Gujarati | NotoSansGujarati |
| ... | *Use --list-fonts for complete list* | ... |

</details>

## 🏗️ Project Structure

```
gujarati-font-converter/
├── 📁 src/                              # Source code
│   ├── 🎨 beautiful_gujarati_gui.py     # Professional GUI
│   ├── 🌙 ultra_modern_gui.py          # Dark theme GUI  
│   ├── 🖥️ multi_font_converter.py      # CLI interface
│   └── 🗂️ font_mapping.py              # 35+ fonts database
├── 📁 executables/                      # Ready-to-run .exe files
│   ├── Beautiful Gujarati Converter.exe
│   └── Ultra-Modern Gujarati Converter.exe
├── 📁 docs/                             # Documentation
├── 📄 README.md                         # This file
├── 📋 requirements.txt                  # Python dependencies
└── 📝 LICENSE                           # MIT License
```

## 🔧 Building Your Own Executable

Want to create your own customized .exe files?

```bash
# Install PyInstaller
pip install pyinstaller

# Build Beautiful GUI executable
pyinstaller --onefile --windowed --name "Beautiful Gujarati Converter" src/beautiful_gujarati_gui.py

# Build Ultra-Modern GUI executable  
pyinstaller --onefile --windowed --name "Ultra-Modern Gujarati Converter" src/ultra_modern_gui.py

# Find your .exe files in the dist/ folder
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork** the repository
2. **🔧 Create** your feature branch (`git checkout -b feature/amazing-feature`)
3. **💻 Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **🚀 Push** to the branch (`git push origin feature/amazing-feature`)
5. **📝 Open** a Pull Request

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## ⚠️ Usage Guidelines

- Uses public font conversion APIs - please respect rate limits
- Includes smart delay mechanisms to prevent IP blocking
- For educational and personal use
- Commercial use permitted under MIT license terms

## 🙋‍♂️ Support & Help

- **🐛 Bug Reports**: [Create an issue](../../issues/new)
- **💡 Feature Requests**: [Request features](../../issues/new?template=feature_request.md)
- **⭐ Star the repo**: If you find this useful!
- **📢 Share**: Help others discover this tool

## 📈 Download Stats

- **Total Downloads**: See [releases](../../releases) page
- **Latest Version**: Check [releases](../../releases/latest) for updates
- **File Sizes**: ~12.4MB per executable (includes all dependencies)

---

<div align="center">

**Made with ❤️ for the Gujarati Community**

[⬇️ Download Executables](executables/) • [🌟 Star Repo](../../stargazers) • [🐛 Report Issue](../../issues)

**No installation required • Just download and run! 🚀**

</div>