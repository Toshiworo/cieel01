from BotAmino import *
 
import requests
from os import path
import urllib.request
import datetime
 
import json 
from time import sleep
from functools import update_wrapper, wraps
from amino import Client, SubClient
client = Client()
def socketRoot():
    j=0
    while True:
        if j>=300:
            print("Updating socket.......")
            client.close()
            client.run_amino_socket()
            print("Socket updated")
            j=0
        j=j+1
        time.sleep(1)
 
 
print("wait...")
email="e5irgt7mg@1secmail.net"
password="Poto12"
client = BotAmino(email, password)

client.prefix = "/"
 
client.wait=8 # set the prefix to /

claim_data = {}
claim_data_file = "claim_data.json"
if path.exists(claim_data_file):
    with open(claim_data_file) as f:
        claim_data = json.load(f)
 
@client.command("pong") # "pong" the command, the test function is not necessary
def pong(data: Parameters):
    if data.subClient.is_in_staff(data.authorId): # will execute the command if the user is in the amino's staff (learder/curator)
        data.subClient.send_message(data.chatId, message="ping!")
        
@client.command("claim")
def rest(args):
    now= datetime.datetime.now().day
    full=datetime.datetime.now()
    delta = full - datetime.timedelta(hours=24)
    com=str(args.comId)
    user=str(args.authorId)
    level=int(args.level)
    ccid=None
    
    if level < 5:
        args.subClient.send_message(args.chatId,message=f"<${args.author}$> you are below level 5",replyTo=args.messageId, mentionUserIds=[args.authorId])
    else:
            if user not in claim_data:
                wallet=int(args.subClient.get_wallet_amount())
                wikiId=args.subClient.get_user_wikis(userId=args.authorId,size=1).wikiId
                #print(wikiId)
                if len(wikiId) ==0 or wallet< 40:
                    blogId=args.subClient.get_user_blogs(userId=args.authorId,size=1).blogId
                    if len(blogId) ==0:
                        args.subClient.send_message(args.chatId,message=f"<${args.author}$> make a blog or maybe my wallet is empty",replyTo=args.messageId, mentionUserIds=[args.authorId])
                    else:
                        args.subClient.send_coins(blogId=blogId[0],coins=40)
                        args.subClient.send_message(args.chatId,message=f"<${args.author}$> claimed props",replyTo=args.messageId, mentionUserIds=[args.authorId])
                        claim_data[user] = {"tim": now, "full_time": str(delta)}
                    with open(claim_data_file, "w") as f:
                        json.dump(claim_data, f)
                else:
                    
                    args.subClient.send_coins(objectId=wikiId[0],coins=40)
                    args.subClient.send_message(args.chatId,message=f"<${args.author}$> claimed props",replyTo=args.messageId, mentionUserIds=[args.authorId])
                    claim_data[user] = {"tim": now, "full_time": str(delta)}
                    with open(claim_data_file, "w") as f:
                        json.dump(claim_data, f)
             
            else:
                        old = claim_data[user]["tim"]
                        if now-old !=0:
                            
                            wikiId=args.subClient.get_user_wikis(userId=args.authorId,size=1).wikiId
                            wallet=int(args.subClient.get_wallet_amount())
                            if len(wikiId) ==0 or wallet< 40:
                                blogId=args.subClient.get_user_blogs(userId=args.authorId,size=1).blogId
                                if len(blogId) ==0:
                                    args.subClient.send_message(args.chatId,message=f"<${args.author}$> make a blog or maybe my wallet is empty",replyTo=args.messageId, mentionUserIds=[args.authorId])
                                else:
                                    args.subClient.send_coins(blogId=blogId[0],coins=40)
                                    args.subClient.send_message(args.chatId,message=f"<${args.author}$> claimed props",replyTo=args.messageId, mentionUserIds=[args.authorId])
                                    update2(user,now,str(delta))
                            else:
                                args.subClient.send_coins(objectId=wikiId[0],coins=40)
                                args.subClient.send_message(args.chatId,message=f"<${args.author}$> claimed props",replyTo=args.messageId, mentionUserIds=[args.authorId])
                                update_wrapper(user,now,str(delta))
                                
                                claim_data[user] = {"tim": now, "full_time": str(delta)}
                                with open(claim_data_file, "w") as f:
                                    json.dump(claim_data, f)
                        else:
                            remaining = datetime.datetime.strptime(claim_data[user]["full_time"], 
                            '%Y-%m-%d %H:%M:%S.%f') + datetime.timedelta(days=1)
                            args.subClient.send_message(args.chatId, message=f"<${args.author}$> You can only claim props once per day, remaining time: {remaining - full}", replyTo=args.messageId, mentionUserIds=[args.authorId])
                                              
                  
                
import os
from time import sleep
import threading
import sys
def maintenance():
    print("launch maintenance")
    i = 0
    while i < 7200:
        i += 10
        sleep(10)
    os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])
client.launch()
threading.Thread(target=maintenance).start()
def reconsocketloop():
    while True:
        client.close()
        client.run_amino_socket()
        sleep(120)
 
 
socketloop = threading.Thread(target=reconsocketloop, daemon=True)
socketloop.start()
 
print("Ready")