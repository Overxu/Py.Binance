import websocket
import json
import os
from heapq import nlargest

# before use put in console #pip install websocket-client

def on_message(ws, message):
    data = json.loads(message)
    if data['e'] == 'depthUpdate':
        bids = nlargest(5, data['b'], key=lambda x: float(x[0]))
        asks = sorted(data['a'], key=lambda x: float(x[0]))[:5][::-1] #to reverse the order
        os.system("cls")
        print("===========================================")
        print("Top 5 Bids:")
        for ask in asks:
            print(f"Price: {ask[0]}, Quantity: {ask[1]}")
        print("===========================================")
        
        print("Top 5 Asks:")
        for bid in bids:
            print(f"Price: {bid[0]}, Quantity: {bid[1]}")
        print("===========================================")

        
        #ws.close()
        #exit(0)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    print("WebSocket opened.")
    # Subscribe to the depth updates for the desired trading pair (e.g., BTCUSDT)
    ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"btcusdt@depth"], "id":1}))

if __name__ == "__main__":
    # Connect to Binance WebSocket API
    # Create a User
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@depth", 
                                on_message=on_message, 
                                on_error=on_error, 
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()