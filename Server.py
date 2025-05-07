#!/usr/bin/env python

import asyncio
import websockets
import datetime

# --- Configuration ---
HOST = "127.0.0.1"  # Listen on localhost (127.0.0.1)
# Use '' or '0.0.0.0' to listen on all available interfaces
PORT = 8815    # Port to listen on


PATH = "ROOMS FOLDER PATH/"
connected_clients = set()

def save_file(name, content):
	global PATH
	F = open(PATH + name, "w")
	F.write(content);
	F.close()

def read_file(name):
	global PATH
	R  = ""
	F = open(PATH + name, "r")
	R = F.read()
	F.close()
	return R

def get_room(name):
	return read_file(name)


async def echo_handler(websocket):
    """
    Handles individual client connections.
    Receives messages and echoes them back.
    """
    client_addr = websocket.remote_address
    print(f"Client connected: {client_addr}")
    connected_clients.add(websocket)
    try:
        
        # The 'async for' loop elegantly handles receiving messages
        # until the client disconnects.
        async for message in websocket:
            print(f"Received from {client_addr}: {message}")
            response = f"Echo ({datetime.datetime.now()}): {message}"
            
            arr = message.split("\n")
            type = arr[0]
            name = arr[1]
            content = arr[2]
            
            
            SA = ""
            if (len(content) > 4):
            	try:
            		for i in range(len(arr)-2):
            		  	U = arr[i+2]
            		  	SA = SA + U + "\n"
            	except  e:
            		print("err")
          
        
         #   try:
            	
            	
            #content = arr[2]
          #  c e as Exception:
       #     	'
           #// for i in range(8988):
            #	print("AAAAAJAB")
            if type == "request":
            	print("getting", name)
            	response = get_room(name)
           
            if type == "send":
            	print("recived:", content)
            	save_file(name, SA)
            
            # Send the response back to the client
            await websocket.send(response)
            print(f"Sent to {client_addr}: {response}")
			
            # Example: Broadcast to other clients (optional)
            # others = [client for client in connected_clients if client != websocket]
            # if others:
            #     broadcast_msg = f"Client {client_addr} said: {message}"
            #     await asyncio.wait([client.send(broadcast_msg) for client in others])

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client {client_addr} disconnected normally.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client {client_addr} disconnected with error: {e}")
    except Exception as e:
        print(f"An error occurred with client {client_addr}: {e}")
    finally:
        # Remove client from the set upon disconnection
        connected_clients.remove(websocket)
        print(f"Client connection closed: {client_addr}")

async def main():
    """Starts the WebSocket server."""
    # websockets.serve takes the handler, host, and port
    # It returns a Server object
    async with websockets.serve(echo_handler, HOST, PORT):
        print(f"WebSocket server started on ws://{HOST}:{PORT}")
        # Keep the server running indefinitely
        await asyncio.Future()  # Runs forever until stopped (e.g., Ctrl+C)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
    except Exception as e:
        print(f"Server failed to start or run: {e}")