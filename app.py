import threading
from image_processor import run_scheduler
from image_processor import write_log
from websocket_listener import run_ws
import time

# Run the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()


# Start the WebSocket connection in a separate thread
thread = threading.Thread(target=run_ws, daemon=True)
thread.start()


# Main thread can perform other tasks
try:
    while True:
        # Replace this with other operations or simply pass
        print("Program running.")
        time.sleep(10)
        
except KeyboardInterrupt:
    write_log("Error: Program Terminated!")
    print("Program terminated.")
