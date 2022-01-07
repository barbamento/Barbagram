from logging import raiseExceptions
import time
from typing import ValuesView
from typing_extensions import ParamSpec
import pandas as pd
import requests
import polling2
import json

class message():
    def __init__(self,json):
        self.json=json
        if not self.isok():
            raise ValueError("Not connected to the server")
        self.type=self.message_type()
        self.store_constant()

    def isok(self):
        self.status=self.json["ok"]
        if not self.status:
            self.error=json["error_code"]
            raise ValueError ("Error code number : {} \n Reason : {}".format(self.error,json["description"]))
        return self.status
        
    def message_type(self):
        self.type=list(self.json["result"][-1].keys())[1]
        return self.type

    def store_constant(self):
        self.message_json=self.json["result"][0]
        self.update_id=self.message_json["update_id"]
        if self.type=="callback_query":
            self.text=self.message_json[self.type]["data"]
            self.chat_id=self.message_json[self.type]["message"]["chat"]["id"]
        elif self.type=="message":
            self.text=self.message_json[self.type]["text"]
            self.chat_id=self.message_json[self.type]["chat"]["id"]
    

class button:
    def __init__(self,text,**kwarg):
        self.button={"text":text}
        for i in kwarg:
            self.button[i]=kwarg[i]
    
    def to_inline(self,callback,**kwarg):
        self.button["callback_data"]=callback
        return self.button

class keyboard:
    def __init__(self,buttons,orientation="orizontal"):
        self.keyboard=[]
        for text in buttons:
            self.keyboard+=[button(text)]

    def to_keyboard(self,orientation="orizontal"):
        kb=[i.button for i in self.keyboard]
        if orientation=="orizontal":
            return {"keyboard":[kb]}
        elif orientation=="vertical":
            return {"keyboard":[ [i] for i in kb]}
        else:
            raise ValueError("orientation invalid")

    def to_inline(self,callback_data=None,orientation="orizontal"):
        if callback_data==None:
            callback_data=range(len(self.keyboard))
        for i in range(len(self.keyboard)):
            self.keyboard[i]=self.keyboard[i].to_inline(callback_data[i])
        if orientation=="orizontal":
            return {"inline_keyboard":[self.keyboard]}
        elif orientation=="vertical":
            return {"inline_keyboard":[ [i] for i in self.keyboard]}
        else:
            raise ValueError("orientation invalid")

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
            return requests.get("https://api.telegram.org/bot"+str(self.TOKEN)+"/getUpdates?offset="+str(offset)).json()
  
    def sendMessage(self,**kwargs):
        params=self.to_message(**kwargs)
        params["method"]="sendMessage"
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