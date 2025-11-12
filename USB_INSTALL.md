# USB Installation Guide (Simplest Method)

> **This is the easiest way to install Stremio on your Hisense TV!**

## 🎯 What You Need

- USB flash drive (any size, formatted as FAT32 or exFAT)
- Computer with internet access
- Hisense TV with USB port

## 📋 Step-by-Step Instructions

### 1. Download Stremio APK

**Option A: Use our update script (recommended)**
```bash
# Clone this repository
git clone https://github.com/defendeuw/stremio-hisense-install.git
cd stremio-hisense-install

# Install dependencies
pip3 install -r requirements.txt

# Download latest Stremio APK (with automatic failover)
python3 update_apk.py
```

The APK will be saved as `stremio.apk` in the folder.

**Option B: Manual download**
1. Visit https://www.stremio.com/downloads
2. Click "Download for Android TV"
3. Save the file (rename to `stremio.apk` for clarity)

**Option C: Download from GitHub Release**
1. Go to https://github.com/defendeuw/stremio-hisense-install/releases
2. Download the latest release
3. Extract the ZIP file
4. APK is included inside

---

### 2. Copy APK to USB Drive

1. **Insert USB drive** into your computer
2. **Copy** the `stremio.apk` file to the root of the USB drive
3. **Safely eject** the USB drive

**USB Structure:**
```
USB Drive/
└── stremio.apk
```

---

### 3. Enable Developer Mode on TV

1. Press **Settings** on your TV remote
2. Go to **System** → **About**
3. Click on **Build** or **Build Number** **7 times** rapidly
4. You should see: "Developer mode enabled"

---

### 4. Enable Unknown Sources

1. Go to **Settings** → **Security & Restrictions**
2. Enable **Unknown Sources** (or **Install from Unknown Sources**)

---

### 5. Install from USB

1. **Insert USB drive** into your TV's USB port
2. Wait for notification or open **File Manager** / **Media** app
3. Navigate to USB drive (may be called "USB Device" or "External Storage")
4. Find `stremio.apk` file
5. Click on it and select **Install**
6. Wait for installation to complete
7. Click **Done** or **Open**

---

### 6. Launch Stremio

1. Go to **Apps** or **Applications** menu on TV
2. Find and launch **Stremio**
3. Log in with your Stremio account
4. Enjoy!

---

## 🔄 Updating Stremio via USB

When Stremio gets old and needs updating:

1. **Download new APK** (using update script or manually)
2. **Copy to USB drive**
3. **Plug USB into TV**
4. **Install** - it will update over the old version automatically
5. **Done!**

**No need to uninstall** - Android will update the existing app.

---

## ❓ FAQ

**Q: What USB format should I use?**
A: FAT32 or exFAT (most USB drives come pre-formatted correctly)

**Q: My TV doesn't detect the USB drive?**
A: Try a different USB port, reformat the drive, or try a different USB stick

**Q: Can I install other apps this way?**
A: Yes! Any Android APK can be installed via USB on Vidaa OS

**Q: Is this safer than DNS method?**
A: Both are equally safe. USB is simpler but requires physical access to TV

**Q: Can I delete the APK from USB after installation?**
A: Yes, the APK is only needed for installation

---

## 🆚 USB vs DNS Method Comparison

| Feature | USB Method | DNS Method |
|---------|-----------|------------|
| **Complexity** | ⭐⭐ Simple | ⭐⭐⭐⭐ Complex |
| **Setup Time** | 2 minutes | 15-20 minutes |
| **Requirements** | USB drive | Computer + Python |
| **Remote Install** | ❌ No (need physical access) | ✅ Yes (over network) |
| **Update Process** | Same as install | Same as install |
| **Best For** | One-time setup | Remote/frequent updates |

---

## 🎉 That's It!

USB installation is the **simplest method** for most users. Use the DNS method only if:
- You don't have physical access to your TV
- You want to update remotely from another room
- You're installing on multiple TVs over the network

**For most people, USB is the way to go!**
