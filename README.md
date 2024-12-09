# FTP Server with Command-Line Arguments

## Description

This Python-based FTP server allows users to easily set up a local FTP server with customizable settings via command-line arguments. The server can be configured with a specific username, password, and directory to serve, all while providing default values for simplicity. The `pyftpdlib` library is used to handle the FTP functionality, making it easy to create and manage FTP servers in Python.

By running the script with different parameters, you can specify:
- **FTP Username**: The username required to log in to the server.
- **FTP Password**: The password for authenticating users.
- **Directory**: The folder on your machine that will be shared via FTP.

This FTP server is designed for local network use or testing purposes and can be easily customized to fit specific needs.

## Features

- **Simple Setup**: Easily start an FTP server with just a few commands.
- **Customizable**: Provide custom FTP usernames, passwords, and directories via command-line arguments.
- **Default Values**: Defaults for username (`user`), password (`pass`), and directory (current working directory) for quick setup.
- **Permissions**: Full read-write permissions are granted to the specified user for the shared directory.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux, provided the appropriate permissions are set for the FTP port (default is 21).

## Requirements

- **Python 3.x**: This script is compatible with Python 3.
- **pyftpdlib**: A lightweight FTP server library for Python. You can install it via `pip`:
  ```bash
  pip install pyftpdlib
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ftp-server.git
   cd ftp-server
   ```

2. Install the required dependencies:
   ```bash
   pip install pyftpdlib
   ```

## Usage

### Command-Line Arguments

- **`-u`, `--username`**: Specify the username for FTP authentication. (Default: `user`)
- **`-p`, `--password`**: Specify the password for FTP authentication. (Default: `pass`)
- **`-d`, `--directory`**: Specify the directory to share via FTP. (Default: Current working directory)

### Examples

1. **Run the server with default settings** (username: `user`, password: `pass`, directory: current directory):
   ```bash
   python ftp_server.py
   ```

2. **Run the server with custom username, password, and directory**:
   ```bash
   python ftp_server.py -u "myuser" -p "mypassword" -d "C://Users/amirhy/Desktop"
   ```

3. **Run the server with a custom username and password, using the current directory**:
   ```bash
   python ftp_server.py -u "myuser" -p "mypassword"
   ```

4. **Run the server with a custom directory but default username and password**:
   ```bash
   python ftp_server.py -d "/home/user/myfolder"
   ```

### Starting the FTP Server

Once the server is running, it will listen on all available network interfaces (0.0.0.0) on port 21. You can connect to the server from another machine on your local network using an FTP client like FileZilla or a command-line FTP client, using the provided username and password.

**Important**: On some systems (especially Linux and macOS), you may need elevated privileges (e.g., using `sudo`) to bind to port 21 since it's a privileged port.

```bash
sudo python ftp_server.py
```

### Default Behavior

- The FTP server will run indefinitely (`serve_forever`), allowing multiple clients to connect and interact with the shared directory.
- FTP permissions are set to allow full read and write access for the authenticated user (`elradfmw` permissions).
- If no username or password is specified, the defaults (`user` and `pass`) will be used.

## Security Notice

This FTP server runs in plain text and is not secure for use over the internet, as passwords and data are transmitted unencrypted. It is intended for local network use or testing purposes only. For secure file transfers, consider using SFTP or FTPS.

## Troubleshooting

- **Permission Issues**: Ensure that the directory you want to share has the appropriate read/write permissions for the user running the server.
- **Port 21 Availability**: If the server fails to start on port 21, you may need to choose a different port (e.g., 2121) or run the script with elevated privileges:
  ```bash
  sudo python ftp_server.py
  ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
