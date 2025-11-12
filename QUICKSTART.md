# Quick Start Guide

## First Time Installation

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Edit config.json with your IP address
# Replace 192.168.1.100 with your computer's actual IP

# 3. Download Stremio APK
python3 update_apk.py

# 4. Start the server (requires sudo/admin)
sudo python3 server.py

# 5. On your TV:
#    - Change DNS to your computer's IP
#    - Open https://vidaahub.com/
#    - Click "Install Stremio"
#    - Restore DNS settings
#    - Restart TV
```

## Update Stremio (When it gets old)

```bash
# 1. Download latest APK
python3 update_apk.py

# 2. Start server
sudo python3 server.py

# 3. On your TV:
#    - Change DNS to your computer's IP
#    - Open https://vidaahub.com/
#    - Click "Install Stremio"
#    - Restore DNS settings
#    - Restart TV
```

## Find Your IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

**macOS/Linux:**
```bash
ifconfig | grep inet
# or
ip addr show
# or
hostname -I
```

## Common Issues

**"Permission denied" when starting server:**
- Use `sudo` on Linux/macOS
- Run Command Prompt as Administrator on Windows

**TV can't connect:**
- Make sure computer and TV are on the same network
- Verify DNS is set to your computer's IP
- Check that server is running (terminal shows "Server started")

**APK not found:**
- Run `python3 update_apk.py` first

For detailed instructions, see [README.md](README.md)
