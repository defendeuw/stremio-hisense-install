#!/usr/bin/env python3
"""
Stremio Hisense (Vidaa) Sideload Helper
DNS and HTTP server for sideloading Stremio on Hisense TVs
"""

import http.server
import socketserver
import json
import os
import sys
import threading
from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
CONFIG_FILE = 'config.json'

def load_config():
    """Load configuration from config.json"""
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"Configuration file {CONFIG_FILE} not found!")
        logger.error("Please create config.json with your local IP address.")
        sys.exit(1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

        if 'local_ip' not in config:
            logger.error("'local_ip' not found in config.json")
            sys.exit(1)

        return config
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing config.json: {e}")
        sys.exit(1)

config = load_config()

LOCAL_IP = config['local_ip']
HTTP_PORT = config.get('http_port', 80)
DNS_PORT = config.get('dns_port', 53)
TARGET_DOMAIN = config.get('target_domain', 'vidaahub.com')

logger.info("="*50)
logger.info("Stremio Hisense Sideload Server")
logger.info("="*50)
logger.info(f"Local IP: {LOCAL_IP}")
logger.info(f"HTTP Port: {HTTP_PORT}")
logger.info(f"DNS Port: {DNS_PORT}")
logger.info(f"Target Domain: {TARGET_DOMAIN}")
logger.info("="*50)


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler to serve the installation page"""

    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info("%s - %s" % (self.address_string(), format % args))

    def do_GET(self):
        """Handle GET requests"""
        logger.info(f"HTTP Request: {self.path} from {self.client_address[0]}")

        # Serve the main page for vidaahub.com
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Read and serve the HTML page
            html_file = 'index.html'
            if os.path.exists(html_file):
                with open(html_file, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>Error: index.html not found</h1>")

        # Serve the Stremio APK file
        elif self.path.startswith('/stremio'):
            apk_file = 'stremio.apk'
            if os.path.exists(apk_file):
                self.send_response(200)
                self.send_header('Content-type', 'application/vnd.android.package-archive')
                self.send_header('Content-Disposition', f'attachment; filename="stremio.apk"')
                file_size = os.path.getsize(apk_file)
                self.send_header('Content-Length', str(file_size))
                self.end_headers()

                with open(apk_file, 'rb') as f:
                    self.wfile.write(f.read())

                logger.info(f"Served Stremio APK ({file_size} bytes)")
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Stremio APK file not found</h1>")
                logger.error("Stremio APK file not found!")

        # Serve the APKPure APK file (optional - for easy updates on TV)
        elif self.path.startswith('/apkpure'):
            apk_file = 'apkpure.apk'
            if os.path.exists(apk_file):
                self.send_response(200)
                self.send_header('Content-type', 'application/vnd.android.package-archive')
                self.send_header('Content-Disposition', f'attachment; filename="apkpure.apk"')
                file_size = os.path.getsize(apk_file)
                self.send_header('Content-Length', str(file_size))
                self.end_headers()

                with open(apk_file, 'rb') as f:
                    self.wfile.write(f.read())

                logger.info(f"Served APKPure APK ({file_size} bytes)")
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>APKPure not available. Download from apkpure.com</h1>")
                logger.info("APKPure APK requested but not found (optional file)")

        else:
            # Default file serving
            super().do_GET()


class CustomDNSResolver(BaseResolver):
    """Custom DNS resolver to redirect vidaahub.com to local IP"""

    def resolve(self, request, handler):
        """Resolve DNS queries"""
        reply = request.reply()
        qname = request.q.qname
        qtype = QTYPE[request.q.qtype]

        domain = str(qname).rstrip('.')

        # Log all DNS queries
        logger.debug(f"DNS Query: {domain} ({qtype}) from {handler.client_address[0]}")

        # Redirect target domain to local IP
        if TARGET_DOMAIN in domain.lower() and qtype == 'A':
            logger.info(f"DNS: Redirecting {domain} -> {LOCAL_IP}")
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(LOCAL_IP), ttl=60))
        else:
            # For other domains, return NXDOMAIN or forward to real DNS
            logger.debug(f"DNS: Not intercepting {domain}")
            pass

        return reply


def start_http_server():
    """Start the HTTP server"""
    try:
        # Change to script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        handler = CustomHTTPRequestHandler
        httpd = socketserver.TCPServer(("", HTTP_PORT), handler)

        logger.info(f"HTTP Server started on port {HTTP_PORT}")
        httpd.serve_forever()
    except PermissionError:
        logger.error(f"Permission denied to bind to port {HTTP_PORT}")
        logger.error("Try running with sudo (Linux/Mac) or as Administrator (Windows)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"HTTP Server error: {e}")
        sys.exit(1)


def start_dns_server():
    """Start the DNS server"""
    try:
        resolver = CustomDNSResolver()
        dns_server = DNSServer(resolver, port=DNS_PORT, address="")

        logger.info(f"DNS Server started on port {DNS_PORT}")
        dns_server.start_thread()

        # Keep the thread alive
        while True:
            threading.Event().wait(1)

    except PermissionError:
        logger.error(f"Permission denied to bind to port {DNS_PORT}")
        logger.error("Try running with sudo (Linux/Mac) or as Administrator (Windows)")
        sys.exit(1)
    except Exception as e:
        logger.error(f"DNS Server error: {e}")
        sys.exit(1)


def check_requirements():
    """Check if all required files exist"""
    errors = []

    if not os.path.exists('index.html'):
        errors.append("index.html not found")

    if not os.path.exists('stremio.apk'):
        errors.append("stremio.apk not found - run update_apk.py to download it")

    if errors:
        logger.error("Missing required files:")
        for error in errors:
            logger.error(f"  - {error}")
        logger.error("\nPlease ensure all required files are present.")
        return False

    return True


def main():
    """Main entry point"""
    logger.info("Starting Stremio Sideload Server...")

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Start DNS server (blocking)
    try:
        start_dns_server()
    except KeyboardInterrupt:
        logger.info("\nShutting down servers...")
        sys.exit(0)


if __name__ == "__main__":
    main()
