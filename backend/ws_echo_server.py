import asyncio
import websockets

async def echo(websocket):
    print("Client connected.")
    try:
        while True:
            await websocket.send("Test message")
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

async def main():
    print(" Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
