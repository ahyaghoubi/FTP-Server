import os
import logging
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Function to get user inputs
def get_user_inputs():
    print("Welcome to the FTP Server Setup!")
    
    username = input("Enter a username (default: 'user'): ").strip() or "user"
    password = input("Enter a password (default: 'pass'): ").strip() or "pass"
    directory = input(f"Enter a directory to share (default: {os.getcwd()}): ").strip() or os.getcwd()
    while not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist or is not accessible.")
        directory = input("Please enter a valid directory: ").strip()
    
    port = input("Enter the FTP port (default: 2121): ").strip() or "2121"
    
    return username, password, directory, int(port)

# FTP Server Setup
def start_ftp_server(username, password, directory, port):
    # Create an authorizer object to handle authentication
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, directory, perm="elradfmw")
    
    # Instantiate FTPHandler with the authorizer for authentication
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 60100)

    # Define address and port for the server
    address = ("0.0.0.0", port)
    server = servers.FTPServer(address, handler)

    logging.info(f"Starting FTP server with user '{username}' on port {port}")
    logging.info(f"Serving directory: {directory}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down the FTP server.")

# Main function
def main():
    username, password, directory, port = get_user_inputs()
    start_ftp_server(username, password, directory, port)

if __name__ == "__main__":
    main()
