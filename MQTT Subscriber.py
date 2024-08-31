import random
from paho.mqtt import client as mqtt_client
import json

broker = 'broker.emqx.io'
port = 1883
topic = "your/topic"  # The topic you are subscribing to
client_id = f'subscribe-{random.randint(0, 100)}'
username = "your_username"
password = "your_password"

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")
        try:
            # Parse the JSON payload
            data = json.loads(payload)
            angle = data.get("angle")
            distance = data.get("distance")
            print(f"Angle: {angle}, Distance: {distance}")
        except json.JSONDecodeError:
            print("Failed to decode JSON from payload")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
