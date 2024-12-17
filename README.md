# **FTP Server Setup Application**

A simple, cross-platform graphical application to configure and launch an FTP server using Python. This app allows you to securely share directories over FTP with custom credentials.

---

## **Features**

- ✅ **User-Friendly GUI**: Set up an FTP server without using the command line.  
- ✅ **Cross-Platform**: Supports **Windows**, **macOS**, and **Linux**.  
- ✅ **Customizable Credentials**: Set your own username and password for FTP access.  
- ✅ **Directory Selection**: Choose which directory to share over FTP.  
- ✅ **Automatic Local IP Detection**: Detects and validates the local IP address.  
- ✅ **Real-Time Status**: Displays the server's state and connection details.

---

### **How to Use**

1. **Download the Executable**:
   - Windows: [server_setup_windows.exe](https://github.com/ahyaghoubi/FTP-Server/releases)
   - macOS: [server_setup_macos](https://github.com/ahyaghoubi/FTP-Server/releases)
   - Linux: [server_setup_linux](https://github.com/ahyaghoubi/FTP-Server/releases)

2. **Run the Application**:
   - Windows: Double-click `server_setup_windows.exe`.
   - macOS/Linux: Open a terminal and run:
     ```bash
     ./server_setup
     ```

3. **Set Up Your FTP Server**:
   - Enter your **username**, **password**, and **port**.
   - Select the **directory** you want to share.
   - Click **"Start Server"**.

4. **Connect to the FTP Server**:
   - Use an FTP client like **FileZilla** or a browser.
   - Enter the local IP and port displayed in the app.

5. **Stop the Server**:
   - Click the **"Stop Server"** button to stop the FTP server and exit the application.

---

## **Running From Source**

To run the `server_setup.py` script directly on your system, follow these steps:

### **1. Install Python**
Ensure **Python 3.10+** is installed:
   ```bash
   python3 --version
   ```

If Python is not installed, download it from [python.org](https://www.python.org/).

---

### **2. Install Required Dependencies**

The following dependencies are required to run the app:

| Dependency         | Description                            |
|---------------------|----------------------------------------|
| `pyftpdlib`         | FTP server library.                   |
| `tkinter` (built-in)| GUI library for Python.               |
| `os` and `socket`   | Built-in modules for OS and network.  |
| `logging`           | Standard library for logging.         |
| `threading`         | For running the FTP server in threads.|
| `sys`               | For system operations.                |

To install the required libraries, run:

```bash
pip install pyftpdlib
```

### **Note on `tkinter`**:
- **Windows and macOS**: `tkinter` comes pre-installed with Python.
- **Linux**: Install `tkinter` separately using the package manager:
   - For Debian/Ubuntu-based systems:
     ```bash
     sudo apt-get install python3-tk
     ```
   - For RedHat-based systems:
     ```bash
     sudo yum install python3-tkinter
     ```

---

### **3. Run the Application**

Navigate to the project directory and run the script:

```bash
python3 server_setup.py
```

---

## **System Requirements**

| Platform | Requirements                        |
|----------|-------------------------------------|
| Windows  | Windows 10 or later (64-bit)        |
| macOS    | macOS 10.15 (Catalina) or later     |
| Linux    | Ubuntu 18.04 or later               |

---

## **Releases**

| Version   | Description             |
|-----------|-------------------------|
| v1.0.0    | Initial stable release. |

[Download the Latest Release](https://github.com/ahyaghoubi/FTP-Server/releases)

---

## **Known Issues**

- Ports below 1024 require administrative privileges.
- Some FTP clients may require passive ports to be opened in the firewall.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**

Contributions are welcome! Please open an issue to report bugs, suggest features, or contribute improvements.

---

## **Support**

If you encounter any issues, please open a ticket in the [Issues](https://github.com/ahyaghoubi/FTP-Server/issues) section.
