import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import requests

class Window(QtWidgets.QTabWidget):
    def __init__(self, current_user):
        super().__init__()
        self.setWindowTitle("CHATBOX")
        self.setGeometry(300, 300,700,850)
        self.move(100,10)
        self.setStyleSheet("background: white;")  
        self.setStyleSheet("color: white; background: #242926")
        self.recievers=[]
        self.recievers_phn=[]
        self.chats=[]
        self.msg = ""
        self.selected_chat='0'
        self.n_grok="http://127.0.0.1:5000"
        self.cur_usr=current_user
        self.status = "Not Connected"
     
        if(current_user == ''):
            self.setLayout(self.user_registration_UI())
        else:
            self.setLayout(self.user_in_UI())
        
    def user_registration_UI(self):
        main_w = QVBoxLayout()
        #print("reg")
        reg_form = QFormLayout()
        phn = QLineEdit()
        phn.textChanged.connect(self.reg_phn)
        
        name = QLineEdit()
        name.textChanged.connect(self.reg_name)

        reg_button = QPushButton("Register")
        reg_button.clicked.connect(self.reg_btn)

        reg_form.addRow(QLabel())
        reg_form.addRow(QLabel("Phone: "), phn)
        reg_form.addRow(QLabel())
        reg_form.addRow(QLabel("Name: "), name)
        reg_form.addRow(QLabel())
        reg_form.addRow(reg_button)
        reg_form.addRow(QLabel())
        main_w.addLayout(reg_form)

        self.setGeometry(300, 300,400,250)
        return main_w

    def reg_phn(self,text):
        self.reg_phoneno = text
    
    def reg_name(self,text):
        self.reg_usname = text

    def reg_btn(self):
        print("rat")
        if(len(self.n_grok)>5):
            r = requests.get(self.n_grok +"/get_user/"+str(self.reg_phoneno))
            r=r.json()
            if(r == "0"):
                r = requests.get(self.n_grok +"/registration/"+str(self.reg_phoneno)+"/"+str(self.reg_usname))
                rec_file = open("reciever.usr","w+")
                rec_file.write(str(self.reg_phoneno) + " " + str(self.reg_usname))
                rec_file.close()
                self.hide()
                self.__init__(str(self.reg_phoneno) + " " + str(self.reg_usname))
                self.show()
                    
            else:
                if(r[str(self.reg_phoneno)] != str(self.reg_usname)):
                    print("User Already Registered...\n But Wrong User Name Entered")
                else:
                    rec_file = open("reciever.usr","w+")
                    rec_file.write(str(self.reg_phoneno) + " " + str(self.reg_usname))
                    rec_file.close()
                    self.hide()
                    self.__init__(str(self.reg_phoneno) + " " + str(self.reg_usname))
                    self.show()
                    
                    

    def user_in_UI(self):

        main_w = QHBoxLayout()

        #Reciever Pane
        r_pane = QVBoxLayout()
        if(self.cur_usr[-1:] == '\n'):
            x=self.cur_usr[:-1]
        else:
            x=self.cur_usr
        user_lbl = QLabel(x[11:] + "\n" + x[:10])
        user_lbl.setStyleSheet("border: 1px solid white; color: black; font-family: SansSerif; font-size: 28px; background-color : #dee3fa;")
        user_lbl.setFont(QFont('Arial', 30))
        user_lbl.setAlignment(Qt.AlignCenter)
        r_pane.addWidget(user_lbl)

        #Reciever List
        r_Box = QGroupBox()
        self.r_form = QFormLayout()
        
        addnewchat_layout = QHBoxLayout()
        addnewchat_layout.addWidget(QLabel("Add  "))
        self.add_chat = QLineEdit()
        self.add_chat.setStyleSheet("background-color : #c0c4c2;")
        self.add_chat.textChanged.connect(self.newchatchanged)
        self.add_chat.editingFinished.connect(self.addnewchat)
        addnewchat_layout.addWidget(self.add_chat)

        r_pane.addLayout(addnewchat_layout)

        #self.r_form.addWidget(self.add_chat)
        self.recievers_btns = []
        
        for i in range(len(self.recievers)):
            self.recievers_btns.append(QPushButton(self.recievers[i][1]+"\n"+self.recievers[i][0]))
            if(self.recievers[i][0]==self.selected_chat):
                self.recievers_btns[i].setStyleSheet("QPushButton"
                                "{"
                                "background-color : #409399;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : #409399;"
                                "}"
                                )

            else:
                self.recievers_btns[i].setStyleSheet("QPushButton"
                                "{"
                                "background-color : #4d74bd;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : #409399;"
                                "}"
                                )
            self.recievers_btns[i].clicked.connect(self.chat_select)

            self.r_form.addWidget(self.recievers_btns[i])

        r_Box.setLayout(self.r_form)
        r_scroll = QScrollArea()
        r_scroll.setWidget(r_Box)
        r_scroll.setWidgetResizable(True)
        r_scroll.setFixedHeight(650)
        r_scroll.setFixedWidth(250)

        r_pane.addWidget(r_scroll)
        main_w.addLayout(r_pane)

        #Msg Pane
        msg_s_r_pane = QVBoxLayout()
        title = QLabel("CHATBOX")
        title.setStyleSheet("border: 2px solid white; color:#3a54c9; SansSerif; font-size: 78px; background-color : #7cfcbc;")
        title.setIndent(10)
        title.setAlignment(Qt.AlignCenter)
        msg_s_r_pane.addWidget(title)
        self.statusbar = QLabel(self.status)
        msg_s_r_pane.addWidget(self.statusbar)

        #Chat Box
        c_Box = QGroupBox()
        self.c_form = QFormLayout()
        self.chat_labels = []
        
        for i in range(len(self.chats)):
            self.chat_labels.append(QLabel(self.chats[i][0]))
            if(self.chats[i][1]==0):        #0 for sent msgs and 1 for recieved
                self.chat_labels[i].setAlignment(Qt.AlignRight)
            else:
                self.chat_labels[i].setAlignment(Qt.AlignLeft)
            self.c_form.addRow(self.chat_labels[i])

        c_Box.setLayout(self.c_form)
        c_scroll = QScrollArea()
        c_scroll.setWidget(c_Box)
        c_scroll.setWidgetResizable(True)
        c_scroll.setFixedHeight(620)
        c_scroll.setFixedWidth(600)
        msg_s_r_pane.addWidget(c_scroll)

        #Send Pane
        send = QHBoxLayout()
        self.send_box = QLineEdit()
        self.send_box.setStyleSheet("background-color : #c0c4c2;")
        self.send_box.textChanged.connect(self.msgChanged)
        self.send_box.editingFinished.connect(self.send_msg)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_msg)
        self.send_btn.setStyleSheet("QPushButton"
                                "{"
                                "background-color : #000080;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : purple;"
                                "}"
                                )

        send.addWidget(self.send_box)
        send.addWidget(self.send_btn)

        msg_s_r_pane.addLayout(send)

        main_w.addLayout(msg_s_r_pane)
        return main_w

    def update_status(self):
        try:
            self.statusbar.setText(self.status)
        except:
            pass
        
    def newchatchanged(self,text):
        self.new_chat = text
    
    def addnewchat(self):
        print(self.new_chat)
        print(self.n_grok)
        if(len(self.new_chat) == 10 and (len(self.n_grok)>5)):
            r = requests.get(self.n_grok +"/get_user/"+str(self.new_chat))
            print(self.n_grok +"/get_user/"+str(self.new_chat))
            r=(r.json())
            print(r)
            
            if(r == "0"):
                print("User doesn't exist")
            else:
                x=''
                for i in r:
                    x = (i,r[i])
                self.recievers.insert(0,(x[0], x[1]))
                r_file = open("reciever.usr","a")
                r_file.write("\n"+x[0]+" "+ x[1])
                r_file.close()

                self.new_chat = "" 
                self.add_chat.setText("")
                self.refresh_w()
            

    def set_n_grok(self, url):
        self.n_grok = url
        #print("=="+self.n_grok+"==")

    def msgChanged(self, text):
      self.msg = text

    def send_msg(self):
      if(self.msg != "" and (len(self.n_grok)>5)):
        #print((self.n_grok+ '/' + str(self.selected_chat) + '/' + str(self.cur_usr[:10]) + '/' + self.msg))  
        r= requests.get(self.n_grok+ '/' + str(self.cur_usr[:10]) + '/' + str(self.selected_chat) + '/' + self.msg)
        #print(r)

        #self.chats.insert(0,(self.msg,0))
        f = open(str(self.selected_chat)+".ct","a") 
        f.write("0 "+self.msg+"\n") 
        f.close()
        
        self.msg = "" 
        self.send_box.setText("")
        self.refresh_c()


    def chat_select(self):
        b=self.sender()
        
        if(self.selected_chat!='0'):
            self.recievers_btns[self.recievers_phn.index(self.selected_chat)].setStyleSheet("QPushButton"
                                    "{"
                                    "background-color : #409399;"
                                    "}"
                                    "QPushButton::pressed"
                                    "{"
                                    "background-color : #409399;"
                                    "}"
                                    )

        self.selected_chat = b.text()[-10:]
        
        b.setStyleSheet("QPushButton"
                                "{"
                                "background-color : #4d74bd;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : #409399;"
                                "}"
                                )
        
        
        self.refresh_c()
        

    def refresh_w(self):
        #print("Bharat")
        #print(self.recievers)
        self.recievers_phn=[]
        for i in range(len(self.recievers)):
            self.recievers_phn.append(self.recievers[i][0])
            if(i<(len(self.recievers_btns))):
                self.recievers_btns[i].setText(self.recievers[i][1]+"\n"+self.recievers[i][0])
            else:
                self.recievers_btns.append(QPushButton(self.recievers[i][1]+"\n"+self.recievers[i][0]))
            
            if(self.recievers[i][0]==self.selected_chat):
                #print('a')
                self.recievers_btns[i].setStyleSheet("QPushButton"
                                "{"
                                "background-color : #4d74bd;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : #409399;"
                                "}"
                                )

            else:
                #print('j')
                self.recievers_btns[i].setStyleSheet("QPushButton"
                                "{"
                                "background-color : #409399;"
                                "}"
                                "QPushButton::pressed"
                                "{"
                                "background-color : #409399;"
                                "}"
                                )

            self.recievers_btns[i].clicked.connect(self.chat_select)
            self.r_form.addWidget(self.recievers_btns[i])
            
    def refresh_c(self):
        try:
            chats_file = open(self.selected_chat+".ct","r")
        except:
            chats_file = open(self.selected_chat+".ct","w+")
            chats_file.close()
            chats_file = open(self.selected_chat+".ct","r")
        
        #print(self.selected_chat)

        self.chats=[]
        for line in reversed(chats_file.readlines()):
            if(line!='\n'):
                self.chats.append((line[2:], int(line[0])))
        
        chats_file.close()

        #print(self.chats)

    
        for i in reversed(range(self.c_form.count())):
            self.c_form.itemAt(i).widget().deleteLater()
        

        self.chat_labels = []
        
        for i in range(len(self.chats)):
            self.chat_labels.append(QLabel(self.chats[i][0]))
            if(self.chats[i][1]==0):
                self.chat_labels[i].setAlignment(Qt.AlignRight)
            else:
                self.chat_labels[i].setAlignment(Qt.AlignLeft)
            self.c_form.addWidget(self.chat_labels[i])
        #print(self.chats)
        #print("hkl")
    

        

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 12pt;font-color: white;}")
    app.setStyle("fusion")
    custom_font = QFont()
    custom_font.setWeight(12)
    QApplication.setFont(custom_font, "QLabel")
    window = Window()

    window.show()
    sys.exit(app.exec_())
'''