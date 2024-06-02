import adafruit_dht
import json
import sys
import time
from awsiot import mqtt5_client_builder
from awscrt import mqtt5
from board import D17
from concurrent.futures import Future

SLEEP_TIME = 60
CONNECTION_SUCCESS_RESPONSE_TIMEOUT = 100
PUBLISH_COMPLETION_RESPONSE_TIMEOUT = 100

topic_name = "RaspberryPi"
future_connection_success_data = Future()

def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Connection Success")
    global future_connection_success_data
    future_connection_success_data.set_result(lifecycle_connect_success_data)

def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Connection Failure - failed with exception:{}".format(lifecycle_connection_failure.exception))

if __name__ == '__main__':
    dht = adafruit_dht.DHT11(D17)

    endpoint = sys.argv[1]
    client_id = "raspberry-pi"

    client = mqtt5_client_builder.mtls_from_path(
        endpoint=endpoint, 
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        cert_filepath="./raspberry_pi_cert.pem",
        pri_key_filepath="./raspberry_pi_private_key.pem",
        client_id=client_id)

    client.start()

    lifecycle_connect_success_data = future_connection_success_data.result(CONNECTION_SUCCESS_RESPONSE_TIMEOUT)
    connack_packet = lifecycle_connect_success_data.connack_packet
    print(
        f"Connected to endpoint:'{endpoint}' with Client ID:'{client_id}' with reason_code:{repr(connack_packet.reason_code)}")

    while True:
        try:
            print(f"Humidity: {dht.humidity}")
            print(f"Temperature: {dht.temperature}")

            publish_future = client.publish(mqtt5.PublishPacket(
                topic=topic_name,
                payload=json.dumps({"humidity": dht.humidity, "temperature": dht.temperature}),
                qos=mqtt5.QoS.AT_LEAST_ONCE
            ))
            publish_completion_data = publish_future.result(PUBLISH_COMPLETION_RESPONSE_TIMEOUT)
            print("PubAck received with {}".format(repr(publish_completion_data.puback.reason_code)))
        except RuntimeError as error:
            # Catch RuntimeError, because of https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/33
            print(error.args[0])
            time.sleep(SLEEP_TIME)
            continue
        except Exception as error:
            # If any other error occurs, exit
            dht.exit()
            client.stop()
            raise error
        time.sleep(SLEEP_TIME)