from slackclient import SlackClient
import os
import sys
import json
import requests

with open('key.json') as json_data:
    d = json.load(json_data)
    key = d['token']

slack_client = SlackClient(key)

def sendMessageToSlack(channel_id,message,emoji):
    try:
        slack_client.api_call("chat.postMessage",channel=channel_id,text=message,username='Alert',icon_emoji=emoji)
    except Exception,e:
        print e
        sys.exit(2)

def getChannelID():
    channels = slack_client.api_call("channels.list")['channels']
    if channels:
        for channel in channels:
            if channel['name'] == 'general':
                return channel['id']
def main():
    try:
        r = requests.get('http://0.0.0.0')
        if(r.status_code == 200):
            id = getChannelID()
            sendMessageToSlack(id, "The Server is up ",":python:")
        else:
             sendMessageToSlack(id, "Something wrong with the application ")
    except Exception,e:
        sendMessageToSlack(getChannelID(), "The server is down",":skull:")
        sys.exit(2)

main()