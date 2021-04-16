
from flask import Flask, jsonify
app = Flask(__name__)

def open_file(file,x):
   try:
      return open(file,str(x))
   except:
      print(file)
      users = open(file,"w+")
      users.close()
      return open(file,str(x))

@app.route('/get_user/<int:user_id>')
def getuser(user_id):
   users = open_file("users.usr","r+")
   usr_list = users.readlines()
   usr_data = {} 
   for i in usr_list:
      if(i[-1:]=='\n'):
         i=i[:-1]
      usr_data[i[:10]] = i[11:]
   
   if(str(user_id) not in usr_data):
      return '0'
   else:
      return jsonify({str(user_id):usr_data[str(user_id)]})

@app.route('/registration/<int:user_id>/<us_name>')
def register(user_id, us_name):
   users = open_file("users.usr","r+")
   usr_list= users.readlines()
   usr_data=[]
   for i in usr_list:
      if(i[-1:]=='\n'):
         i=i[:-1]
      usr_data.append(i[:10])
      usr_data.append(i[11:])
   print(usr_data)
   print(user_id)
   if(str(user_id) not in usr_data):
      users.write(str(user_id)+" "+str(us_name)+"\n")
   return '200'


@app.route('/<int:sender_id>/<int:reciever_id>/<msg>')
def send(sender_id,reciever_id,msg):

   chat=open_file(str(sender_id)+"-"+str(reciever_id)+".ct","a")
   chat.write("0 "+msg+"\n")
   chat.close()

   recievers = open_file(str(reciever_id)+".usr",'r')

   new_r_list=[]
   flag=1
   for i in recievers.readlines():
      new_r_list.append(i)
      if(i[-1:]=='\n'):
         i=i[:-1]
      if(i == str(sender_id)):
         flag*=0
         
   if(flag!=0):
      new_r_list.insert(0,str(sender_id)+"\n")
   recievers.close()
   
   recievers = open(str(reciever_id)+".usr","w+")
   for i in new_r_list:
      recievers.write(i)
   recievers.close()

   return '200'

@app.route('/<int:user_id>')
def recieve(user_id):

   sender_file = open_file(str(user_id)+".usr",'r')
      
   sender=sender_file.readline()
   if(sender==""):
      return '0'
   else:
      
      users = open_file("users.usr",'r')
      usr_list= users.readlines()
      users.close()
      usr_data=[]
      for i in usr_list:
         if(i[-1:]=='\n'):
            i=i[:-1]
         usr_data.append(i[:10])
         usr_data.append(i[11:])
      
      data={}
      #print(usr_data)     
      print(str(str(sender[:-1]) + " " + str(usr_data[usr_data.index(str(sender[:-1]))+1]))) 
      
      while(sender!="" and sender!="\n"):
         chats=open_file(sender[:-1]+"-"+str(user_id)+".ct",'r')
         msgs=chats.readlines()
         chats.close()

         print("="+str(sender[:-1])+"=")
         data[str(str(sender[:-1]) + " " + str(usr_data[usr_data.index(str(sender[:-1]))+1]))]=[]

         for i in range(len(msgs)):
            if(msgs[i][0] == '0'):
               data[(str(sender[:-1]) + " "+ str(usr_data[usr_data.index(str(sender[:-1]))+1]))].append(msgs[i][2:-1])
               msgs[i] = msgs[i][1:]
               msgs[i] = "1"+ msgs[i]

         chats=open_file(sender[:-1]+"-"+str(user_id)+".ct","w")     
         for msg in msgs:
            chats.write(msg)
         chats.close()

         sender=sender_file.readline()
      
      sender_file.close()

      sender_file = open(str(user_id)+".usr","w+")
      sender_file.write("")
      sender_file.close()

      return (data)


if __name__ == '__main__':
   app.run( host="0.0.0.0")