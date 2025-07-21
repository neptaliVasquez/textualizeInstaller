# 🧪 POC Installer (Textualize)

This is a proof-of-concept terminal-based installer built with [Textual](https://github.com/Textualize/textual), a modern TUI (Text User Interface) framework for Python.

## 📋 Features

- Interactive, scrollable terminal UI
- SSL certificate setup form with multiple fields
- Simple screen navigation (Next / Back)
- Clean layout using `Textual` components like `Label`, `TextArea`, `Button`, and `VerticalScroll`

## ⚙️ Requirements

- Python 3.9+
- [Textual](https://pypi.org/project/textual/)
  
## 📦 Installation

It is recommended to create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Or manually install dependencies
```bash
pip install textual
```


# 🚀 Running the Installer
```bash
python poc.py
```