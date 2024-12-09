import argparse
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Start an FTP server.")
parser.add_argument("-u", "--username", type=str, default="user", help="FTP username (default: 'user')")
parser.add_argument("-p", "--password", type=str, default="pass", help="FTP password (default: 'pass')")
parser.add_argument("-d", "--directory", type=str, default=os.getcwd(), help="Directory to share (default: current directory)")

# Parse command-line arguments
args = parser.parse_args()

# Create an authorizer object to handle authentication
authorizer = DummyAuthorizer()

# Add user with permission to read and write files
authorizer.add_user(args.username, args.password, args.directory, perm="elradfmw")

# Instantiate FTPHandler with the authorizer for authentication
handler = FTPHandler
handler.authorizer = authorizer

# Define address and port for the server
address = ("0.0.0.0", 21)  # Listen on every IP on your machine on port 21

# Create the FTPServer instance and pass the handler and address
server = servers.FTPServer(address, handler)

# Start the server
print(f"Starting FTP server with user '{args.username}' and password '{args.password}'")
print(f"Serving directory: {args.directory}")
server.serve_forever()
