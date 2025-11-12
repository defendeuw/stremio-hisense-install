#!/usr/bin/env python3
"""
GitHub Release Preparation Script
Creates a release package with Stremio APK included
"""

import os
import sys
import json
import shutil
import zipfile
from datetime import datetime

# Configuration
RELEASE_DIR = "release"
PACKAGE_NAME = "stremio-hisense-install"

# Files to include in release
INCLUDE_FILES = [
    'server.py',
    'update_apk.py',
    'config.json',
    'index.html',
    'requirements.txt',
    'README.md',
    'USB_INSTALL.md',
    'QUICKSTART.md',
    '.gitignore'
]

# Color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_colored(message, color=Colors.OKBLUE):
    """Print colored message"""
    print(f"{color}{message}{Colors.ENDC}")


def create_release_package():
    """Create release package with APK"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("GitHub Release Package Creator", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()

    # Check if APK exists
    if not os.path.exists('stremio.apk'):
        print_colored("ERROR: stremio.apk not found!", Colors.FAIL)
        print_colored("Please run 'python3 update_apk.py' first to download the APK.", Colors.WARNING)
        print()
        response = input("Do you want to download it now? (y/n): ").strip().lower()
        if response == 'y':
            print()
            os.system('python3 update_apk.py')
            print()
            if not os.path.exists('stremio.apk'):
                print_colored("Download failed. Exiting.", Colors.FAIL)
                sys.exit(1)
        else:
            sys.exit(1)

    # Get APK info
    apk_size = os.path.getsize('stremio.apk') / (1024 * 1024)
    print_colored(f"✓ Found stremio.apk ({apk_size:.2f} MB)", Colors.OKGREEN)
    print()

    # Create release directory
    print_colored("[1/4] Creating release directory...", Colors.OKBLUE)
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
    os.makedirs(RELEASE_DIR)
    print_colored(f"  ✓ Created {RELEASE_DIR}/", Colors.OKGREEN)
    print()

    # Copy files
    print_colored("[2/4] Copying files...", Colors.OKBLUE)
    for filename in INCLUDE_FILES:
        if os.path.exists(filename):
            shutil.copy2(filename, os.path.join(RELEASE_DIR, filename))
            print_colored(f"  ✓ {filename}", Colors.OKCYAN)
        else:
            print_colored(f"  ⚠ {filename} not found, skipping", Colors.WARNING)

    # Copy APK
    shutil.copy2('stremio.apk', os.path.join(RELEASE_DIR, 'stremio.apk'))
    print_colored(f"  ✓ stremio.apk", Colors.OKCYAN)
    print()

    # Create installation instructions
    print_colored("[3/4] Creating INSTALL.txt...", Colors.OKBLUE)
    install_txt = """
STREMIO HISENSE TV INSTALLER
=============================

Thank you for downloading! You have two installation options:

OPTION 1: USB INSTALLATION (EASIEST - RECOMMENDED)
==================================================

1. Copy 'stremio.apk' to a USB flash drive
2. Plug USB into your Hisense TV
3. Enable Developer Mode:
   - Settings → System → About
   - Click "Build" 7 times
4. Enable Unknown Sources:
   - Settings → Security → Unknown Sources → Enable
5. Open File Manager on TV → USB → stremio.apk
6. Click Install → Done!

See USB_INSTALL.md for detailed instructions.


OPTION 2: DNS INSTALLATION (ADVANCED)
======================================

Use this if you want to install remotely over network.

1. Install Python 3.6+ on your computer
2. Edit config.json with your computer's IP address
3. Run: pip3 install -r requirements.txt
4. Run: sudo python3 server.py
5. Follow steps in README.md

See README.md for detailed instructions.


UPDATING STREMIO
================

When Stremio gets old:
- USB Method: Download new APK, copy to USB, install (2 min)
- DNS Method: Run update_apk.py, start server, reinstall (5 min)


NEED HELP?
==========

- Full Documentation: README.md
- USB Guide: USB_INSTALL.md
- Quick Reference: QUICKSTART.md
- Issues: https://github.com/defendeuw/stremio-hisense-install/issues


TESTED ON
=========

✓ Hisense PX1TUK-PRO
✓ Hisense U7G Series
✓ Hisense U8G Series
✓ Most Hisense TVs with Vidaa OS 2.0+

Enjoy Stremio on your TV!
"""
    with open(os.path.join(RELEASE_DIR, 'INSTALL.txt'), 'w') as f:
        f.write(install_txt.strip())
    print_colored("  ✓ Created installation instructions", Colors.OKGREEN)
    print()

    # Create ZIP archive
    print_colored("[4/4] Creating ZIP archive...", Colors.OKBLUE)
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_filename = f"{PACKAGE_NAME}-{timestamp}.zip"

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(PACKAGE_NAME, os.path.relpath(file_path, RELEASE_DIR))
                zipf.write(file_path, arcname)
                print_colored(f"  + {arcname}", Colors.OKCYAN)

    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)
    print()
    print_colored(f"  ✓ Created {zip_filename} ({zip_size:.2f} MB)", Colors.OKGREEN)
    print()

    # Summary
    print_colored("=" * 60, Colors.OKGREEN)
    print_colored("✓ Release Package Ready!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.OKGREEN)
    print()
    print_colored("Package Details:", Colors.HEADER)
    print_colored(f"  File: {zip_filename}", Colors.OKCYAN)
    print_colored(f"  Size: {zip_size:.2f} MB", Colors.OKCYAN)
    print_colored(f"  Contents: {len(INCLUDE_FILES) + 2} files (including APK)", Colors.OKCYAN)
    print()
    print_colored("Next Steps for GitHub Release:", Colors.HEADER)
    print_colored("  1. Go to: https://github.com/defendeuw/stremio-hisense-install/releases/new", Colors.OKBLUE)
    print_colored("  2. Create a new tag (e.g., v1.0.0)", Colors.OKBLUE)
    print_colored("  3. Title: 'Stremio Hisense Installer v1.0.0'", Colors.OKBLUE)
    print_colored(f"  4. Upload: {zip_filename}", Colors.OKBLUE)
    print_colored("  5. Add release notes (example below)", Colors.OKBLUE)
    print()
    print_colored("Suggested Release Notes:", Colors.HEADER)
    print()
    print("""# Stremio for Hisense TV (Vidaa OS)

Complete installer for Stremio on Hisense TVs running Vidaa OS.

## 📦 What's Included

- ✅ Stremio APK (latest version)
- ✅ USB installation guide (simplest method)
- ✅ DNS installation scripts (advanced method)
- ✅ Automatic update script with failover mirrors
- ✅ Complete documentation

## 🚀 Quick Start (USB Method - Recommended)

1. Download and extract this release
2. Copy `stremio.apk` to USB drive
3. Plug USB into your Hisense TV
4. Install via File Manager
5. Done!

See `USB_INSTALL.md` for detailed instructions.

## 🔄 Updates

When Stremio needs updating:
- **USB**: Download new release, install APK from USB
- **DNS**: Run `python3 update_apk.py` and follow steps

## ✅ Tested On

- Hisense PX1TUK-PRO
- Hisense U7G Series (Vidaa OS 4+)
- Hisense U8G Series (Vidaa OS 5+)
- Most Hisense TVs with Vidaa OS 2.0+

## 📚 Documentation

- Full guide: `README.md`
- USB installation: `USB_INSTALL.md`
- Quick reference: `QUICKSTART.md`

## 🆘 Support

If you encounter issues, check the troubleshooting guide in `README.md` or open an issue.
""")
    print()


if __name__ == "__main__":
    try:
        create_release_package()
    except KeyboardInterrupt:
        print_colored("\n\nCancelled by user.", Colors.WARNING)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n\nError: {e}", Colors.FAIL)
        sys.exit(1)
