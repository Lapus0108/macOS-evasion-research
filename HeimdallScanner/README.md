## 🧰 Purpose

**HeimdallScanner** is meant to determine how easily a system can be identified as a virtualized or sandboxed environment. This Python toolkit can be used to evaluate the efficiency of certain anti-fingerprinting techniques, supporting researchers in improving the resistence to VM evasion. 

## 📁 Modules

The core functionality of the system scanner is divided across several modules that scan:
  - Hardware & software configuration
  - Artifacts of virtualization software 
  - Connected devices & peripherals
  - User activity

## 📦 Requirements

This tool is specially designed for **macOS systems** and requires Python 3.8 or newer.

To install the dependencies:

```bash
cd HeimdallScanner
pip install -r requirements.txt
```

## 💻 How to run it?

The scanner can be executed as a script using the Python utility, an approach which allows the user to disable or enable modules, as well as to extend its functionality:
```bash
python HeimdallScanner.py [options]
```

An alternative is to generate a standalone Mach-O binary using PyInstaller, allowing the scanner to be executed without relying on the Python runtime. Installation instructions for PyInstaller can be found at [this link](https://pyinstaller.org/en/stable/installation.html). To create a single executable file, the following command can be used:
```bash
pyinstaller --onefile --add-data "modules/paths.json:modules" HeimdallScanner.py
```

## 🔹 Usage
**HeimdallScanner** supports 2 command-line options:
```bash
-v, --verbose     Display additional details about the checks that detected a virtual machine
-f, --full-paths  Run system utilities using their full path instead of only the name (ex:
'/usr/sbin/system_profiler' instead of 'system_profiler')
```