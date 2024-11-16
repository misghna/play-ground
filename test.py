import subprocess
import re

def get_enx_interfaces():
    # Run the 'ip link show' command
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    
    # Check the output and extract interfaces starting with 'enx'
    interfaces = []
    for line in result.stdout.splitlines():
        match = re.search(r'^\d+: (enx[^\s:]+):', line)
        if match:
            interfaces.append(match.group(1))
    
    return interfaces

# Get the interfaces and print them
enx_interfaces = get_enx_interfaces()
print(enx_interfaces)
