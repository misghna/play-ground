import subprocess
import re

def get_first_enx_interface():
    # Run the 'ip link show' command
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    
    # Check the output and extract interfaces starting with 'enx'
    for line in result.stdout.splitlines():
        match = re.search(r'^\d+: (enx[^\s:]+):', line)
        if match:
            return match.group(1)
    
    return "not found"

def configure_nmcli(interface_name, ip_address, subnet_mask, gateway, dns_servers):
    try:
        # Convert IP address and subnet mask into CIDR notation
        cidr_notation = f"{ip_address}/{subnet_mask}"

        # Check if a connection exists for the interface
        result = subprocess.run(["nmcli", "-t", "-f", "NAME,DEVICE", "con", "show"], capture_output=True, text=True, check=True)
        connections = result.stdout.splitlines()

        connection_name = None
        for connection in connections:
            name, device = connection.split(":")
            if device.strip() == interface_name:
                connection_name = name.strip()
                break

        if connection_name:
            # Modify the existing connection
            print(f"Modifying existing connection '{connection_name}' for interface {interface_name}...")
            subprocess.run([
                "nmcli", "con", "mod", connection_name,
                "ipv4.addresses", cidr_notation,
                "ipv4.gateway", gateway,
                "ipv4.dns", ",".join(dns_servers),
                "ipv4.method", "manual"
            ], check=True)
        else:
            # Add a new connection
            connection_name = f"Connection_for_{interface_name}"
            print(f"Adding new connection '{connection_name}' for interface {interface_name}...")
            subprocess.run([
                "nmcli", "con", "add",
                "type", "ethernet",
                "ifname", interface_name,
                "con-name", connection_name,
                "ipv4.addresses", cidr_notation,
                "ipv4.gateway", gateway,
                "ipv4.dns", ",".join(dns_servers),
                "ipv4.method", "manual"
            ], check=True)

        # Bring up the connection
        print(f"Bringing up the connection '{connection_name}' for {interface_name}...")
        subprocess.run(["nmcli", "con", "up", connection_name], check=True)

        print(f"Network configuration applied successfully for {interface_name}.")

    except subprocess.CalledProcessError as e:
        print(f"Error configuring network: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def verify_nmcli():
    # Verify the current network configuration
    result = subprocess.run(["nmcli", "dev", "show"], capture_output=True, text=True, check=True)
    print(result.stdout)

    
first_enx_interface = get_first_enx_interface()
# Example usage

if __name__ == "__main__":
    # Interface and network configuration details
    interface_name = first_enx_interface  # Replace with your interface name
    ip_address = "192.168.0.90"  # Replace with your desired IP
    subnet_mask = "24"  # Replace with your subnet mask
    gateway = "192.168.0.1"  # Replace with your gateway
    dns_servers = ["8.8.8.8", "8.8.4.4"]  # Replace with your DNS servers

    # Configure and verify network settings
    configure_nmcli(interface_name, ip_address, subnet_mask, gateway, dns_servers)
    verify_nmcli()


