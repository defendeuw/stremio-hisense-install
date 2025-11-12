#!/usr/bin/env python3
"""
Stremio APK Updater with Multiple Mirrors and Failsafe
Downloads the latest Stremio APK for sideloading with automatic fallback
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
from datetime import datetime

CONFIG_FILE = 'config.json'
APK_FILE = 'stremio.apk'

# Multiple mirror URLs for Stremio APK (automatic failover)
# These are checked in order if one fails
STREMIO_MIRRORS = [
    {
        "name": "Official Stremio CDN (Primary)",
        "url": "https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk",
        "priority": 1
    },
    {
        "name": "Official Stremio CDN (Alt)",
        "url": "https://dl.strem.io/android/latest/stremio.apk",
        "priority": 2
    },
    {
        "name": "GitHub Releases (Backup)",
        "url": "https://github.com/Stremio/stremio-shell/releases/latest/download/stremio-android-tv.apk",
        "priority": 3
    }
]

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds, will use exponential backoff

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


def download_apk_with_retry(url, output_file, mirror_name="", retry_count=0):
    """Download APK file with retry logic"""
    try:
        if retry_count > 0:
            print_colored(f"  Retry attempt {retry_count}/{MAX_RETRIES}...", Colors.WARNING)

        print_colored(f"\nDownloading from: {mirror_name}", Colors.OKCYAN)
        print_colored(f"URL: {url}", Colors.OKCYAN)
        print_colored("This may take a few minutes depending on your connection...\n", Colors.WARNING)

        # Download with progress
        urllib.request.urlretrieve(url, output_file, reporthook=download_progress_hook)
        print()  # New line after progress bar

        return True, None

    except urllib.error.HTTPError as e:
        error_msg = f"HTTP Error {e.code}: {e.reason}"
        print_colored(f"\n\n{error_msg}", Colors.FAIL)
        return False, error_msg
    except urllib.error.URLError as e:
        error_msg = f"URL Error: {e.reason}"
        print_colored(f"\n\n{error_msg}", Colors.FAIL)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print_colored(f"\n\n{error_msg}", Colors.FAIL)
        return False, error_msg


def download_with_mirrors(mirrors, output_file):
    """Try downloading from multiple mirrors with retry logic"""
    print_colored(f"Attempting download with {len(mirrors)} available mirrors...", Colors.OKBLUE)
    print()

    all_errors = []

    for mirror_idx, mirror in enumerate(mirrors, 1):
        mirror_name = mirror['name']
        mirror_url = mirror['url']

        print_colored(f"[Mirror {mirror_idx}/{len(mirrors)}] {mirror_name}", Colors.HEADER)
        print_colored("─" * 60, Colors.OKBLUE)

        # Try this mirror with retries
        for attempt in range(MAX_RETRIES):
            success, error = download_apk_with_retry(
                mirror_url,
                output_file,
                mirror_name,
                retry_count=attempt
            )

            if success:
                print_colored(f"\n✓ Successfully downloaded from: {mirror_name}", Colors.OKGREEN)
                return True

            # Record error
            all_errors.append({
                'mirror': mirror_name,
                'attempt': attempt + 1,
                'error': error
            })

            # If not last retry, wait before trying again
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                print_colored(f"  Waiting {wait_time}s before retry...", Colors.WARNING)
                time.sleep(wait_time)
            else:
                print_colored(f"  Failed after {MAX_RETRIES} attempts", Colors.FAIL)

        # Try next mirror if this one failed
        if mirror_idx < len(mirrors):
            print()
            print_colored(f"Switching to next mirror...", Colors.WARNING)
            print()

    # All mirrors failed
    print()
    print_colored("=" * 60, Colors.FAIL)
    print_colored("✗ Download failed from all mirrors", Colors.FAIL)
    print_colored("=" * 60, Colors.FAIL)
    print()
    print_colored("Error summary:", Colors.HEADER)
    for err in all_errors:
        print_colored(f"  [{err['mirror']}] Attempt {err['attempt']}: {err['error']}", Colors.FAIL)

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


def get_mirrors(config):
    """Get mirror list from config or use defaults"""
    mirrors = []

    # Check if config has custom URL
    custom_url = config.get('stremio_apk_url')
    if custom_url:
        mirrors.append({
            'name': 'Custom URL (from config.json)',
            'url': custom_url,
            'priority': 0
        })

    # Add built-in mirrors
    mirrors.extend(STREMIO_MIRRORS)

    # Sort by priority
    mirrors.sort(key=lambda x: x['priority'])

    return mirrors


def main():
    """Main function"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored("Stremio APK Updater with Failsafe", Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)
    print()

    # Load config
    print_colored("[1/5] Loading configuration...", Colors.OKBLUE)
    config = load_config()

    # Get available mirrors
    mirrors = get_mirrors(config)
    print_colored(f"  ✓ Found {len(mirrors)} download mirrors", Colors.OKGREEN)
    for idx, mirror in enumerate(mirrors, 1):
        print_colored(f"    {idx}. {mirror['name']}", Colors.OKCYAN)

    print()

    # Check existing APK
    print_colored("[2/5] Checking existing APK...", Colors.OKBLUE)
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

    # Download APK with mirror failover
    print_colored("[3/5] Downloading Stremio APK...", Colors.OKBLUE)
    print_colored("Using automatic failover - will try all mirrors if needed", Colors.OKBLUE)
    print()

    success = download_with_mirrors(mirrors, APK_FILE)

    if not success:
        print()
        print_colored("=" * 60, Colors.FAIL)
        print_colored("✗ Download Failed", Colors.FAIL)
        print_colored("=" * 60, Colors.FAIL)
        print()
        print_colored("All mirrors failed. Possible solutions:", Colors.WARNING)
        print_colored("  1. Check your internet connection", Colors.OKCYAN)
        print_colored("  2. Try again later (servers might be down)", Colors.OKCYAN)
        print_colored("  3. Download APK manually from https://www.stremio.com/downloads", Colors.OKCYAN)
        print_colored("     and save it as 'stremio.apk' in this folder", Colors.OKCYAN)
        print_colored("  4. Check if your firewall/antivirus is blocking downloads", Colors.OKCYAN)
        print()
        sys.exit(1)

    print()

    # Verify download
    print_colored("[4/5] Verifying download...", Colors.OKBLUE)
    if os.path.exists(APK_FILE):
        size = get_file_size(APK_FILE)
        file_size_bytes = os.path.getsize(APK_FILE)

        # Check if file is too small (likely corrupted)
        if file_size_bytes < 10 * 1024 * 1024:  # Less than 10 MB
            print_colored(f"  ✗ Warning: Downloaded file seems too small ({size})", Colors.WARNING)
            print_colored("  This might be a corrupted download. Try running update again.", Colors.WARNING)
        else:
            print_colored(f"  ✓ APK downloaded successfully: {size}", Colors.OKGREEN)
            print_colored(f"  ✓ File size looks correct", Colors.OKGREEN)
    else:
        print_colored("  Error: APK file not found after download!", Colors.FAIL)
        sys.exit(1)

    print()

    # Final message
    print_colored("[5/5] Update complete!", Colors.OKBLUE)
    print()
    print_colored("=" * 60, Colors.OKGREEN)
    print_colored("✓ Stremio APK Ready!", Colors.OKGREEN)
    print_colored("=" * 60, Colors.OKGREEN)
    print()
    print_colored("Next steps to install/update on your TV:", Colors.HEADER)
    print_colored("  1. Start the server: sudo python3 server.py", Colors.OKCYAN)
    print_colored("  2. Change your TV's DNS to your computer's IP", Colors.OKCYAN)
    print_colored("  3. Open https://vidaahub.com/ on your TV", Colors.OKCYAN)
    print_colored("  4. Click 'Install Stremio' to install/update", Colors.OKCYAN)
    print_colored("  5. Restore DNS settings and restart your TV", Colors.OKCYAN)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\nUpdate cancelled by user.", Colors.WARNING)
        sys.exit(0)
