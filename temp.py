import os

def get_cpu_temp():
    # Read the CPU temperature from the system file
    temp = os.popen("vcgencmd measure_temp").readline()
    # Extract and clean up the temperature value
    temp = temp.replace("temp=", "").replace("'C\n", "")
    return float(temp)

# Display the CPU temperature
cpu_temp = get_cpu_temp()
print(f"CPU Temperature: {cpu_temp}°C")
