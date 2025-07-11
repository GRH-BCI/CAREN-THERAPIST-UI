import asyncio
import websockets

WS_URL = "ws://localhost:8765"

async def main():
    print("Connecting to WebSocket server...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("Connected. Waiting for data...\n")
            while True:
                message = await websocket.recv()
                print(message)
    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    asyncio.run(main())