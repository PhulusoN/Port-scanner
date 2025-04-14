import socket  # Import the socket library for network connections
# Import ThreadPoolExecutor for concurrent execution
from concurrent.futures import ThreadPoolExecutor


def scan_port(ip, port):
    """Scan a single port on the given IP address."""
    try:
        # Create a socket object using IPv4 and TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set a timeout of 1 second for the connection attempt
            sock.settimeout(1)
            # Try to connect to the specified port
            result = sock.connect_ex((ip, port))
            if result == 0:
                return port  # If the result is 0, the port is open
            return None  # If the port is closed, return None
    except socket.error as e:
        print(f"Error creating socket for port {port}: {e}")
        return None


def scan_ports(ip, start_port, end_port, max_workers=100):
    """Scan a range of ports on the given IP address."""
    open_ports = []  # List to store open ports
    # Use ThreadPoolExecutor to scan ports concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a dictionary of futures for each port to be scanned
        futures = {executor.submit(scan_port, ip, port): port for port in range(
            start_port, end_port + 1)}
        # Iterate over the futures to get the results
        for future in futures:
            port = futures[future]  # Get the port associated with the future
            try:
                result = future.result()  # Get the result of the port scan
                if result is not None:
                    # If the port is open, add it to the list
                    open_ports.append(result)
            except Exception as e:
                # Print any errors encountered during scanning
                print(f"Error scanning port {port}: {type(e).__name__} - {e}")
    return open_ports  # Return the list of open ports


if __name__ == "__main__":
    # Prompt the user for the target IP address
    target_ip = input("Enter the IP address to scan: ")
    # Prompt the user for the starting port number
    start_port = int(input("Enter the starting port number: "))
    # Prompt the user for the ending port number
    end_port = int(input("Enter the ending port number: "))

    print(f"Scanning {target_ip} from port {start_port} to {end_port}...")
    # Call the scan_ports function to scan the specified range of ports
    open_ports = scan_ports(target_ip, start_port, end_port)

    # Check if any open ports were found and print the results
    if open_ports:
        # Print the list of open ports
        print(f"Open ports: {', '.join(map(str, open_ports))}")
    else:
        # Inform the user if no open ports were found
        print("No open ports found.")
