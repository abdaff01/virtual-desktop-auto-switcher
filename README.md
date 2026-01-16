# Virtual Desktop Auto-Switcher

A Windows utility with a Tkinter GUI that automatically cycles through virtual desktops
(1 → 2 → ... → n → 1) using keyboard shortcuts via PyAutoGUI.

## Features
- Set number of desktops (2–10)
- Set switch interval (1–60 seconds)
- Start/Stop switching
- Status indicator + current desktop display

## Requirements
- Windows 10/11 with Virtual Desktops enabled
- Python 3.9+ recommended

## Install
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
