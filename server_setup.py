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

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

server = None  # Global server object to allow stopping it directly

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

def start_ftp_server_gui(username, password, directory, port, stop_event, status_label, input_frame, stop_button):
    global server
    try:
        # Check for restricted ports
        if port < 1024:
            raise PermissionError("Ports below 1024 require administrative privileges. Please use a port above 1024.")

        # Check if directory exists
        if not os.path.exists(directory):
            raise FileNotFoundError("The selected directory no longer exists or is inaccessible.")

        # Get and test local IP
        local_ip = get_local_ip()
        if not test_local_ip(local_ip):
            local_ip = "127.0.0.1"
            logging.warning("Switching to localhost because the detected IP is unreachable.")

        # Check if port is already in use
        if is_port_in_use(port):
            raise OSError(f"Port {port} is already in use.")

        # Allow socket reuse to prevent conflicts
        handler = FTPHandler
        authorizer = DummyAuthorizer()
        authorizer.add_user(username, password, directory, perm="elradfmw")
        handler.authorizer = authorizer
        handler.passive_ports = range(60000, 60100)

        address = (local_ip, port)
        server = servers.FTPServer(address, handler)
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Hide input frame and update status
        input_frame.pack_forget()
        status_label.config(text=f"Server Running at ftp://{local_ip}:{port}\nUsername: {username}\nPassword: {password}", fg="green")
        stop_button.pack(pady=10)
        logging.info("FTP Server started.")

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
        server = None
        stop_button.pack_forget()
        input_frame.pack(pady=10)
        status_label.config(text="Server Stopped", fg="red")
        logging.info("FTP Server stopped.")

def main():
    stop_event = threading.Event()
    server_thread = None

    def start_server():
        nonlocal server_thread
        username = username_entry.get() or "user"
        password = password_entry.get() or "pass"
        port = port_entry.get() or "2121"
        try:
            port = int(port)
            directory = filedialog.askdirectory(title="Select Directory to Share")
            if not directory:
                messagebox.showerror("Error", "No directory selected.")
                return

            stop_event.clear()
            server_thread = threading.Thread(target=start_ftp_server_gui, args=(
                username, password, directory, port, stop_event, status_label, input_frame, stop_button), daemon=True)
            server_thread.start()
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")

    def stop_server():
        global server
        if server:
            logging.info("Stopping FTP Server...")
            server.close_all()  # Stop the server immediately
            logging.info("FTP Server stopped.")
        root.destroy()  # Close the tkinter window
        os._exit(0)  # Exit the application completely and terminate the terminal

    # GUI Setup
    root = tk.Tk()
    root.title("FTP Server Setup")
    root.geometry("400x400")

    # Input Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="FTP Server Configuration", font=("Sans-Serif", 13)).pack(pady=10)

    tk.Label(input_frame, text="Username:", font=("Sans-Serif", 13)).pack()
    username_entry = tk.Entry(input_frame, font=("Sans-Serif", 13))
    username_entry.insert(0, "user")
    username_entry.pack()

    tk.Label(input_frame, text="Password:", font=("Sans-Serif", 13)).pack()
    password_entry = tk.Entry(input_frame, show="*", font=("Sans-Serif", 13))
    password_entry.insert(0, "pass")
    password_entry.pack()

    tk.Label(input_frame, text="Port:", font=("Sans-Serif", 13)).pack()
    port_entry = tk.Entry(input_frame, font=("Sans-Serif", 13))
    port_entry.insert(0, "2121")
    port_entry.pack()

    start_button = tk.Button(input_frame, text="Select Directory & Start Server", font=("Sans-Serif", 13), command=start_server)
    start_button.pack(pady=10)

    # Stop Button (hidden initially)
    stop_button = tk.Button(root, text="Stop Server", font=("Sans-Serif", 13), command=stop_server)

    # Status Label
    status_label = tk.Label(root, text="Server Not Running", font=("Sans-Serif", 13), fg="blue")
    status_label.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: [stop_server()])
    root.mainloop()

if __name__ == "__main__":
    main()
