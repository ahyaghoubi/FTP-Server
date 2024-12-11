import argparse
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Set up argument parsing
parser = argparse.ArgumentParser(description="Start an FTP server.")
parser.add_argument("-u", "--username", type=str, default="user", help="FTP username (default: 'user')")
parser.add_argument("-p", "--password", type=str, default="pass", help="FTP password (default: 'pass')")
parser.add_argument("-d", "--directory", type=str, default=os.getcwd(), help="Directory to share (default: current directory)")
parser.add_argument("--port", type=int, default=2121, help="Port to run the FTP server on (default: 2121)")

# Parse command-line arguments
args = parser.parse_args()

# Verify directory exists
if not os.path.isdir(args.directory):
    raise ValueError(f"Directory '{args.directory}' does not exist or is not accessible.")

# Create an authorizer object to handle authentication
authorizer = DummyAuthorizer()

# Add user with permission to read and write files
authorizer.add_user(args.username, args.password, args.directory, perm="elradfmw")

# Instantiate FTPHandler with the authorizer for authentication
handler = FTPHandler
handler.authorizer = authorizer

# Configure passive mode to use a specific range of ports (optional)
handler.passive_ports = range(60000, 60100)

# Define address and port for the server
address = ("0.0.0.0", args.port)  # Listen on every IP on the specified port

# Create the FTPServer instance and pass the handler and address
server = servers.FTPServer(address, handler)

# Start the server
logging.info(f"Starting FTP server with user '{args.username}' and password '{args.password}'")
logging.info(f"Serving directory: {args.directory}")
logging.info(f"Server is listening on port {args.port}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    logging.info("Shutting down the FTP server.")
