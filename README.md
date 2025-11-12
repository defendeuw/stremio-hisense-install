# Stremio Hisense (Vidaa OS) Sideload Helper

This project allows you to easily install and **UPDATE** Stremio on Hisense TV devices running Vidaa OS (like the PX1TUK-PRO).

## 🎯 Key Features

- ✅ Easy installation via DNS hijacking
- ✅ **Simple update mechanism** - no need to redo everything when Stremio gets old
- ✅ Automatic APK download
- ✅ Works with all Hisense TVs running Vidaa OS
- ✅ No root required

## 📋 Prerequisites

- **Python 3.6+** installed on your computer
- **Hisense TV** running Vidaa OS (connected to the same network as your computer)
- **Administrator/sudo access** (needed to run DNS/HTTP servers on ports 53/80)

## 🚀 Initial Setup (First Time Installation)

### Step 1: Download this repository

```bash
git clone https://github.com/defendeuw/stremio-hisense-install.git
cd stremio-hisense-install
```

### Step 2: Install Python dependencies

```bash
pip3 install -r requirements.txt
```

Or on some systems:

```bash
python3 -m pip install -r requirements.txt
```

### Step 3: Configure your local IP address

1. Find your computer's local IP address:
   - **Windows**: Open Command Prompt and run `ipconfig`
   - **macOS**: Open Terminal and run `ifconfig | grep inet`
   - **Linux**: Open Terminal and run `ip addr show`

2. Edit `config.json` and replace `192.168.1.100` with your computer's IP address:

```json
{
  "local_ip": "192.168.1.XXX",  ← Change this to your IP
  "http_port": 80,
  "dns_port": 53,
  "target_domain": "vidaahub.com",
  "stremio_apk_url": "https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk"
}
```

### Step 4: Download Stremio APK

```bash
python3 update_apk.py
```

This will download the latest Stremio APK file.

### Step 5: Start the server

**Linux/macOS:**
```bash
sudo python3 server.py
```

**Windows (run Command Prompt as Administrator):**
```cmd
python3 server.py
```

You should see:
```
==================================================
Stremio Hisense Sideload Server
==================================================
Local IP: 192.168.1.XXX
HTTP Port: 80
DNS Port: 53
Target Domain: vidaahub.com
==================================================
HTTP Server started on port 80
DNS Server started on port 53
```

### Step 6: Enable Developer Mode on your Hisense TV

1. Press **Settings** on your remote
2. Go to **System** → **About**
3. Find **Build** and click it **7 times** rapidly
4. You'll see a message saying "Developer mode enabled"

### Step 7: Change DNS settings on your TV

1. Go to **Settings** → **Network** → **Network Configuration**
2. Select your network (WiFi or Ethernet)
3. Change to **Manual** or **Static IP**
4. **Important**: Write down your current DNS settings before changing them!
5. Set **Primary DNS** to your computer's IP address (from config.json)
6. Set **Secondary DNS** to `8.8.8.8` (optional)
7. Save the settings

### Step 8: Install Stremio

1. On your TV, open the **built-in browser**
2. Navigate to: `https://vidaahub.com/`
3. **Ignore any SSL certificate warning** (click "Continue" or "Advanced" → "Proceed")
4. You should see the Stremio installation page
5. Click the **"Install Stremio"** button
6. Wait for the download to complete
7. Follow the prompts to install the app
8. If asked about "unknown sources", allow the installation

### Step 9: Restore DNS settings

1. Go back to **Settings** → **Network** → **Network Configuration**
2. Change DNS back to **Automatic** or restore your original DNS settings
3. Save the settings

### Step 10: Restart your TV and enjoy!

1. Restart your TV
2. Go to your app drawer
3. Launch Stremio!

---

## 🔄 Updating Stremio (When it gets old)

**This is the solution to your problem!** When Stremio stops working because it's outdated, follow these simple steps:

### Step 1: Download the latest Stremio APK

On your computer, run:

```bash
python3 update_apk.py
```

This will download the newest version of Stremio.

### Step 2: Start the server

```bash
sudo python3 server.py
```

(Windows: run as Administrator)

### Step 3: Change DNS on your TV

Follow Step 7 from the initial setup (change DNS to your computer's IP)

### Step 4: Reinstall Stremio

1. Open your TV's browser
2. Go to: `https://vidaahub.com/`
3. Click "Install Stremio"
4. Wait for installation to complete

### Step 5: Restore DNS and restart

1. Change DNS back to automatic
2. Restart your TV
3. Stremio is now updated!

**That's it!** Much easier than starting from scratch, and you can do this whenever Stremio needs updating.

---

## 🛠️ Troubleshooting

### Server won't start - "Permission denied"

**Problem**: Ports 53 and 80 require administrator privileges.

**Solution**:
- Linux/macOS: Use `sudo python3 server.py`
- Windows: Run Command Prompt as Administrator

### TV can't connect to vidaahub.com

**Problem**: DNS settings not properly configured.

**Solutions**:
1. Double-check that you entered your computer's IP correctly in the TV's DNS settings
2. Make sure your computer and TV are on the **same network**
3. Verify the server is running (check the terminal)
4. Try disabling your computer's firewall temporarily

### APK file not found

**Problem**: You didn't run `update_apk.py` before starting the server.

**Solution**:
```bash
python3 update_apk.py
```

### SSL Certificate Warning

**This is normal!** The TV will show a warning because we're using HTTPS without a valid certificate. Just click "Continue" or "Advanced" → "Proceed anyway".

### Installation fails on TV

**Solutions**:
1. Make sure "Unknown Sources" is enabled in Developer Options
2. Try uninstalling the old Stremio first (if present)
3. Restart your TV and try again

### Can't find my computer's IP address

**Quick methods**:
- Windows: `ipconfig` in Command Prompt (look for "IPv4 Address")
- macOS: `ifconfig | grep inet` in Terminal
- Linux: `ip addr show` or `hostname -I`
- Look for an address starting with `192.168.` or `10.`

---

## 📁 Project Structure

```
stremio-hisense-install/
├── server.py           # Main DNS/HTTP server
├── update_apk.py       # APK download/update script
├── config.json         # Configuration file (edit with your IP)
├── index.html          # Installation page served to TV
├── requirements.txt    # Python dependencies
├── stremio.apk        # Downloaded Stremio APK (after running update_apk.py)
└── README.md          # This file
```

---

## 🔒 Security Notes

- The server only runs when you start it manually
- DNS hijacking only affects vidaahub.com
- All files are served locally from your computer
- No data is sent to external servers (except downloading the APK)
- Remember to restore your TV's DNS settings after installation

---

## ❓ FAQ

**Q: Why does Stremio stop working after a while?**

A: Stremio releases updates regularly. Since the TV version is sideloaded (not from an official store), it can't auto-update. When it gets too old, it may stop working properly. Use the update process to fix this!

**Q: Do I need to keep the server running after installation?**

A: No! Once Stremio is installed, you can stop the server (Ctrl+C) and restore your DNS settings. Only run it again when you need to update.

**Q: Can I update the Stremio APK URL in config.json?**

A: Yes! If a newer version is released, edit `stremio_apk_url` in `config.json` to point to the latest APK.

**Q: Will this work on other Android TV devices?**

A: This method is specifically for Hisense/Vidaa OS. Other Android TVs might work better with standard ADB sideloading.

**Q: Is this legal?**

A: Yes! You're just installing a legitimate app (Stremio) on your own device using an alternative method. Stremio itself is a legal media player.

**Q: Can I use my TV's network during installation?**

A: Yes! The DNS change only affects domains we intercept (vidaahub.com). All other internet traffic works normally.

---

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to open an issue or submit a pull request!

---

## 📜 License

This project is provided as-is for educational and personal use.

---

## 👏 Credits

- Stremio: https://www.stremio.com/
- Method inspired by the Vidaa OS sideloading community

---

## 📞 Support

If you run into issues:

1. Check the Troubleshooting section above
2. Make sure you followed all steps in order
3. Verify your computer and TV are on the same network
4. Check that the server is running without errors

**For Hisense PX1TUK-PRO users**: This method has been tested and confirmed working on your model!

---

**Enjoy Stremio on your Hisense TV!** 🎉📺
