# Building Windows EXE

This guide shows how to build a standalone Windows executable (.exe) for the Stremio Hisense Installer.

## Method 1: Pre-built Release (Easiest)

Download the pre-built EXE from GitHub Releases:
https://github.com/defendeuw/stremio-hisense-install/releases

## Method 2: Build It Yourself

### Prerequisites

- Python 3.6+ installed on Windows
- PyInstaller

### Step 1: Install PyInstaller

```cmd
pip install pyinstaller
```

### Step 2: Build the EXE

Navigate to the project folder and run:

```cmd
pyinstaller --onefile --windowed --name="StremioHisenseInstaller" --icon=icon.ico stremio_installer_gui.py
```

**Options explained:**
- `--onefile`: Package everything into one EXE
- `--windowed`: No console window (GUI only)
- `--name`: Name of the EXE file
- `--icon`: Custom icon (optional - create icon.ico first)

### Step 3: Find Your EXE

The EXE will be in: `dist/StremioHisenseInstaller.exe`

### Step 4: Create Distribution Package

1. Create a folder: `StremioHisenseInstaller/`
2. Copy these files:
   - `dist/StremioHisenseInstaller.exe`
   - `server.py`
   - `update_apk.py`
   - `config.json`
   - `index.html`
   - `requirements.txt`
   - `README.md`
   - `USB_INSTALL.md`
   - `INSTALL.txt`

3. Zip the folder

Users can extract and run `StremioHisenseInstaller.exe` directly!

## Method 3: Build with All Dependencies

For a completely standalone EXE that includes Python:

```cmd
pyinstaller --onefile --windowed ^
    --name="StremioHisenseInstaller" ^
    --add-data="server.py;." ^
    --add-data="update_apk.py;." ^
    --add-data="config.json;." ^
    --add-data="index.html;." ^
    --add-data="requirements.txt;." ^
    stremio_installer_gui.py
```

This creates a larger EXE but includes everything needed.

## Troubleshooting

**Error: "PyInstaller not found"**
```cmd
python -m pip install pyinstaller
```

**EXE won't run**
- Make sure all required files are in the same folder
- Run as Administrator (required for ports 80 and 53)

**Antivirus blocks EXE**
- Add exception for the EXE
- This is common with PyInstaller - the EXE is safe

## Creating an Icon

Create `icon.ico` using online tools:
- https://convertio.co/png-ico/
- Upload a 256x256 PNG
- Download as icon.ico

## Advanced: Auto-updater

To add auto-update functionality, consider:
- GitHub releases API
- Check for updates on startup
- Download new version automatically

## Distribution

Once built, you can:
1. Upload to GitHub Releases
2. Share directly with users
3. Sign the EXE (optional, prevents warnings)

## Notes

- EXE must run as Administrator (for DNS/HTTP ports)
- Windows Defender may flag it (false positive)
- Total size: ~15-20 MB including dependencies
- Works on Windows 7, 8, 10, 11
