import argparse
import json
import os
import signal
import sys

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from jtalk import jtalk


DEVICE_NAME = os.getenv('DEVICE_NAME', 'demo')
AWS_ENDPOINT = os.getenv('AWS_ENDPOINT')
AWS_ROOTCA = os.getenv('AWS_ROOTCA')
AWS_PRIVKEY = os.getenv('AWS_PRIVKEY')
AWS_CERT = os.getenv('AWS_CERT')

client = AWSIoTMQTTClient(DEVICE_NAME)  
client.configureEndpoint(AWS_ENDPOINT, 8883)
client.configureCredentials(AWS_ROOTCA, AWS_PRIVKEY, AWS_CERT)
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(300)
client.configureMQTTOperationTimeout(10)


def say(client, userdata, message):
    """
        jtalk関数を呼び出すコールバック
    """
    data = json.loads(message.payload.decode('utf-8'))
    jtalk(data['text'])

def main():
    client.subscribe('speaker/'+DEVICE_NAME+'/say', 1, say)
    client.connect(60)
    client.publish('speaker/'+DEVICE_NAME+'/stat', 'connected.', 1) 
    try:
        signal.pause()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()