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

# Get the first interface and print the result
first_enx_interface = get_first_enx_interface()
print(first_enx_interface)
