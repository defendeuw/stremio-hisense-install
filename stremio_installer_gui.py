#!/usr/bin/env python3
"""
Stremio Hisense Installer - Windows GUI Application
Simple one-click installer for Stremio on Hisense TVs
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
import sys
import os
import subprocess
import json

# Try importing required modules
try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

class StremioInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stremio Hisense TV Installer")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Variables
        self.local_ip = tk.StringVar()
        self.server_running = False
        self.server_process = None

        # Detect IP automatically
        self.detect_ip()

        # Create UI
        self.create_ui()

    def detect_ip(self):
        """Auto-detect local IP address"""
        try:
            # Connect to external address to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            self.local_ip.set(ip)
        except:
            self.local_ip.set("192.168.1.100")

    def create_ui(self):
        """Create the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Stremio Hisense TV Installer",
            font=("Arial", 20, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=20)

        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # IP Address section
        ip_frame = tk.LabelFrame(main_frame, text="Step 1: Computer IP Address", font=("Arial", 10, "bold"), padx=10, pady=10)
        ip_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(ip_frame, text="Your computer's IP:", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
        ip_entry = tk.Entry(ip_frame, textvariable=self.local_ip, font=("Arial", 11), width=20)
        ip_entry.grid(row=0, column=1, padx=10)

        tk.Button(
            ip_frame,
            text="Detect IP",
            command=self.detect_ip,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9)
        ).grid(row=0, column=2)

        info_label = tk.Label(
            ip_frame,
            text="This IP will be used by your TV to connect to this computer.",
            font=("Arial", 8),
            fg="gray"
        )
        info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # Download APK section
        download_frame = tk.LabelFrame(main_frame, text="Step 2: Download Stremio APK", font=("Arial", 10, "bold"), padx=10, pady=10)
        download_frame.pack(fill=tk.X, pady=(0, 10))

        self.download_status = tk.Label(download_frame, text="Not downloaded", font=("Arial", 9), fg="orange")
        self.download_status.pack(anchor=tk.W)

        tk.Button(
            download_frame,
            text="Download Stremio APK",
            command=self.download_apk,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25
        ).pack(pady=5)

        self.download_progress = ttk.Progressbar(download_frame, mode='indeterminate')
        self.download_progress.pack(fill=tk.X, pady=5)

        # Server control section
        server_frame = tk.LabelFrame(main_frame, text="Step 3: Start Server", font=("Arial", 10, "bold"), padx=10, pady=10)
        server_frame.pack(fill=tk.X, pady=(0, 10))

        self.server_status = tk.Label(server_frame, text="Server stopped", font=("Arial", 9), fg="red")
        self.server_status.pack(anchor=tk.W)

        self.server_button = tk.Button(
            server_frame,
            text="Start Server",
            command=self.toggle_server,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=25
        )
        self.server_button.pack(pady=5)

        # Instructions section
        instructions_frame = tk.LabelFrame(main_frame, text="Step 4: On Your TV", font=("Arial", 10, "bold"), padx=10, pady=10)
        instructions_frame.pack(fill=tk.BOTH, expand=True)

        instructions_text = scrolledtext.ScrolledText(
            instructions_frame,
            wrap=tk.WORD,
            font=("Arial", 9),
            height=10,
            state=tk.NORMAL
        )
        instructions_text.pack(fill=tk.BOTH, expand=True)

        instructions = f"""1. On your TV, go to Settings → Network → Network Configuration

2. Change DNS to Manual/Static

3. Set Primary DNS to: {self.local_ip.get()}
   (Your computer's IP address shown above)

4. Save settings

5. Open your TV's web browser

6. Go to: https://vidaahub.com/

7. Bypass SSL warning (click Advanced → Proceed)

8. Click "Install Stremio" button

9. After installation, restore DNS to Automatic

10. Restart TV and enjoy Stremio!

ALTERNATIVE: USB Installation (Easier!)
- After downloading APK above, copy 'stremio.apk' to USB drive
- Plug USB into TV and install from File Manager
- No DNS changes needed!
"""
        instructions_text.insert(tk.END, instructions)
        instructions_text.config(state=tk.DISABLED)

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 8)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def download_apk(self):
        """Download Stremio APK"""
        if os.path.exists('stremio.apk'):
            response = messagebox.askyesno(
                "APK Exists",
                "Stremio APK already exists. Download again?"
            )
            if not response:
                return

        self.download_progress.start()
        self.download_status.config(text="Downloading...", fg="orange")
        self.status_bar.config(text="Downloading Stremio APK...")

        # Run download in separate thread
        thread = threading.Thread(target=self._download_apk_thread)
        thread.daemon = True
        thread.start()

    def _download_apk_thread(self):
        """Download APK in background thread"""
        try:
            # Check if update_apk.py exists
            if os.path.exists('update_apk.py'):
                # Use the update script
                result = subprocess.run(
                    [sys.executable, 'update_apk.py'],
                    capture_output=True,
                    text=True,
                    input='y\n'  # Auto-confirm download
                )

                if result.returncode == 0 and os.path.exists('stremio.apk'):
                    self.root.after(0, self._download_success)
                else:
                    self.root.after(0, self._download_failed, "Update script failed")
            else:
                # Fallback: direct download
                url = "https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk"
                urllib.request.urlretrieve(url, 'stremio.apk')
                self.root.after(0, self._download_success)

        except Exception as e:
            self.root.after(0, self._download_failed, str(e))

    def _download_success(self):
        """Handle successful download"""
        self.download_progress.stop()
        self.download_status.config(text="✓ Downloaded successfully", fg="green")
        self.status_bar.config(text="APK ready. You can now start the server or copy to USB.")
        messagebox.showinfo(
            "Success",
            "Stremio APK downloaded successfully!\n\n"
            "You can now:\n"
            "1. Start the server and use DNS method, OR\n"
            "2. Copy 'stremio.apk' to USB and install directly on TV"
        )

    def _download_failed(self, error):
        """Handle download failure"""
        self.download_progress.stop()
        self.download_status.config(text="✗ Download failed", fg="red")
        self.status_bar.config(text="Download failed. Try again or download manually.")
        messagebox.showerror(
            "Download Failed",
            f"Failed to download APK:\n{error}\n\n"
            "Try downloading manually from:\n"
            "https://www.stremio.com/downloads"
        )

    def toggle_server(self):
        """Start or stop the server"""
        if not self.server_running:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        """Start the DNS/HTTP server"""
        # Check if APK exists
        if not os.path.exists('stremio.apk'):
            messagebox.showwarning(
                "APK Not Found",
                "Please download the Stremio APK first!"
            )
            return

        # Update config.json
        try:
            config = {
                "local_ip": self.local_ip.get(),
                "http_port": 80,
                "dns_port": 53,
                "target_domain": "vidaahub.com",
                "stremio_apk_url": "https://dl.strem.io/android/v1.6.11/StremioTV-1.6.11.apk"
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update config: {e}")
            return

        # Check if server.py exists
        if not os.path.exists('server.py'):
            messagebox.showerror(
                "Server Not Found",
                "server.py not found! Make sure all files are present."
            )
            return

        # Start server
        try:
            # Check for admin rights on Windows
            if sys.platform == 'win32':
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if not is_admin:
                    messagebox.showwarning(
                        "Administrator Rights Required",
                        "This program needs to run as Administrator!\n\n"
                        "Please:\n"
                        "1. Close this program\n"
                        "2. Right-click on the program\n"
                        "3. Select 'Run as Administrator'"
                    )
                    return

            self.server_process = subprocess.Popen(
                [sys.executable, 'server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            self.server_running = True
            self.server_status.config(text="✓ Server running", fg="green")
            self.server_button.config(text="Stop Server", bg="#f44336")
            self.status_bar.config(text=f"Server running. Set TV DNS to: {self.local_ip.get()}")

            messagebox.showinfo(
                "Server Started",
                f"Server is now running!\n\n"
                f"On your TV:\n"
                f"1. Set DNS to: {self.local_ip.get()}\n"
                f"2. Open browser and go to: https://vidaahub.com/\n"
                f"3. Install Stremio\n\n"
                f"Keep this window open while installing!"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server:\n{e}")

    def stop_server(self):
        """Stop the DNS/HTTP server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None

        self.server_running = False
        self.server_status.config(text="Server stopped", fg="red")
        self.server_button.config(text="Start Server", bg="#4CAF50")
        self.status_bar.config(text="Server stopped")

    def on_closing(self):
        """Handle window closing"""
        if self.server_running:
            response = messagebox.askyesno(
                "Server Running",
                "Server is still running. Stop server and exit?"
            )
            if response:
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = StremioInstallerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
