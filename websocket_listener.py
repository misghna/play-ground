import asyncio
import websockets
import re
from util import write_log
from camera_ptz import turn_camera

uri = "ws://localhost:8080/ws"  # WebSocket server URI


async def connect():
    connection_status=False
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to the WebSocket server")
                if(not connection_status): 
                    write_log("Connected to the WebSocket server")
                    connection_status=True
                # Start tasks for sending and receiving messages
                await asyncio.gather(
                    send_message_periodically(websocket),
                    receive_messages(websocket)
                )
        except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
            print(f"Connection lost: {e}. Reconnecting in 30 seconds...")
            if(connection_status): 
                write_log("WS connection lost with the server")
                connection_status=False
            await asyncio.sleep(30)  # Wait before trying to reconnect

async def send_message_periodically(websocket):
    while True:
        try:
            await websocket.send("667")
            print("Sent message to server: 667")
            await asyncio.sleep(30)  # Wait 30 seconds before sending the next message
        except websockets.ConnectionClosed:
            print("Connection closed, stopping send loop.")
            break

async def receive_messages(websocket):
    while True:
        try:
            message = await websocket.recv()
            print("Message from server:", message)
            process_message(message)  # Call the processing function
        except websockets.ConnectionClosed:
            print("Connection closed, stopping receive loop.")
            break

def process_message(message):
    """
    Parse and Process the received message from the WebSocket server.
    """
    pattern = r"^(tilt|zoom|pan)\d+$"
    if bool(re.match(pattern, message)):
        turn_camera(message)


def run_ws():
    # Run the main connect function to keep the connection alive and retry on failure
    asyncio.run(connect())

