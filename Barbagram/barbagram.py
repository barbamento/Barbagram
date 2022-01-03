import time
from typing import ValuesView
from typing_extensions import ParamSpec
import pandas as pd
import requests
import polling2
import json

if True:
    base_structure2={"chat_id":None,
                    "text":None,
                    "parse_mode":None,
                    "entities":None,
                    "disable_web_page_preview":None,
                    "disable_notification":None,
                    "protect_content":None,
                    "reply_to_message_id":None,
                    "allow_sending_without_reply":None,
                    "reply_markup":None,
                }

class message():
    def __init__(self,json,testing=True):
        self.status=json["ok"]
        if not self.status:
            self.error=json["error_code"]
            if testing:
                raise ValueError ("Error code number : {} \n Reason : {}".format(self.error,json["description"]))
            else:
                print("Error code number : {} \n Reason : {}".format(self.error,json["description"]))
        else:
            self.message_json=json["result"][0]
            self.update_id=self.message_json["update_id"]
            self.chat_id=self.message_json["message"]["chat"]["id"]
            self.text=self.message_json["message"]["text"]

class button:
    def __init__(self,text,callback):
        pass

class keyboard:
    def __init__(self,buttons,shape=None):
        if shape==None:
            shape=[len(buttons),1]
        array=[]
        for i in buttons:
            array+=[{"text":i}]
        self.keyboard=array

    def to_inline(self,callback_data=None):#do a function in the buttons class then call it iteratively
        if callback_data!=None:
            if len(self.keyboard)!=len(callback_data):
                raise ValueError ("keyboard and callback data dimension mismatch")
        for dict,i in list(zip(self.keyboard,range(len(self.keyboard)))):
            dict["callback_data"]=i
        self.keyboard={"inline_keyboard":[self.keyboard]}

class telegram:
    def __init__(self,TOKEN):
        self.TOKEN=TOKEN

    def print_link(self):
        print("https://api.telegram.org/bot"+str(self.TOKEN)+"/getMe")

    def getMe(self):
        return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getMe").json()

    def getUpdates(self,offset=None):
        if offset==None:
            return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getUpdates").json()
        elif isinstance(offset,int):
            print(offset)
            return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getUpdates?offset="+str(offset)).json()
  
    def InlineMarkupButton(self,**kwargs):#deprecated?
        button={}
        for i in kwargs:
            button[i]=kwargs[i]
        return button

    def sendMessage(self,**kwargs):
        params=self.to_message(**kwargs)
        params["method"]="sendMessage"
        print(params)
        return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/",json=params)

    def to_message(self,**kwargs):
        base_structure={}
        for i in kwargs:
            base_structure[i]=kwargs[i]
        return base_structure

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

    def setComands(self,list):
        return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/setMyCommands?commands={prova,prova}").json()
        
if __name__=="__main__":
    pass