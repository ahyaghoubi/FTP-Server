# FTP Server with Command-Line Arguments

## Description

This Python-based FTP server allows users to easily set up a local FTP server with customizable settings via command-line arguments. The server can be configured with a specific username, password, directory to serve, and port number. The `pyftpdlib` library is used to handle the FTP functionality, making it easy to create and manage FTP servers in Python.

By running the script with different parameters, you can specify:
- **FTP Username**: The username required to log in to the server.
- **FTP Password**: The password for authenticating users.
- **Directory**: The folder on your machine that will be shared via FTP.
- **Port**: The port on which the FTP server will listen.

This FTP server is designed for local network use or testing purposes and can be easily customized to fit specific needs.

## Features

- **Simple Setup**: Easily start an FTP server with just a few commands.
- **Customizable**: Provide custom FTP usernames, passwords, directories, and ports via command-line arguments.
- **Default Values**: Defaults for username (`user`), password (`pass`), directory (current working directory), and port (2121) for quick setup.
- **Permissions**: Full read-write permissions are granted to the specified user for the shared directory.
- **Passive Mode**: Configurable passive mode ports for compatibility with NAT/firewalls.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux, provided the appropriate permissions are set.

## Requirements

- **Python 3.x**: This script is compatible with Python 3.
- **pyftpdlib**: A lightweight FTP server library for Python. You can install it via `pip`:
  ```bash
  pip install pyftpdlib
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ahyaghoubi/FTP-Server.git
   cd FTP-Server
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
- **`--port`**: Specify the port for the FTP server to listen on. (Default: 2121)

### Examples

1. **Run the server with default settings** (username: `user`, password: `pass`, directory: current directory, port: 2121):
   ```bash
   python ftp_server.py
   ```

2. **Run the server with custom username, password, and directory**:
   ```bash
   python ftp_server.py -u "myuser" -p "mypassword" -d "/path/to/folder"
   ```

3. **Run the server with a custom port**:
   ```bash
   python ftp_server.py --port 2121
   ```

4. **Run the server with a custom directory but default username and password**:
   ```bash
   python ftp_server.py -d "/home/user/myfolder"
   ```

### Starting the FTP Server

Once the server is running, it will listen on all available network interfaces (`0.0.0.0`) on the specified port. You can connect to the server from another machine on your local network using an FTP client like FileZilla or a command-line FTP client, using the provided username and password.

**Important**: If running on a privileged port (e.g., 21), elevated privileges may be required:

```bash
sudo python ftp_server.py
```

### Default Behavior

- The FTP server will run indefinitely (`serve_forever`), allowing multiple clients to connect and interact with the shared directory.
- FTP permissions are set to allow full read and write access for the authenticated user (`elradfmw` permissions).
- If no username, password, or directory is specified, the defaults (`user`, `pass`, and current working directory) will be used.

## Security Notice

This FTP server runs in plain text and is not secure for use over the internet, as passwords and data are transmitted unencrypted. It is intended for local network use or testing purposes only. For secure file transfers, consider using SFTP or FTPS.

## Troubleshooting

- **Permission Issues**: Ensure that the directory you want to share has the appropriate read/write permissions for the user running the server.
- **Port Availability**: If the server fails to start on the specified port, ensure it is not in use by another application. To change the port, use the `--port` argument.
- **Firewall and NAT**: If clients cannot connect, ensure that the firewall allows the specified port and that passive mode ports are configured and open in NAT/firewall settings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
