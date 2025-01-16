import os
import logging
import socket
import tkinter as tk
from tkinter import filedialog, messagebox
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import threading
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

server = None  # Global FTP server object
http_server = None  # Global HTTP server object
CONFIG_FILE = "server_config.json"  # File to save server configuration

def get_local_ip():
    """Retrieve the local IP address of the machine, even without internet."""
    try:
        # Use a dummy connection to get the local IP if possible
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        # Fallback: Get the first available IP address on the local network interface
        local_ip = "127.0.0.1"
        interfaces = socket.getaddrinfo(socket.gethostname(), None)
        for addr in interfaces:
            ip = addr[4][0]
            if ip.startswith("192.") or ip.startswith("10.") or ip.startswith("172."):
                local_ip = ip
                break
    return local_ip

def test_local_ip(ip):
    """Test if the detected local IP address is reachable."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, 0))  # Bind to the IP and an ephemeral port
        return True
    except Exception as e:
        logging.warning(f"Unable to bind to IP {ip}: {e}")
        return False

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("0.0.0.0", port)) == 0

def start_http_server(directory, port=8000):
    """Start an HTTP server in the specified directory."""
    global http_server
    try:
        os.chdir(directory)  # Change to the selected directory
        http_server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
        logging.info(f"HTTP Server started at http://{get_local_ip()}:{port}")
        http_server.serve_forever()
    except Exception as e:
        logging.error(f"Failed to start HTTP server: {e}")
        messagebox.showerror("HTTP Server Error", f"Failed to start HTTP server: {e}")

def start_ftp_server_gui(username, password, directory, ftp_port, http_port, stop_event, status_label, input_frame, stop_button):
    global server
    try:
        # Check for restricted ports
        if ftp_port < 1024 or http_port < 1024:
            raise PermissionError("Ports below 1024 require administrative privileges. Please use a port above 1024.")

        # Check if directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError("The selected directory no longer exists or is inaccessible.")

        # Get and test local IP
        local_ip = get_local_ip()
        if not test_local_ip(local_ip):
            local_ip = "127.0.0.1"
            logging.warning("Switching to localhost because the detected IP is unreachable.")

        # Check if ports are already in use
        if is_port_in_use(ftp_port):
            raise OSError(f"FTP Port {ftp_port} is already in use.")
        if is_port_in_use(http_port):
            raise OSError(f"HTTP Port {http_port} is already in use.")

        # Allow socket reuse to prevent conflicts
        handler = FTPHandler
        authorizer = DummyAuthorizer()
        authorizer.add_user(username, password, directory, perm="elradfmw")
        handler.authorizer = authorizer
        handler.passive_ports = range(60000, 60100)

        address = (local_ip, ftp_port)
        server = servers.FTPServer(address, handler)
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Start HTTP server in a separate thread
        http_thread = threading.Thread(target=start_http_server, args=(directory, http_port), daemon=True)
        http_thread.start()

        # Hide input frame and update status
        input_frame.pack_forget()
        status_label.config(
            text=f"FTP Server Running at ftp://{local_ip}:{ftp_port}\n"
                 f"HTTP Server Running at http://{local_ip}:{http_port}\n"
                 f"Username: {username}\nPassword: {password}",
            fg="green"
        )
        stop_button.pack(pady=10)
        logging.info("FTP and HTTP Servers started.")

        server.serve_forever()
    except PermissionError as pe:
        logging.error(f"Permission Error: {pe}")
        messagebox.showerror("Permission Denied", f"{pe}")
    except FileNotFoundError as fnf:
        logging.error(f"File Error: {fnf}")
        messagebox.showerror("Directory Error", f"{fnf}")
    except OSError as ose:
        logging.error(f"Port Error: {ose}")
        messagebox.showerror("Port Error", f"{ose}")
    except Exception as e:
        logging.error("Error while running FTP server:", exc_info=True)
        messagebox.showerror("Error", f"Failed to start FTP server: {e}")
    finally:
        if server:
            server.close_all()
        if http_server:
            http_server.shutdown()
        server = None
        http_server = None
        stop_button.pack_forget()
        input_frame.pack(pady=10)
        status_label.config(text="Servers Stopped", fg="red")
        logging.info("FTP and HTTP Servers stopped.")

def save_config(username, password, directory, ftp_port, http_port, auto_start):
    """Save server configuration to a file."""
    config = {
        "username": username,
        "password": password,
        "directory": directory,
        "ftp_port": ftp_port,
        "http_port": http_port,
        "auto_start": auto_start
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    logging.info("Configuration saved.")

def load_config():
    """Load server configuration from a file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def enable_auto_start():
    """Enable auto-start on boot for the server."""
    config = load_config()
    if not config:
        messagebox.showerror("Error", "No configuration found. Please save a configuration first.")
        return

    if platform.system() == "Windows":
        # Create a scheduled task to run the script on boot
        script_path = os.path.abspath(__file__)
        command = f'schtasks /create /tn "FTP_HTTP_Server" /tr "{sys.executable} {script_path} --auto-start" /sc onstart /ru SYSTEM'
        os.system(command)
        logging.info("Auto-start enabled on Windows.")
    elif platform.system() in ["Linux", "Darwin"]:
        # Create a systemd service (Linux) or launchd plist (macOS)
        script_path = os.path.abspath(__file__)
        service_content = f"""
[Unit]
Description=FTP and HTTP Server
After=network.target

[Service]
ExecStart={sys.executable} {script_path} --auto-start
Restart=always
User={os.getlogin()}

[Install]
WantedBy=multi-user.target
        """
        if platform.system() == "Linux":
            service_path = "/etc/systemd/system/ftp_http_server.service"
        else:
            service_path = f"/Library/LaunchDaemons/com.example.ftp_http_server.plist"

        try:
            with open(service_path, "w") as f:
                f.write(service_content)
            os.system("systemctl enable ftp_http_server" if platform.system() == "Linux" else f"launchctl load {service_path}")
            logging.info("Auto-start enabled on Linux/macOS.")
        except PermissionError:
            logging.error("Permission denied. Run the script as administrator/root.")
            messagebox.showerror("Permission Denied", "Please run the script as administrator/root to enable auto-start.")
    else:
        logging.error("Unsupported platform for auto-start.")
        messagebox.showerror("Error", "Auto-start is not supported on this platform.")

def disable_auto_start():
    """Disable auto-start on boot for the server."""
    if platform.system() == "Windows":
        os.system('schtasks /delete /tn "FTP_HTTP_Server" /f')
        logging.info("Auto-start disabled on Windows.")
    elif platform.system() in ["Linux", "Darwin"]:
        if platform.system() == "Linux":
            os.system("systemctl disable ftp_http_server")
        else:
            os.system("launchctl unload /Library/LaunchDaemons/com.example.ftp_http_server.plist")
        logging.info("Auto-start disabled on Linux/macOS.")
    else:
        logging.error("Unsupported platform for auto-start.")
        messagebox.showerror("Error", "Auto-start is not supported on this platform.")

def main():
    stop_event = threading.Event()
    server_thread = None

    def start_server():
        nonlocal server_thread
        username = username_entry.get() or "user"
        password = password_entry.get() or "pass"
        ftp_port = ftp_port_entry.get() or "2121"
        http_port = http_port_entry.get() or "8000"
        try:
            ftp_port = int(ftp_port)
            http_port = int(http_port)
            directory = filedialog.askdirectory(title="Select Directory to Share")
            if not directory:
                messagebox.showerror("Error", "No directory selected.")
                return

            stop_event.clear()
            server_thread = threading.Thread(target=start_ftp_server_gui, args=(
                username, password, directory, ftp_port, http_port, stop_event, status_label, input_frame, stop_button), daemon=True)
            server_thread.start()

            # Save configuration
            save_config(username, password, directory, ftp_port, http_port, auto_start_var.get())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")

    def stop_server():
        global server, http_server
        if server:
            logging.info("Stopping FTP Server...")
            server.close_all()  # Stop the FTP server
        if http_server:
            logging.info("Stopping HTTP Server...")
            http_server.shutdown()  # Stop the HTTP server
        root.destroy()  # Close the tkinter window
        os._exit(0)  # Exit the application completely and terminate the terminal

    # GUI Setup
    root = tk.Tk()
    root.title("FTP and HTTP Server Setup")
    root.geometry("500x550")

    # Input Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="FTP and HTTP Server Configuration", font=("Sans-Serif", 13)).pack(pady=10)

    tk.Label(input_frame, text="Username:", font=("Sans-Serif", 13)).pack()
    username_entry = tk.Entry(input_frame, font=("Sans-Serif", 13))
    username_entry.insert(0, "user")
    username_entry.pack()

    tk.Label(input_frame, text="Password:", font=("Sans-Serif", 13)).pack()
    password_entry = tk.Entry(input_frame, show="*", font=("Sans-Serif", 13))
    password_entry.insert(0, "pass")
    password_entry.pack()

    tk.Label(input_frame, text="FTP Port:", font=("Sans-Serif", 13)).pack()
    ftp_port_entry = tk.Entry(input_frame, font=("Sans-Serif", 13))
    ftp_port_entry.insert(0, "2121")
    ftp_port_entry.pack()

    tk.Label(input_frame, text="HTTP Port:", font=("Sans-Serif", 13)).pack()
    http_port_entry = tk.Entry(input_frame, font=("Sans-Serif", 13))
    http_port_entry.insert(0, "8000")
    http_port_entry.pack()

    auto_start_var = tk.BooleanVar()
    auto_start_check = tk.Checkbutton(input_frame, text="Enable Auto-Start on Boot", variable=auto_start_var, font=("Sans-Serif", 13))
    auto_start_check.pack(pady=10)

    start_button = tk.Button(input_frame, text="Select Directory & Start Servers", font=("Sans-Serif", 13), command=start_server)
    start_button.pack(pady=10)

    # Stop Button (hidden initially)
    stop_button = tk.Button(root, text="Stop Servers", font=("Sans-Serif", 13), command=stop_server)

    # Status Label
    status_label = tk.Label(root, text="Servers Not Running", font=("Sans-Serif", 13), fg="blue")
    status_label.pack(pady=10)

    # Auto-Start Buttons
    auto_start_frame = tk.Frame(root)
    auto_start_frame.pack(pady=10)

    enable_auto_start_button = tk.Button(auto_start_frame, text="Enable Auto-Start", font=("Sans-Serif", 13), command=enable_auto_start)
    enable_auto_start_button.pack(side=tk.LEFT, padx=5)

    disable_auto_start_button = tk.Button(auto_start_frame, text="Disable Auto-Start", font=("Sans-Serif", 13), command=disable_auto_start)
    disable_auto_start_button.pack(side=tk.LEFT, padx=5)

    root.protocol("WM_DELETE_WINDOW", lambda: [stop_server()])
    root.mainloop()

if __name__ == "__main__":
    if "--auto-start" in sys.argv:
        # Auto-start mode: Load configuration and start servers
        config = load_config()
        if config:
            stop_event = threading.Event()
            start_ftp_server_gui(
                config["username"],
                config["password"],
                config["directory"],
                config["ftp_port"],
                config["http_port"],
                stop_event,
                None, None, None
            )
    else:
        main()
