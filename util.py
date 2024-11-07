def get_device_id():
    """
    Retrieves the Raspberry Pi's unique serial number.

    Returns:
        str: The serial number as a string, or 'ERROR000000000' if not found.
    """
    serial = "ERROR000000000"
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    serial = line.strip().split(': ')[1]
                    break
    except Exception as e:
        print(f"An error occurred while retrieving the serial number: {e}")
    return serial

# Example usage
# serial_number = get_raspberry_pi_serial()
# print(f"Raspberry Pi Serial Number: {serial_number}")
