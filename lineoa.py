import urequests
import json

url = 'https://api.line.me/v2/bot/message/push'

class LineOA_API():
    def __init__(self, channel_access_token, user_id):
        self.channel_access_token = channel_access_token
        self.user_id = user_id
    
    def sendMessage(self, msg):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.channel_access_token
        }
        
        body = {
            'to': self.user_id,
            'messages': [
                {
                    'type': 'text',
                    'text': msg
                }
            ]
        }
        
        res = urequests.post(url, headers=headers, data=json.dumps(body))
        return res
