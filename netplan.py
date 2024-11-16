import os
import subprocess

def get_first_enx_interface():
    # Run the 'ip link show' command
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    
    # Check the output and extract interfaces starting with 'enx'
    for line in result.stdout.splitlines():
        match = re.search(r'^\d+: (enx[^\s:]+):', line)
        if match:
            return match.group(1)
    
    return "not found"
def write_netplan_config(interface_name, ip_address, subnet_mask, gateway, dns_servers):
    # Construct the Netplan YAML configuration as a string
    netplan_config = f"""
    network:
      version: 2
      ethernets:
        {interface_name}:
          dhcp4: no
          addresses:
            - {ip_address}/{subnet_mask}
          gateway4: {gateway}
          nameservers:
            addresses:
              - {', '.join(dns_servers)}
    """
    # Path to the Netplan configuration file
    netplan_file = "/etc/netplan/usb-netcfg.yaml"

    # Write the configuration to the file
    with open(netplan_file, "w") as file:
        file.write(netplan_config)

    print(f"Netplan configuration written to {netplan_file}")

def apply_netplan():
    try:
        # Apply the Netplan configuration
        subprocess.run(["sudo", "netplan", "apply"], check=True)
        print("Netplan configuration applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying Netplan: {e}")

def verify_netplan():
    # Verify the IP address and network settings
    result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True)
    print(result.stdout)

infname=get_first_enx_interface()
# Example usage
if __name__ == "__main__":
    # Interface and network configuration details
    interface_name = infname  # Replace with your interface name
    ip_address = "192.168.0.90"  # Replace with your desired IP
    subnet_mask = "24"  # Replace with your subnet mask
    gateway = "192.168.0.1"  # Replace with your gateway
    dns_servers = ["8.8.8.8", "8.8.4.4"]  # Replace with your DNS servers

    # Execute the functions
    write_netplan_config(interface_name, ip_address, subnet_mask, gateway, dns_servers)
    apply_netplan()
    verify_netplan()
