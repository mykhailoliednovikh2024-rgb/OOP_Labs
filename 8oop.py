
import asyncio
import requests
import websockets
import ssl
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

BROKER_ADDRESS = "e1ae39c8342544748a66405e512f94a8.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
TOPIC = "home/value"
USERNAME = "hivemq.webclient.1775715273494"
PASSWORD = "8#,@L*U05zOql9ZIrkYb"
MESSAGE = "1008"

REST_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
WS_HOST = "localhost"
WS_PORT = 8765

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Status: Connected to MQTT Broker")
        client.subscribe(TOPIC) 
    else:
        print(f"Status: MQTT Connection failed: {rc}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    print(f"Status: MQTT Message {mid} sent to cloud")

def on_message(client, userdata, msg):
    print(f"Status: RECEIVED from MQTT: {msg.payload.decode()} on topic {msg.topic}")

mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.tls_set(cert_reqs=ssl.CERT_NONE)
mqtt_client.tls_insecure_set(True)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_message = on_message

async def handle_logic(websocket):
    print("Status: WebSocket client connected")
    try:
        while True:
            
            try:
                loop = asyncio.get_event_loop()
                api_res = await loop.run_in_executor(None, lambda: requests.get(REST_URL, timeout=5))
                print(f"Status: API Check OK ({api_res.status_code})")
            except:
                print("Status: API Check Failed")

            # WebSocket
            await websocket.send(MESSAGE)
            print(f"Status: Sent to WS: {MESSAGE}")

            # MQTT
            mqtt_client.publish(TOPIC, MESSAGE, qos=1)
            
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        print("Status: WebSocket client disconnected")

async def main():
    print("Status: Starting...")
    mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)
    mqtt_client.loop_start()

    print(f"Status: Server on ws://{WS_HOST}:{WS_PORT}")
    async with websockets.serve(handle_logic, WS_HOST, WS_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()