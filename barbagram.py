import time
import pandas as pd
import requests
import polling2

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
            incoming_messages=polling2.poll(self.getUpdates,args=([offset]),step=step,timeout=timeout)
            if incoming_messages["result"]==[]:
                offset=None
            else:
                func(incoming_messages)
                offset=incoming_messages["result"][-1]["update_id"]+1
                offset+=1

if __name__=="__main__":
    pass