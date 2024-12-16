# FTP Server with User Input Setup

## Description

This Python-based FTP server enables users to set up a local FTP server interactively via terminal prompts. Built using the `pyftpdlib` library, it supports customizable configurations for the FTP username, password, shared directory, and port. The server is designed for local network use or testing purposes, offering flexibility and ease of use.

## Features

- **Interactive Setup**: Configure the FTP server by entering the username, password, shared directory, and port when prompted.
- **Default Values**: Defaults provided for username (`user`), password (`pass`), directory (current working directory), and port (`2121`) for quick setup.
- **Comprehensive Permissions**: Full read-write permissions (`elradfmw`) for the authenticated user.
- **Passive Mode**: Configured passive mode ports (`60000-60100`) for NAT/firewall compatibility.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.
- **Logging**: Informative logs for server activities and configuration details.
- **Graceful Shutdown**: Handles `KeyboardInterrupt` (Ctrl+C) for clean termination.

## Requirements

- **Python 3.x**: Ensure Python 3 is installed.
- **pyftpdlib**: Install via `pip`:
  ```bash
  pip install pyftpdlib
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahyaghoubi/FTP-Server.git
   cd FTP-Server
   ```

2. Install dependencies:
   ```bash
   pip install pyftpdlib
   ```

## Usage

1. Run the script:
   ```bash
   python ftp_server.py
   ```

2. Follow the prompts:
   - Enter a username (or press Enter for the default: `user`).
   - Enter a password (or press Enter for the default: `pass`).
   - Specify the directory to share (or press Enter for the default: current working directory).
   - Specify the port (or press Enter for the default: `2121`).

3. Once started, the server listens on all network interfaces (`0.0.0.0`) on the specified port. Use an FTP client like FileZilla or a command-line FTP client to connect using the provided credentials.

### Default Behavior

- Full permissions (`elradfmw`) are granted to the specified user for the shared directory.
- Defaults are used for username, password, directory, and port if no inputs are provided.
- The server runs indefinitely (`serve_forever`) and handles multiple connections.

## Security Notice

This FTP server transmits data, including passwords, in plain text and is intended for local network use only. Avoid using it over the internet unless secured with additional measures like FTPS or SFTP.

## Troubleshooting

- **Invalid Directory**: If the provided directory does not exist, the server will prompt you until a valid directory is entered.
- **Port Conflicts**: Ensure the chosen port is not in use. The server will prompt you to re-enter the port if issues occur.
- **Firewall and NAT**: Open the specified and passive mode ports in your firewall or router for successful connections.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
