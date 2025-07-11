# import socket

# UDP_IP = "0.0.0.0"  # Listen on all interfaces
# UDP_PORT = 12345    # Change to match the port used by your Lua script

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))

# print(f"Listening for UDP data on port {UDP_PORT}...")

# display = False  # Control flag

# try:
#     while True:
#         data, addr = sock.recvfrom(4096)  # Buffer size is 4096 bytes
#         message = data.decode(errors='replace').strip()
#         if message == "START":
#             display = True
#             print("==> START received: displaying data")
#         elif message == "END":
#             display = False
#             print("==> END received: pausing display")
#         elif message == "STOP":
#             print("==> STOP received: exiting program")
#             break
#         elif display:
#             print(f"Received from {addr}: {message}")
# except KeyboardInterrupt:
#     print("\nStopped by user.")
# finally:
#     sock.close()

# import asyncio
# import websockets
# import socket

# UDP_IP = "0.0.0.0"
# UDP_PORT = 12345

# clients = set()

# async def udp_listener():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind((UDP_IP, UDP_PORT))
#     print(f"Listening for UDP data on port {UDP_PORT}...")
#     display = False
#     while True:
#         data, addr = sock.recvfrom(4096)
#         message = data.decode(errors='replace').strip()
#         if message == "START":
#             display = True
#             print("==> START received: displaying data")
#         elif message == "END":
#             display = False
#             print("==> END received: pausing display")

#         elif display:
#             print(f"Received from {addr}: {message}")
#             # Send to all connected WebSocket clients
#             for ws in clients:
#                 await ws.send(message)
#     sock.close()

# async def ws_handler(websocket):
#     clients.add(websocket)
#     try:
#         await websocket.wait_closed()
#     finally:
#         clients.remove(websocket)

# async def main():
#     ws_server = await websockets.serve(ws_handler, "localhost", 8765)
#     print("WebSocket server started on ws://localhost:8765")
#     await udp_listener()

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import websockets
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 12345
clients = set()


async def udp_listener():
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(False)
    print(f"Listening for UDP on port {UDP_PORT}...")

    while True:
        try:
            data, addr = await loop.sock_recvfrom(sock, 4096)
            message = data.decode(errors="replace").strip()
            print(f"UDP: {message}")
            for ws in clients.copy():
                try:
                    await ws.send(message)
                except:
                    clients.remove(ws)
        except Exception as e:
            print(f"[UDP Error] {e}")


async def ws_handler(websocket):
    print("WebSocket client connected.")
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("WebSocket client disconnected.")
        clients.remove(websocket)

async def main():
    print("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(ws_handler, "localhost", 8765):
        await udp_listener()

if __name__ == "__main__":
    asyncio.run(main())
