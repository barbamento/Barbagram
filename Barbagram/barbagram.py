import time
import pandas as pd
import requests
import polling2
import json

class message():
    def __init__(self,json,testing=True):
        print(json)
        self.status=json["ok"]
        if not self.status:
            self.error=json["error_code"]
            if testing:
                raise ValueError ("Error code number : {} \n Reason : {}".format(self.error,json["description"]))
            else:
                print("Error code number : {} \n Reason : {}".format(self.error,json["description"]))

        else:
            self.message_json=json["result"][0]
            print(self.message_json)
            self.update_id=self.message_json["update_id"]
            self.chat_id=self.message_json["message"]["chat"]["id"]
            self.text=self.message_json["message"]["text"]

class telegram:
    def __init__(self,TOKEN):
        self.TOKEN=TOKEN

    def getMe(self):
        return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getMe").json()

    def getUpdates(self,offset=None):
        if offset==None:
            return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getUpdates").json()
        elif isinstance(offset,int):
            print(offset)
            return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getUpdates?offset="+str(offset)).json()
        
    def setWebhook(self):
        return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/setWebhook").json()

    def send_message(self,id,text):#riscrivi in maniera iterativa
        comand="https://api.telegram.org/bot"+str(self.TOKEN)+"/sendMessage?chat_id="+str(id)+"&text="+text
        return requests.get(comand)

    def to_message(self,*kwrgs):
        pass
       
    def start_bot(self,func,step=1,timeout=0,
                **kwargs):
        """
        That's the corpus of the bot, it polls in search for updates, then it applies the function passed as argument

            func:
        function, oprates with the results obtained with the getUpdates methods
        """
        stored_messages=self.getUpdates()
        if stored_messages["result"]==[]:
            offset=None
        else:
            offset=stored_messages["result"][-1]["update_id"]
        while 1:
            incoming_message=polling2.poll(self.getUpdates,args=([offset]),step=step,timeout=timeout)
            if incoming_message["result"]==[]:
                offset=None
            else:
                incoming_message=message(json=incoming_message)
                func(incoming_message)
                offset=incoming_message.update_id+1
                offset+=1

if __name__=="__main__":
    pass