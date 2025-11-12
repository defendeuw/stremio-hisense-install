#!/usr/bin/env python3
"""
Stremio APK Updater
Downloads the latest Stremio APK for sideloading
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

CONFIG_FILE = 'config.json'
APK_FILE = 'stremio.apk'

# Color codes for terminal output
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


def load_config():
    """Load configuration"""
    if not os.path.exists(CONFIG_FILE):
        print_colored(f"Error: {CONFIG_FILE} not found!", Colors.FAIL)
        sys.exit(1)

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def get_file_size(filepath):
    """Get human-readable file size"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def download_progress_hook(block_num, block_size, total_size):
    """Show download progress"""
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(downloaded * 100.0 / total_size, 100)
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r  [{bar}] {percent:.1f}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)", end='', flush=True)


def download_apk(url, output_file):
    """Download APK file with progress bar"""
    try:
        print_colored(f"\nDownloading from: {url}", Colors.OKCYAN)
        print_colored("This may take a few minutes depending on your connection...\n", Colors.WARNING)

        # Download with progress
        urllib.request.urlretrieve(url, output_file, reporthook=download_progress_hook)
        print()  # New line after progress bar

        return True

    except urllib.error.HTTPError as e:
        print_colored(f"\n\nHTTP Error: {e.code} - {e.reason}", Colors.FAIL)
        return False
    except urllib.error.URLError as e:
        print_colored(f"\n\nURL Error: {e.reason}", Colors.FAIL)
        return False
    except Exception as e:
        print_colored(f"\n\nError: {e}", Colors.FAIL)
        return False


def backup_old_apk():
    """Backup existing APK file"""
    if os.path.exists(APK_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"stremio_backup_{timestamp}.apk"
        os.rename(APK_FILE, backup_name)
        print_colored(f"  ✓ Old APK backed up as: {backup_name}", Colors.OKGREEN)
        return backup_name
    return None


def main():
    """Main function"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("Stremio APK Updater", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()

    # Load config
    print_colored("[1/4] Loading configuration...", Colors.OKBLUE)
    config = load_config()
    apk_url = config.get('stremio_apk_url')

    if not apk_url:
        print_colored("  Error: 'stremio_apk_url' not found in config.json", Colors.FAIL)
        sys.exit(1)

    print_colored(f"  ✓ APK URL: {apk_url}", Colors.OKGREEN)
    print()

    # Check existing APK
    print_colored("[2/4] Checking existing APK...", Colors.OKBLUE)
    if os.path.exists(APK_FILE):
        size = get_file_size(APK_FILE)
        mod_time = datetime.fromtimestamp(os.path.getmtime(APK_FILE)).strftime("%Y-%m-%d %H:%M:%S")
        print_colored(f"  Found existing APK: {size} (modified: {mod_time})", Colors.WARNING)

        # Ask user if they want to redownload
        response = input(f"\n  Download new version? (y/n): ").strip().lower()
        if response != 'y':
            print_colored("\n  Update cancelled.", Colors.WARNING)
            sys.exit(0)

        # Backup old APK
        print()
        print_colored("  Backing up old APK...", Colors.OKBLUE)
        backup_old_apk()
    else:
        print_colored("  No existing APK found.", Colors.WARNING)

    print()

    # Download APK
    print_colored("[3/4] Downloading Stremio APK...", Colors.OKBLUE)
    success = download_apk(apk_url, APK_FILE)

    if not success:
        print_colored("\nDownload failed!", Colors.FAIL)
        sys.exit(1)

    print()

    # Verify download
    print_colored("[4/4] Verifying download...", Colors.OKBLUE)
    if os.path.exists(APK_FILE):
        size = get_file_size(APK_FILE)
        print_colored(f"  ✓ APK downloaded successfully: {size}", Colors.OKGREEN)
    else:
        print_colored("  Error: APK file not found after download!", Colors.FAIL)
        sys.exit(1)

    print()
    print_colored("=" * 60, Colors.OKGREEN)
    print_colored("✓ Update Complete!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.OKGREEN)
    print()
    print_colored("Next steps:", Colors.HEADER)
    print_colored("  1. Start the server: sudo python3 server.py", Colors.OKCYAN)
    print_colored("  2. Change your TV's DNS to your computer's IP", Colors.OKCYAN)
    print_colored("  3. Open https://vidaahub.com/ on your TV", Colors.OKCYAN)
    print_colored("  4. Click 'Install Stremio' to update the app", Colors.OKCYAN)
    print_colored("  5. Restore DNS settings and restart your TV", Colors.OKCYAN)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\nUpdate cancelled by user.", Colors.WARNING)
        sys.exit(0)
