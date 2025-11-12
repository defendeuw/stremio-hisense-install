#!/usr/bin/env python3
"""
Network Scanner - Find devices on local network
Useful for discovering Hisense TV IP address
"""

import socket
import ipaddress
import subprocess
import platform
import concurrent.futures
import sys

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Create a socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

def get_network_range(ip_address):
    """Get the network range from an IP address"""
    try:
        # Assume /24 subnet (255.255.255.0)
        network = ipaddress.IPv4Network(f"{ip_address}/24", strict=False)
        return network
    except Exception as e:
        print(f"Error calculating network range: {e}")
        return None

def ping_host(ip):
    """Ping a single host to check if it's alive"""
    try:
        # Platform-specific ping command
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", "-w", "500", str(ip)]

        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )

        return result.returncode == 0
    except:
        return False

def get_hostname(ip):
    """Try to get hostname for an IP"""
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
        return hostname
    except:
        return None

def check_port(ip, port):
    """Check if a port is open on a host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except:
        return False

def scan_host(ip):
    """Scan a single host"""
    if ping_host(ip):
        hostname = get_hostname(ip)

        # Check common TV ports
        ports_info = []
        common_ports = [80, 8080, 443, 6466, 36866]  # HTTP, HTTPS, ADB, common TV ports

        for port in common_ports:
            if check_port(ip, port):
                ports_info.append(port)

        # Try to identify if it's a TV
        is_likely_tv = False
        device_type = "Unknown"

        if hostname:
            hostname_lower = hostname.lower()
            if any(brand in hostname_lower for brand in ['hisense', 'tv', 'vidaa', 'smart']):
                is_likely_tv = True
                device_type = "Likely TV/Smart Device"

        if 6466 in ports_info or 36866 in ports_info:
            is_likely_tv = True
            device_type = "Android Device (ADB)"

        return {
            'ip': str(ip),
            'hostname': hostname,
            'ports': ports_info,
            'is_likely_tv': is_likely_tv,
            'device_type': device_type
        }

    return None

def scan_network(network, max_workers=50):
    """Scan all hosts in the network"""
    print(f"\nScanning network: {network}")
    print(f"This may take a minute or two...\n")

    hosts = list(network.hosts())
    discovered_devices = []

    # Use thread pool for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scanning tasks
        future_to_ip = {executor.submit(scan_host, ip): ip for ip in hosts}

        # Process results as they complete
        completed = 0
        for future in concurrent.futures.as_completed(future_to_ip):
            completed += 1
            if completed % 10 == 0:
                print(f"Progress: {completed}/{len(hosts)} hosts scanned...", end='\r')

            result = future.result()
            if result:
                discovered_devices.append(result)

    print(f"\nScan complete! Found {len(discovered_devices)} active device(s)\n")
    return discovered_devices

def main():
    print("=" * 60)
    print("Network Scanner - Find Your Hisense TV")
    print("=" * 60)

    # Get local IP
    local_ip = get_local_ip()
    if not local_ip:
        print("Error: Could not determine local IP address")
        sys.exit(1)

    print(f"\nYour computer's IP: {local_ip}")

    # Get network range
    network = get_network_range(local_ip)
    if not network:
        print("Error: Could not determine network range")
        sys.exit(1)

    print(f"Network range: {network}")

    # Scan network
    devices = scan_network(network)

    # Display results
    if not devices:
        print("\nNo devices found on the network!")
        print("Make sure your TV is turned on and connected to the same network.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Discovered Devices:")
    print("=" * 60)

    tvs_found = []

    for idx, device in enumerate(devices, 1):
        print(f"\n[{idx}] IP Address: {device['ip']}")
        if device['hostname']:
            print(f"    Hostname: {device['hostname']}")
        if device['ports']:
            print(f"    Open Ports: {', '.join(map(str, device['ports']))}")
        print(f"    Type: {device['device_type']}")

        if device['is_likely_tv']:
            tvs_found.append(device)
            print("    ⭐ POSSIBLE TV/SMART DEVICE ⭐")

    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Total devices found: {len(devices)}")
    print(f"Possible TVs/Smart Devices: {len(tvs_found)}")

    if tvs_found:
        print("\n🎯 Recommended IP(s) for your Hisense TV:")
        for tv in tvs_found:
            print(f"   • {tv['ip']} ({tv['hostname'] or 'No hostname'})")

        # Update config.json with most likely TV
        try:
            import json
            config_file = 'config.json'

            print(f"\n📝 Updating config.json with your computer's IP...")

            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}

            config['local_ip'] = local_ip
            config['http_port'] = 80
            config['dns_port'] = 53
            config['target_domain'] = 'vidaahub.com'

            if 'stremio_apk_url' not in config:
                config['stremio_apk_url'] = 'https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk'

            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"✓ Updated config.json with your IP: {local_ip}")

        except Exception as e:
            print(f"⚠️  Could not update config.json: {e}")
    else:
        print("\n[!] No obvious TV devices detected.")
        print("Your TV might still be on the network. Check the list above.")

    print("\n💡 Next steps:")
    print("1. Note your TV's IP address from the list above")
    print("2. Your computer's IP has been configured in config.json")
    print("3. Run the server: python server.py")
    print("4. On your TV, change DNS to point to your computer")
    print("\n")

if __name__ == "__main__":
    import os
    main()
