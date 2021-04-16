from gui import *
import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

import threading
import requests
import base64
from time import sleep

n_grok ="http://127.0.0.1:5000" #'http://intruder.pythonanywhere.com'
win = ''
cur_usr=""
c=''

class signal(QObject):
    refresh_c = pyqtSignal()
    refresh_w = pyqtSignal()
    refresh_status = pyqtSignal()



def get_api():
    try:
        r= requests.get(" https://api.github.com/repos/Bharat-Sharma-afk/chatapi/readme")
        x = (((r.json()["content"]).encode("UTF-8")))
        url = ((base64.b64decode(x)).decode("utf-8")) 
        global n_grok
        n_grok = url[:-1]
        global win
        win.set_n_grok(n_grok)
    except:
        get_api()

#def not_in()

def check_new_msg():

    sleep(1)
    global n_grok
    global win
    global c

    if(len(n_grok) <10 or win == "" or win.cur_usr==""):
        #get_api()
        pass
    else:
        try:
            print("Recieving from: "+ n_grok)
            r= requests.get(n_grok+"/"+ win.cur_usr[:10])
            r=(r.json())
            print(r)
            if(r != 0):
                r=dict(r)
                reciever_file = open("reciever.usr","r+")
                recievers_list = reciever_file.readlines()
                recievers_list = recievers_list[1:]
                for i in range(len(recievers_list)):
                    if(recievers_list[i][-1:] == "\n"):
                        recievers_list[i]=recievers_list[i][:-1]
                recievers_list.reverse()
                
                for i in r:
                    if(i in recievers_list):
                        recievers_list.insert(0,recievers_list.pop(recievers_list.index(i)))    
                    else:
                        recievers_list.insert(0,i)
                    
                    try:
                        chat_file = open(i[:10]+".ct","a")
                    except:
                        open(i[:10]+".ct","w+").close()
                        chat_file = open(i[:10]+".ct","a")
                    
                    for x in r[i]:
                        chat_file.write("1 "+x+"\n")
                    
                    chat_file.close()
                    

                reciever_file.close()

                win.recievers = [(i[:10], i[11:]) for i in recievers_list]  

                c.refresh_w.emit()
                c.refresh_c.emit()
                

                reciever_file = open("reciever.usr","w")
                reciever_file.write(win.cur_usr)
                recievers_list.reverse()
                
                for i in range(len(recievers_list)-1):
                    reciever_file.write(recievers_list[i]+ "\n")
                reciever_file.write(recievers_list[len(recievers_list)-1] )
                reciever_file.close()
            win.status="Connected"
        
        except:
            win.status="Not Connected"
     
    try:
        c.refresh_status.emit()
    except:
        pass    
    check_new_msg()

def main():

    reciever_file = open("reciever.usr","r")
    recievers_list = reciever_file.readlines()

    global cur_usr
    if(len(recievers_list) != 0):
        cur_usr = recievers_list[0]
        recievers_list=recievers_list[1:]
        recievers_list.reverse()

    
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 10pt;}")
    app.setStyle("fusion")
    custom_font = QFont()
    custom_font.setWeight(12)
    QApplication.setFont(custom_font, "QLabel")
    
    global win
    win = Window(cur_usr)

    global n_grok
    win.set_n_grok(n_grok)
    
    global c
    c= signal()
    c.refresh_c.connect(win.refresh_c)
    c.refresh_w.connect(win.refresh_w)
    c.refresh_status.connect(win.update_status)
    win.show()
    win.recievers=[]

    for i in recievers_list:
        if(i[-1:]=='\n'):
            i=i[:-1]
        #print((i[:10],i[11:]))
        win.recievers.append((i[:10],i[11:]))

    win.refresh_w()
    sys.exit(app.exec_())

#f = threading.Thread(target=get_api,args=())
g = threading.Thread(target=main,args=())
g.start()
#main()
#f.start()
print(n_grok)

#sleep(5)
h = threading.Thread(target=check_new_msg,args=())
h.start()
#check_new_msg()



