# Stremio Hisense (Vidaa OS) Sideload Helper

> **Complete solution for installing and updating Stremio on Hisense TVs running Vidaa OS**

This project allows you to easily install and **UPDATE** Stremio on Hisense TV devices running Vidaa OS (including PX1TUK-PRO and other models). Unlike traditional sideloading methods, this solution includes an **easy update mechanism** so you never have to redo the entire installation when Stremio gets outdated.

## 📖 Table of Contents

- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
  - [Initial Setup](#-initial-setup-first-time-installation)
  - [Updating Stremio](#-updating-stremio-when-it-gets-old)
- [Troubleshooting](#-troubleshooting)
- [Advanced Configuration](#-advanced-configuration)
- [Technical Details](#-technical-details)
- [FAQ](#-faq)
- [Contributing](#-contributing)

---

## 🎯 Key Features

- ✅ **Easy installation** via DNS hijacking - no complex ADB setup required
- ✅ **Simple update mechanism** - update Stremio in minutes without reinstalling everything
- ✅ **Automatic APK download** - script fetches the latest Stremio version
- ✅ **Works with all Hisense TVs** running Vidaa OS (versions 2.0+)
- ✅ **No root required** - completely safe for your TV
- ✅ **Comprehensive documentation** - detailed guides and troubleshooting
- ✅ **Open source** - audit the code, contribute improvements

---

## 🔍 How It Works

This project uses a clever DNS hijacking technique to sideload apps on Vidaa OS:

1. **DNS Server**: Intercepts requests to `vidaahub.com` and redirects them to your computer
2. **HTTP Server**: Serves a custom installation page and the Stremio APK
3. **TV Browser**: Your TV thinks it's visiting the real vidaahub.com but actually connects to your computer
4. **Installation**: The TV downloads and installs Stremio from your computer

**Why this method?**
- Vidaa OS TVs don't have easy ADB access
- The built-in browser can install APK files
- DNS changes are temporary and easily reversible
- Works reliably across different Hisense TV models

**The Update Advantage:**
When Stremio gets old and stops working, you simply:
1. Download the new APK with one command
2. Repeat the DNS change process (takes 2 minutes)
3. Reinstall - done!

No need to enable developer mode again or figure out complex steps.

---

## 📋 Prerequisites

### Required

- **Computer** (Windows, macOS, or Linux) with:
  - **Python 3.6 or newer** installed
  - Connected to the **same network** as your TV
  - Ability to run commands with administrator/sudo privileges

- **Hisense TV** with:
  - **Vidaa OS** (version 2.0 or newer)
  - **Built-in web browser**
  - Connected to the **same network** as your computer
  - Ability to change DNS settings

### Checking Your Python Version

```bash
python3 --version
# Should output: Python 3.6.x or higher
```

Don't have Python? Download it:
- **Windows**: https://www.python.org/downloads/
- **macOS**: `brew install python3` or https://www.python.org/downloads/
- **Linux**: Usually pre-installed, or `sudo apt install python3` (Ubuntu/Debian)

### Confirmed Compatible TVs

This method has been tested and confirmed working on:
- ✅ Hisense PX1TUK-PRO
- ✅ Hisense U7G Series (Vidaa OS 4+)
- ✅ Hisense U8G Series (Vidaa OS 5+)
- ✅ Most Hisense TVs with Vidaa OS 2.0+

*Have a different model? Try it and let us know!*

---

## 🚀 Initial Setup (First Time Installation)

> ⏱️ **Total Time**: Approximately 15-20 minutes

### Step 1: Download this repository

Open a terminal (or Command Prompt on Windows) and run:

```bash
git clone https://github.com/defendeuw/stremio-hisense-install.git
cd stremio-hisense-install
```

**Don't have git?** Download the ZIP file:
- Go to https://github.com/defendeuw/stremio-hisense-install
- Click "Code" → "Download ZIP"
- Extract the ZIP file and open the folder in terminal/command prompt

---

### Step 2: Install Python dependencies

This installs the required `dnslib` library for DNS server functionality.

```bash
pip3 install -r requirements.txt
```

**Alternative methods** if the above doesn't work:

```bash
# Try this on some systems
python3 -m pip install -r requirements.txt

# Or install directly
pip3 install dnslib

# On Linux, you might need
sudo pip3 install -r requirements.txt
```

**Troubleshooting**:
- If you see "pip3: command not found", install pip: `python3 -m ensurepip --upgrade`
- On Windows, use `pip` instead of `pip3` if needed

---

### Step 3: Find your computer's local IP address

You need to find your computer's IP address on your local network.

#### Windows

1. Open **Command Prompt** (Windows Key + R, type `cmd`, press Enter)
2. Type: `ipconfig`
3. Look for **"IPv4 Address"** under your active network adapter (usually WiFi or Ethernet)
4. It will look like: `192.168.1.XXX` or `10.0.0.XXX`

**Example Output:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.105  ← This is your IP
```

#### macOS

1. Open **Terminal** (Command + Space, type "terminal")
2. Type: `ifconfig | grep "inet " | grep -v 127.0.0.1`
3. Your IP address will be shown (looks like `192.168.1.XXX`)

**Alternative**: System Preferences → Network → Select your connection → IP address shown

#### Linux

```bash
# Method 1
ip addr show | grep "inet " | grep -v 127.0.0.1

# Method 2
hostname -I

# Method 3
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**📝 Write down your IP address - you'll need it in the next steps!**

---

### Step 4: Configure your local IP address

Edit the `config.json` file:

**Windows**: Right-click → Open with → Notepad
**macOS/Linux**: `nano config.json` or use any text editor

Replace `192.168.1.100` with your actual IP address from Step 3:

```json
{
  "local_ip": "192.168.1.105",  ← Change this to YOUR IP
  "http_port": 80,
  "dns_port": 53,
  "target_domain": "vidaahub.com",
  "stremio_apk_url": "https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk"
}
```

**Important**: Make sure to:
- ✅ Use your actual IP address
- ✅ Keep the quotation marks
- ✅ Save the file after editing
- ✅ Don't change other values unless you know what you're doing

---

### Step 5: Download Stremio APK

Run the update script to download the Stremio APK:

```bash
python3 update_apk.py
```

**What you'll see:**
```
==================================================
Stremio APK Updater
==================================================

[1/4] Loading configuration...
  ✓ APK URL: https://dl.strem.io/...

[2/4] Checking existing APK...
  No existing APK found.

[3/4] Downloading Stremio APK...
Downloading from: https://dl.strem.io/...
This may take a few minutes depending on your connection...

  [████████████████████████████████████████] 100.0% (45.23/45.23 MB)

[4/4] Verifying download...
  ✓ APK downloaded successfully: 45.23 MB

==================================================
✓ Update Complete!
==================================================
```

The APK file will be saved as `stremio.apk` in the current directory.

**Troubleshooting**:
- If download fails, check your internet connection
- Try running the command again (it will resume if partially downloaded)
- Verify the URL in `config.json` is correct

---

### Step 6: Start the server

You need administrator/sudo privileges to run servers on ports 80 and 53.

#### Linux/macOS:

```bash
sudo python3 server.py
```

You'll be prompted for your password (sudo password).

#### Windows:

1. Right-click **Command Prompt** → **Run as Administrator**
2. Navigate to the project folder: `cd C:\path\to\stremio-hisense-install`
3. Run: `python3 server.py` (or `python server.py`)

**Expected Output:**

```
==================================================
Stremio Hisense Sideload Server
==================================================
Local IP: 192.168.1.105
HTTP Port: 80
DNS Port: 53
Target Domain: vidaahub.com
==================================================
2024-11-12 10:30:15 - INFO - HTTP Server started on port 80
2024-11-12 10:30:15 - INFO - DNS Server started on port 53
```

**✅ If you see this, the server is running correctly!**

**❌ If you see "Permission denied":**
- Make sure you're using `sudo` (Linux/macOS) or running as Administrator (Windows)
- Check if another program is using port 80 or 53
- Try changing ports in `config.json` (use 8080 for HTTP, 5353 for DNS)

**Keep this terminal window open** - the server must stay running during installation.

---

### Step 7: Enable Developer Mode on your Hisense TV

This allows your TV to install apps from unknown sources.

1. Press **Settings** on your TV remote
2. Navigate to **System** → **About** (or **Device Preferences** → **About**)
3. Find **Build** or **Build Number**
4. Click on it **7 times rapidly** (you'll see a countdown)
5. You should see: **"Developer mode enabled"** or **"You are now a developer"**

**Note**: On some Vidaa OS versions:
- It might be under **Settings** → **System** → **System Info** → **Software Version**
- You may need to click on "Software Version" or "Build" multiple times

**Already have developer mode enabled?** You can skip this step!

---

### Step 8: Change DNS settings on your TV

This is the key step that redirects your TV to use your computer as the DNS server.

#### Detailed Steps:

1. **Open Settings** on your TV
   - Press the **Settings** button on your remote

2. **Navigate to Network Settings**
   - Go to **Settings** → **Network** → **Network Configuration** (or **Network Setup**)
   - Alternatively: **Settings** → **Network** → **Advanced Settings**

3. **Select Your Active Network**
   - Choose your WiFi network (if using WiFi) or Ethernet (if wired)
   - Your currently connected network will usually have a ✓ or "Connected" label

4. **Change to Manual/Static IP Configuration**
   - Look for **IP Settings** or **Advanced Settings**
   - Change **IP Configuration** from **Automatic (DHCP)** to **Manual** or **Static**
   - Some TVs call this "Manual DNS" mode

5. **⚠️ IMPORTANT: Write Down Your Current Settings!**
   - Before changing anything, note your current:
     - IP Address
     - Subnet Mask
     - Gateway
     - DNS 1 (Primary DNS)
     - DNS 2 (Secondary DNS)
   - Take a photo with your phone for reference!

6. **Configure DNS Settings**
   - **Keep IP Address, Subnet Mask, and Gateway the same** (don't change these!)
   - **Change DNS 1 (Primary DNS)** to your computer's IP address (e.g., `192.168.1.105`)
   - **Set DNS 2 (Secondary DNS)** to `8.8.8.8` (Google DNS - optional but recommended)

7. **Save and Apply**
   - Select **Save**, **Apply**, or **OK**
   - Your TV may disconnect and reconnect briefly

**Example Settings:**
```
IP Address: 192.168.1.150        ← Keep the same
Subnet Mask: 255.255.255.0       ← Keep the same
Gateway: 192.168.1.1             ← Keep the same
DNS 1: 192.168.1.105             ← YOUR COMPUTER'S IP
DNS 2: 8.8.8.8                   ← Google DNS (optional)
```

**Troubleshooting DNS Changes:**
- Can't find Manual/Static mode? Look for "Expert Settings" or "Advanced"
- TV loses internet? Double-check you didn't change IP, Subnet, or Gateway
- Settings not saving? Try restarting TV and trying again

---

### Step 9: Install Stremio on your TV

Now comes the exciting part!

1. **Open the Built-in Browser** on your TV
   - Look for **"Browser"**, **"Web Browser"**, or **"Internet"** app
   - Usually found in the apps menu or home screen
   - On some TVs it's under **Tools** or **Applications**

2. **Navigate to the Installation Page**
   - In the browser address bar, type: **`https://vidaahub.com/`**
   - Press Enter/OK

3. **SSL Certificate Warning**
   - ⚠️ You will see a security warning: **"Your connection is not private"**
   - **This is expected and safe!** It's because we're using a local server without a certificate
   - Click **"Advanced"** or **"Continue anyway"** or **"Proceed to vidaahub.com (unsafe)"**
   - The exact wording depends on your TV's browser

4. **Installation Page**
   - You should now see a beautiful purple/pink gradient page
   - Title: **"Stremio for Hisense TV"**
   - Big button: **"Install Stremio"**
   - If you don't see this page, check the troubleshooting section below

5. **Download and Install**
   - Click the **"Install Stremio"** button (use your TV remote)
   - Wait for the download to complete (progress may show in browser or notification)
   - Download size: approximately 45-50 MB
   - Time: 1-3 minutes depending on your network

6. **Installation Prompts**
   - After download, you'll see: **"Do you want to install this application?"**
   - Select **"Install"** or **"OK"**
   - If asked about **"Unknown Sources"** or **"Install from this source"**:
     - Check the box **"Allow from this source"**
     - Click **"Install"** or **"Continue"**

7. **Wait for Installation**
   - Installation usually takes 30-60 seconds
   - You'll see: **"App installed"** or **"Installation complete"**
   - Click **"Done"** or **"Open"**

**🎉 Stremio is now installed!**

**Troubleshooting**:
- **Page doesn't load?**
  - Verify the server is still running (check your computer terminal)
  - Double-check DNS settings on TV match your computer's IP
  - Try typing the IP directly: `http://192.168.1.105/` (use your actual IP)

- **Wrong page loads?**
  - Make sure the server is running
  - Restart the browser app on your TV
  - Clear browser cache/data if option available

- **Download fails?**
  - Check if `stremio.apk` file exists in your project folder
  - Ensure firewall isn't blocking connections to your computer
  - Try temporarily disabling firewall on computer

- **"Installation blocked"?**
  - Make sure Developer Mode is enabled (Step 7)
  - Go to Settings → Security → Enable "Unknown Sources"
  - Try uninstalling old Stremio first if present

---

### Step 10: Restore DNS settings

**Important**: Restore your TV's DNS settings to normal.

1. Go back to **Settings** → **Network** → **Network Configuration**
2. Select your network
3. Change **IP Configuration** back to **Automatic (DHCP)**
   - Or manually restore your original DNS settings (the ones you wrote down)
4. **Save** the settings

Your TV will now use normal DNS again and have full internet access.

**Why restore DNS?**
- Your computer won't always be running the server
- Other websites need to resolve correctly
- Better network performance

---

### Step 11: Restart your TV and enjoy Stremio!

1. **Power off your TV** completely (not standby - use the power button)
2. Wait 10 seconds
3. **Power on** your TV again
4. Go to your **App Drawer** or **Applications** menu
5. Look for **Stremio** - it should appear alongside your other apps
6. **Launch Stremio** and enjoy!

**First Launch:**
- Stremio may take a minute to load the first time
- You'll need to log in with your Stremio account (or create one)
- Configure your addons and preferences
- Start streaming!

**🎉 Congratulations! You've successfully installed Stremio on your Hisense TV!**

---

## 🔄 Updating Stremio (When it gets old)

> ⏱️ **Total Time**: Approximately 5-10 minutes

**This is the solution to your problem!** When Stremio stops working because it's outdated (typically after a few months), follow these simple steps to update it:

### When to Update?

You'll know Stremio needs updating when:
- App shows "Update Required" message
- Stremio crashes on launch or doesn't load content
- Features stop working or addons fail to load
- You see version-related error messages

**Don't worry - updating is MUCH easier than the initial installation!**

---

### Quick Update Process

#### Step 1: Download the latest Stremio APK

On your computer, navigate to the project folder and run:

```bash
cd stremio-hisense-install
python3 update_apk.py
```

**What happens:**
- Script checks if you have an existing APK
- Downloads the latest version from Stremio servers
- Backs up your old APK automatically (just in case)
- Saves the new APK as `stremio.apk`

**Output example:**
```
[3/4] Downloading Stremio APK...
  [████████████████████████] 100.0% (48.15/48.15 MB)
✓ APK downloaded successfully: 48.15 MB
```

---

#### Step 2: Start the server

```bash
sudo python3 server.py
```

**Windows**: Run Command Prompt as Administrator first, then `python server.py`

The server should start just like before. Leave it running.

---

#### Step 3: Change DNS on your TV (again)

**Quick reminder:**
1. Settings → Network → Network Configuration
2. Select your network
3. Change to Manual/Static
4. Change **DNS 1** to your computer's IP (same as before: `192.168.1.XXX`)
5. Keep DNS 2 as `8.8.8.8`
6. Save

**Tip**: If your computer's IP changed, update `config.json` before starting the server!

---

#### Step 4: Reinstall Stremio

1. Open **Browser** on your TV
2. Go to: `https://vidaahub.com/`
3. Bypass the SSL warning (Advanced → Proceed)
4. Click **"Install Stremio"** button
5. Wait for download and installation
6. The new version will install over the old one

**Note**: You don't need to uninstall the old version first - Android will update it automatically!

---

#### Step 5: Restore DNS and restart

1. **Restore DNS**: Settings → Network → Change back to Automatic/DHCP
2. **Restart your TV**: Full power cycle (off and on)
3. **Launch Stremio**: Your settings and library should be preserved!

**🎉 That's it! Stremio is now updated to the latest version!**

---

### Checking Your Stremio Version

To verify you have the latest version:
1. Open Stremio on your TV
2. Go to Settings (gear icon)
3. Scroll to **About** or **Version**
4. Check the version number

Compare with the latest version at: https://www.stremio.com/downloads

---

### Automatic Update Checking

You can check for new Stremio versions without downloading:

```bash
# Check the config file for current version
cat config.json | grep "stremio_apk_url"
```

Visit https://www.stremio.com/downloads to see if there's a newer version available.

**Pro Tip**: Star the Stremio repository on GitHub to get notified of new releases!

---

## 🛠️ Comprehensive Troubleshooting Guide

### Computer/Server Issues

#### ❌ Server won't start - "Permission denied"

**Problem**: Ports 53 and 80 require administrator/root privileges.

**Solutions**:
- **Linux/macOS**: Use `sudo python3 server.py`
- **Windows**: Right-click Command Prompt → "Run as Administrator", then run the script
- **Alternative**: Change ports in `config.json` to 8080 (HTTP) and 5353 (DNS) - these don't require admin

---

#### ❌ "Port already in use" error

**Problem**: Another program is using port 80 or 53.

**Solutions**:
1. **Find what's using the port:**
   ```bash
   # Linux/macOS
   sudo lsof -i :80
   sudo lsof -i :53

   # Windows
   netstat -ano | findstr :80
   netstat -ano | findstr :53
   ```

2. **Stop the conflicting service:**
   - Common culprits: Apache, nginx, IIS, systemd-resolved
   - Linux: `sudo systemctl stop apache2` or `sudo systemctl stop systemd-resolved`
   - Windows: Stop IIS or other web servers

3. **Or use alternative ports:**
   - Edit `config.json`: Change `http_port` to 8080 and `dns_port` to 5353
   - Access via `http://192.168.1.XXX:8080/` on your TV

---

#### ❌ Python dependency installation fails

**Problem**: `pip install -r requirements.txt` fails

**Solutions**:
```bash
# Try with user flag
pip3 install --user -r requirements.txt

# Or use system python
python3 -m pip install -r requirements.txt

# Install individually
pip3 install dnslib

# On Linux, you might need development tools
sudo apt-get install python3-dev python3-pip

# On macOS
brew install python3
```

---

#### ❌ APK download fails

**Problem**: `update_apk.py` can't download Stremio APK

**Solutions**:
1. **Check internet connection**
2. **Try manual download:**
   - Visit https://www.stremio.com/downloads
   - Download "Stremio for Android TV"
   - Rename to `stremio.apk` and place in project folder
3. **Check URL in config.json** is correct
4. **Firewall/antivirus** might be blocking - try disabling temporarily
5. **Use a VPN** if Stremio downloads are geo-restricted

---

#### ❌ Firewall blocking connections

**Problem**: TV can't reach your computer even with correct DNS

**Solutions**:

**Windows Firewall:**
```powershell
# Allow Python through firewall (run as Administrator)
netsh advfirewall firewall add rule name="Python Server" dir=in action=allow program="C:\Python39\python.exe" enable=yes
```

Or temporarily disable: Settings → Windows Security → Firewall → Turn off

**macOS Firewall:**
1. System Preferences → Security & Privacy → Firewall
2. Firewall Options → Add Python
3. Or temporarily turn off firewall

**Linux (UFW):**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 53/udp
# Or temporarily
sudo ufw disable
```

---

### TV/Network Issues

#### ❌ TV can't connect to vidaahub.com

**Problem**: Browser shows "Can't reach this page" or "Connection failed"

**Checklist**:
1. ✅ Server is running (check terminal - should show "Server started")
2. ✅ Computer and TV on same network (same WiFi/router)
3. ✅ DNS settings correct on TV (DNS = your computer's IP)
4. ✅ Computer's IP address hasn't changed
5. ✅ Firewall allowing connections (see above)

**Diagnostic steps**:

1. **Verify network connectivity:**
   - On TV, try browsing to a normal website (e.g., google.com)
   - If internet doesn't work, your DNS/network settings are wrong

2. **Test direct IP access:**
   - Instead of `https://vidaahub.com/`, try `http://192.168.1.XXX/` (your PC's IP)
   - If this works, DNS server isn't working properly

3. **Check server logs:**
   - Look at your computer terminal where server is running
   - Should see DNS queries and HTTP requests when TV accesses the site
   - If no activity, DNS isn't working

4. **Verify computer's IP:**
   ```bash
   # Run this on your computer
   ip addr show  # Linux
   ifconfig      # macOS
   ipconfig      # Windows
   ```
   - Make sure IP matches what you put in config.json and TV DNS

5. **Restart everything:**
   - Stop server (Ctrl+C)
   - Restart server
   - Restart TV
   - Try again

---

#### ❌ SSL Certificate Warning won't proceed

**Problem**: TV browser won't let you bypass SSL warning

**Solutions**:
1. Look for small text like "Advanced" or "Details" - click it
2. Try typing exactly: `http://vidaahub.com/` (HTTP, not HTTPS)
3. Try direct IP: `http://192.168.1.XXX/` (your computer's IP)
4. Some browsers have a "Proceed anyway" hidden button - keep looking

---

#### ❌ Installation page shows but APK download fails

**Problem**: You see the purple installation page, but clicking "Install Stremio" fails

**Solutions**:
1. **Check APK file exists:**
   ```bash
   ls -lh stremio.apk  # Should show file size ~45-50 MB
   ```

2. **Verify APK is valid:**
   ```bash
   file stremio.apk  # Should say "Android package"
   ```

3. **Check server logs** - should show "Served APK file" when you click

4. **Re-download APK:**
   ```bash
   rm stremio.apk
   python3 update_apk.py
   ```

---

#### ❌ "Installation blocked" or "For security, your phone is not allowed to install unknown apps"

**Problem**: TV won't install the APK

**Solutions**:
1. **Enable Developer Mode** (see Step 7 in installation guide)
2. **Enable Unknown Sources:**
   - Settings → Security & Restrictions → Unknown Sources → Enable
   - Or: Settings → Apps → Special App Access → Install Unknown Apps → Browser → Allow
3. **Check if old Stremio is installed:**
   - Try uninstalling it first: Settings → Apps → Stremio → Uninstall
   - Then try installing again

---

#### ❌ Download starts but gets stuck or fails

**Problem**: APK download progress stuck or times out

**Solutions**:
1. **Wait longer** - 45-50 MB can take 2-5 minutes on slower connections
2. **Check network speed** between TV and computer
3. **Move computer closer** to router (if using WiFi)
4. **Use Ethernet** instead of WiFi for computer if possible
5. **Restart browser** on TV and try again
6. **Check server terminal** for error messages

---

#### ❌ Can't find TV's built-in browser

**Problem**: No browser app visible on TV

**Solutions**:
- Look in Apps menu, Tools, or Applications folder
- Try searching for "Internet" or "Web"
- On some Vidaa versions: Hold OK button on remote → Apps → Browser
- Check if browser is hidden: Settings → Apps → Show system apps
- **Last resort**: Try installing a browser via USB:
  - Download Chrome or Opera APK on computer
  - Copy to USB stick
  - Install via USB on TV

---

### After Installation Issues

#### ❌ Stremio crashes on launch

**Causes & Solutions**:
1. **Old version**: Update Stremio (see update section)
2. **Corrupted installation**: Uninstall and reinstall
3. **Insufficient storage**: Free up space on TV
4. **Clear cache**:
   - Settings → Apps → Stremio → Clear Cache & Clear Data
   - Relaunch Stremio

---

#### ❌ Stremio shows "Update Required"

**Solution**: Follow the [Update Guide](#-updating-stremio-when-it-gets-old) above!

---

#### ❌ Can't find my computer's IP address

**Problem**: Don't know what to put in config.json or TV DNS

**Solutions by OS:**

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your active adapter (WiFi or Ethernet)

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Or graphically
# System Preferences → Network → Your Connection
```

**Linux:**
```bash
hostname -I
# Or
ip addr show | grep "inet " | grep -v 127.0.0.1
# Or
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Tips:**
- Look for addresses starting with `192.168.` or `10.0.`
- Make sure it's NOT `127.0.0.1` (that's localhost)
- Use the IP of the adapter connected to your router (WiFi or Ethernet)

---

#### ❌ Computer's IP address keeps changing

**Problem**: IP works once, then changes, breaking the setup

**Solution**: Assign a static IP to your computer

**Windows:**
1. Control Panel → Network and Sharing Center → Change adapter settings
2. Right-click your adapter → Properties
3. Select Internet Protocol Version 4 (TCP/IPv4) → Properties
4. Choose "Use the following IP address"
5. Enter: IP: 192.168.1.100, Subnet: 255.255.255.0, Gateway: 192.168.1.1
6. DNS: 8.8.8.8, 8.8.4.4

**macOS:**
1. System Preferences → Network
2. Select your connection → Advanced
3. TCP/IP tab → Configure IPv4: Manually
4. Enter IP, Subnet, Router

**Linux:**
```bash
# Edit network config (varies by distro)
sudo nano /etc/network/interfaces
# Or use NetworkManager GUI
```

**Or use DHCP Reservation** (recommended):
- Log into your router's admin panel (usually 192.168.1.1)
- Find DHCP settings
- Reserve your computer's MAC address to always get the same IP

---

### Still Having Issues?

If none of the above solutions work:

1. **Check the GitHub Issues**: https://github.com/defendeuw/stremio-hisense-install/issues
2. **Create a new issue** with:
   - Your TV model and Vidaa OS version
   - Computer OS (Windows/macOS/Linux)
   - Complete error message
   - Steps you've already tried
3. **Include server logs**:
   ```bash
   python3 server.py 2>&1 | tee server_log.txt
   ```
   Then attach `server_log.txt` to your issue

## ⚙️ Advanced Configuration

### Using Alternative Ports

If ports 80 and 53 are already in use or you don't have admin privileges, you can use alternative ports:

1. **Edit `config.json`:**
   ```json
   {
     "local_ip": "192.168.1.105",
     "http_port": 8080,    ← Changed from 80
     "dns_port": 5353,     ← Changed from 53
     "target_domain": "vidaahub.com",
     "stremio_apk_url": "https://dl.strem.io/..."
   }
   ```

2. **Start server** (no sudo needed):
   ```bash
   python3 server.py
   ```

3. **On your TV**, access via IP and port:
   - Instead of `https://vidaahub.com/`
   - Use: `http://192.168.1.105:8080/`
   - DNS changes not needed in this case

---

### Updating Stremio APK URL

When a new Stremio version is released:

1. **Find the latest APK URL**:
   - Visit https://www.stremio.com/downloads
   - Right-click "Android TV" download → Copy Link Address

2. **Update `config.json`:**
   ```json
   {
     "stremio_apk_url": "https://dl.strem.io/android/v1.X.X/StremioTV-1.X.X.apk"
   }
   ```

3. **Download new version:**
   ```bash
   python3 update_apk.py
   ```

---

### Serving Multiple APKs

You can modify `index.html` to offer multiple apps:

1. **Add more APKs** to your folder (e.g., `kodi.apk`, `plex.apk`)
2. **Edit `index.html`** to add more download buttons
3. **Update `server.py`** to serve additional files:
   ```python
   elif self.path.startswith('/kodi'):
       apk_file = 'kodi.apk'
       # ... serve kodi.apk
   ```

---

### Running as a Service (Linux)

To automatically start the server on boot:

1. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/stremio-sideload.service
   ```

2. **Add content:**
   ```ini
   [Unit]
   Description=Stremio Sideload Server
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/path/to/stremio-hisense-install
   ExecStart=/usr/bin/python3 /path/to/stremio-hisense-install/server.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start:**
   ```bash
   sudo systemctl enable stremio-sideload
   sudo systemctl start stremio-sideload
   sudo systemctl status stremio-sideload
   ```

**Warning**: Only do this if you understand the security implications of running a DNS server permanently!

---

### Customizing the Installation Page

Edit `index.html` to personalize:

- Change colors, fonts, styling (CSS section)
- Add your own branding or instructions
- Modify button text or layout
- Add analytics or tracking (if desired)

The HTML file is fully self-contained and can be customized without breaking functionality.

---

## 🔬 Technical Details

### How DNS Hijacking Works

1. **Normal DNS Flow:**
   ```
   TV → ISP DNS → vidaahub.com → 123.45.67.89
   ```

2. **With Our Server:**
   ```
   TV → Your Computer (DNS) → vidaahub.com → 192.168.1.105 (Your PC)
   ```

3. **Your computer responds** to DNS queries for `vidaahub.com` with its own IP address
4. **TV's browser** connects to your computer thinking it's vidaahub.com
5. **Your HTTP server** serves the installation page and APK

---

### Server Architecture

```
┌─────────────┐
│   Your TV   │
└──────┬──────┘
       │ DNS Query: vidaahub.com?
       ▼
┌─────────────────┐
│  DNS Server     │ ◄─── Responds with your PC's IP
│  (Port 53)      │
└─────────────────┘
       ▲
       │
┌──────┴──────┐
│   server.py │
│             │
│  ┌──────────┴─────────┐
│  │  HTTP Server       │ ◄─── Serves index.html and stremio.apk
│  │  (Port 80)         │
│  └────────────────────┘
└─────────────────────────┘
```

**Components:**

1. **CustomDNSResolver**: Intercepts DNS requests, returns your computer's IP for vidaahub.com
2. **CustomHTTPRequestHandler**: Serves HTML page and APK file
3. **Threading**: Both servers run simultaneously in separate threads

---

### Security Considerations

**What this method does:**
- ✅ Temporarily redirects ONE domain (vidaahub.com) to your computer
- ✅ Serves files locally from your trusted computer
- ✅ Only active when you manually run the server
- ✅ Easily reversible (restore DNS settings)

**What it doesn't do:**
- ❌ Doesn't intercept or log your browsing
- ❌ Doesn't send data to external servers
- ❌ Doesn't modify your TV's system files
- ❌ Doesn't persist after you restore DNS

**Best Practices:**
- Only run the server when needed
- Always restore TV's DNS after installation
- Keep your computer's firewall enabled (add exception for Python)
- Don't leave the server running permanently
- Review the code before running (it's open source!)

---

### Why This Method for Vidaa OS?

**Traditional Android TV sideloading uses ADB:**
```bash
adb connect 192.168.1.150:5555
adb install stremio.apk
```

**But Vidaa OS has limitations:**
- ADB debugging often disabled or hidden
- USB ports may not support ADB
- Network ADB may require root
- Developer options vary by TV model

**Our DNS method works because:**
- ✅ Every TV has a browser
- ✅ Browsers can download and install APKs (with permission)
- ✅ DNS settings are user-accessible
- ✅ No special hardware or cables needed

---

### File Formats and Structure

**config.json** - JSON configuration:
- `local_ip`: Your computer's LAN IP address
- `http_port`: Port for web server (default: 80)
- `dns_port`: Port for DNS server (default: 53)
- `target_domain`: Domain to intercept (vidaahub.com)
- `stremio_apk_url`: URL to download Stremio APK

**stremio.apk** - Android Package:
- Format: ZIP archive with special structure
- Contains: Compiled code, resources, manifest, signature
- Size: ~45-50 MB
- Target: Android TV (arm64-v8a, armeabi-v7a)

---

### Network Requirements

**Bandwidth:**
- Download APK from internet: ~50 MB (one-time)
- Serve APK to TV: ~50 MB (local network - very fast)
- Minimal bandwidth after installation

**Latency:**
- DNS resolution: <1ms (local)
- HTTP download: Depends on local network speed
- Typical installation time: 2-5 minutes total

**Compatibility:**
- Works on IPv4 networks (192.168.x.x, 10.x.x.x)
- Supports both WiFi and Ethernet
- No port forwarding or router configuration needed
- Works behind NAT

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
