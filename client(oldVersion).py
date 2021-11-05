import os
from tkinter import *
import tkinter.messagebox as mbox 
from tkinter import ttk, filedialog
import tkinter as tk
import socket
import threading
import numpy as np
import cv2, pickle,struct
import PIL.Image, PIL.ImageTk


TITLE = "Client "
connected =False
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
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


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    #print(client.recv(1024).decode(FORMAT))

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

def send_file(conn, filename):
    file = open(filename,"rb")
    size = get_Size(file)
    size = str(size)
    file.close()
    # conn.send(size.encode(FORMAT))
    send1(conn,size)

    with open(filename, "rb") as fp:
        data = fp.read(1024)
        while data:
            conn.send(data)
            data = fp.read(1024)
            if not data:
                break


def recv_file(conn, filename):
    size = recv1(conn)
    size = int(size)
    i = 0
    with open(filename,"wb") as file:
        while True:
            i +=1024
            byte_read = 1024
            
            data = conn.recv(byte_read)
            file.write(data)
            if i > size:
                file.close()
                break
            if size - i < 1024:
                byte_read = size - i

def recv_file1(conn,filename):
    size = recv1(conn)
    size = int(size)
    t = size/2
    t= int(t)
    with open(filename,'wb') as file:
        for i in range(t):
            data = conn.recv(2)
            file.write(data)

def PlaceWindow(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def CloseWindow(root):
    root.destroy()


 #ProcessRunning------------------------------------------------------------------------------------------

#PROCESSRUNNING-------------------------------------------------------------------------------------------
def doProcessRunning():
    global connected
    if connected == True:
        proc_name_l, pid_l, thread_cnt_l = [], [], []
        count = 0

        def KILL_PR():


            def KILL_PR_EXECUTE(event):
                send(KILL_PROCESS_VIA_PID)
                kill_this_pid = entry.get()
                send1(client,str(kill_this_pid))
                succeed = recv1(client)
                if succeed == "True":
                    
                    mbox.showinfo(None,"Operation compeleted")
                else:
                    mbox.showinfo(None,"Process not found")

            RootPR_KILL = Toplevel(RootPR)
            RootPR_KILL.title(40*" "+"KILL")
            RootPR_KILL.geometry("400x50")
            RootPR_KILL.resizable(0, 0)
            RootPR_KILL.grab_set()

            entry = Entry(RootPR_KILL, width = 40)
            buttonPR_KILL_InSide = Button(RootPR_KILL, text = "KILL",width=10, height = 1)
            buttonPR_KILL_InSide.bind("<Button-1>", KILL_PR_EXECUTE)


            entry.place(x = 20, y = 15)
            buttonPR_KILL_InSide.place(x = 280, y = 15)

            
            
        
        def SHOW_PR():
            send(RUNNING_PROCESS)
            size = recv1(client)
            size = int(size)
            for i in range(size):
                name = recv1(client)
                pid = recv1(client)
                threadCount =recv1(client)
                
                tree.insert('', 'end', iid= i, text="" , values=(name,pid,threadCount))
                
            
        
        def DELETE_PR():
            for i in tree.get_children():
                tree.delete(i)
            

        def START_PR():
            def START_PR_EXECUTE():
                send(START_PROCESS)
                proc = entry.get()
                send1(client, proc)
                

            RootPR_START = Toplevel(RootPR)

            RootPR_START.title(40*" "+"START")
            RootPR_START.geometry("400x50")
            
            RootPR_START.resizable(0, 0)
            RootPR_START.grab_set()
            
            entry = Entry(RootPR_START, width = 40)
            buttonPR_START_InSide = Button(RootPR_START, text = "START",width=10, height = 1, command = START_PR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonPR_START_InSide.place(x = 280, y = 15)

        def Back():
            CloseWindow(RootPR)

        #------------------------------------------------------
        RootPR = Toplevel(Client_windows)
        RootPR.title("Process")
        PlaceWindow(RootPR, 730, 400)
        RootPR.grab_set()
        RootPR.resizable(0,0)
        

        
        #KILL
        buttonPR_KILL = Button(RootPR, text = 'KILL', width = 15, height = 4, command= KILL_PR)
        buttonPR_KILL.place(x = 175, y = 20)

        #SHOW
        buttonPR_SHOW = Button(RootPR, text = 'SHOW', width = 15, height = 4, command = SHOW_PR)
        buttonPR_SHOW.place(x = 290, y = 20)

        #DELETE
        buttonPR_SHOW = Button(RootPR, text = 'DELETE', width = 15, height = 4, command = DELETE_PR)
        buttonPR_SHOW.place(x = 405, y = 20)

        #Start
        buttonPR_SHOW = Button(RootPR, text = 'START', width = 15, height = 4, command= START_PR)
        buttonPR_SHOW.place(x = 520, y = 20) 

        #BACK
        Back_button = Button(RootPR, text = "BACK", width = 15, height = 4, command = Back)
        Back_button.place(x = 60, y = 20)

        #Table
        tree =ttk.Treeview(RootPR, column=("c1", "c2", "c3"), show='headings')
        vsb = ttk.Scrollbar(RootPR, orient="vertical", command=tree.yview)
        
        tree.bind('<Button-1>', "break")
    
        tree.column("#1", anchor=tk.CENTER, minwidth = 0, width = 260, stretch= FALSE)
        tree.heading("#1", text="Name Process")
        tree.column("#2", anchor=tk.CENTER, minwidth = 0, width = 157 ,stretch=FALSE)
        tree.heading("#2", text="ID Process")
        tree.column("#3", anchor=tk.CENTER, minwidth = 0, width = 157, stretch=FALSE)
        tree.heading("#3", text="Count Thread")
        tree.place(x = 60, y = 100, height = 250)
        vsb.place(x = 635, y = 100, height = 250)
    else:
        mbox.showinfo(None,"No connection established!")


#KEYSTROKE------------------------------------------------------------------------------------------------
hooked = False
def doKEYSTROKE():
    global connected
    if connected == True:

        def HOOK():
            global hooked
            if hooked == False: 
                hooked=True
                send1(client,KEYLOGGING)
            else : pass
            
        def A():
            threading.Thread(target=HOOK).start()



        def UNHOOK():  
            global hooked
            hooked = False
            send1(client,STOP_KEYLOGGING)

        def B():
            threading.Thread(target=UNHOOK).start()



        def PRINT():
            global hooked
            if hooked ==True:
                send1(client,PRINT_KEYLOG)
                key_log_string = recv1(client)
                if key_log_string == "File not found":
                    key_log_string =""
                else:
                    text.config(state="normal")
                    text.insert('end',key_log_string)
                    text.config(state="disabled")
                   
            else:
                mbox.showinfo(None,"Keystroke is not hooked!")
        def C():
            threading.Thread(target=PRINT).start()
        def DELETE():
            text.config(state="normal")
            text.delete(1.0,'end')
            text.config(state="disabled")
        def D():
            threading.Thread(target=DELETE).start()
        def Back():
            CloseWindow(RootK)

        def LockKeyboard():
            send(LOCK_KEYBOARD)
            reply = recv1(client)
            if reply == 'DONE':
                mbox.showinfo(None,"Server keyboard locked!")
            else:
                mbox.showinfo(None,"Error occurred while trying to lock server's keyboard")
    
        def unLockKeyboard():
            send(UNLOCK_KEYBOARD)
            reply = recv1(client)
            if reply == 'DONE':
                mbox.showinfo(None,"Server keyboard unlocked!")
            else:
                mbox.showinfo(None,"Error occurred while trying to unlock server's keyboard")



        #-----------------------------------------------------------------------------------    

        RootK = Toplevel(Client_windows)
        RootK.title("Keyboard")
        PlaceWindow(RootK, 730, 400)
        RootK.grab_set()
        RootK.resizable(0,0)

        #HOOK
        buttonK_HOOK = Button(RootK, text = 'Hook',width = 15, height = 3, command = A)
        buttonK_HOOK.place(x = 60, y = 20)

        #UNHOOK
        buttonK_UNHOOK = Button(RootK, text = 'UnHook', width = 15, height = 3, command= B)
        buttonK_UNHOOK.place(x = 175, y = 20)

        #PRINT
        buttonK_PRINT = Button(RootK, text = 'Print', width = 15, height = 3, command= C)
        buttonK_PRINT.place(x = 520, y = 20)

        #DELETE
        buttonK_DELETE = Button(RootK, text = 'Lock Keyboard', width = 15, height = 3, command = LockKeyboard)
        buttonK_DELETE.place(x = 290, y = 20)

        #BACK
        Back_button = Button(RootK, text = "Unlock Keyboard", width = 15, height = 3, command = unLockKeyboard)
        Back_button.place(x = 405, y = 20)
        
        #BACK
        Back_button = Button(RootK, text = "Back", width = 15, height = 2, command = Back)
        Back_button.place(x = 175, y = 350)

        #DELETE
        buttonK_DELETE = Button(RootK, text = 'Delete', width = 15, height = 2, command= D)
        buttonK_DELETE.place(x = 405, y = 350)       

        #TABLE
        text = Text(RootK)
        text.place(x = 60, y = 90, width = 575, height = 250)
    else:
        mbox.showinfo(None,"No connection established!")


#APPRunning-----------------------------------------------------------------------------------------------

def doAPPRunning():
    global connected
    if connected == True:

        def KILL_AR():

            def KILL_PR_EXECUTE():
                send(KILL_PROCESS_VIA_PID)
                kill_this_pid = entry.get()
                send1(client,str(kill_this_pid))
                succeed = recv1(client)
                if succeed == "True":
                    
                    mbox.showinfo(None,"Operation compeleted")
                else:
                    mbox.showinfo(None,"Process not found")

            
            RootAR_KILL = Toplevel(RootAR)
            RootAR_KILL.title(40*" "+"KILL")
            RootAR_KILL.geometry("400x50")
            RootAR_KILL.resizable(0, 0)
            RootAR_KILL.grab_set()

            entry = Entry(RootAR_KILL, width = 40)
            buttonAR_KILL_InSide = Button(RootAR_KILL, text = "KILL",width=10, height = 1, command= KILL_PR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonAR_KILL_InSide.place(x = 280, y = 15)

        def SHOW_AR():
            
            send(RUNNING_APP)
            msg = recv1(client)
            if msg == "No running app!":
                mbox.showinfo(None,'No applications running on server os!')
            else:
                size = int(msg)
                for i in range(size):
                    name = recv1(client)
                    pid = recv1(client)
                    threadCount =recv1(client)
                    
                    tree.insert('', 'end', iid= i, text="" , values=(name,pid,threadCount))
                

        def DELETE_AR():
            for i in tree.get_children():
                tree.delete(i)

        def START_AR():
            def START_AR_EXECUTE():
                send(START_PROCESS)
                proc = entry.get()
                send1(client, proc)

            
            RootAR_START = Toplevel(RootAR)
            RootAR_START.title(40*" "+"START")
            RootAR_START.geometry("400x50")
            RootAR_START.resizable(0, 0)
            RootAR_START.grab_set()

            entry = Entry(RootAR_START, width = 40)
            buttonAR_START_InSide = Button(RootAR_START, text = "START",width=10, height = 1, command= START_AR_EXECUTE)

            entry.place(x = 20, y = 15)
            buttonAR_START_InSide.place(x = 280, y = 15)

        def Back():
            CloseWindow(RootAR)
        #--------------------------------------------
        RootAR = Toplevel(Client_windows)
        RootAR.title("ListApp")
        RootAR.grab_set()
        PlaceWindow(RootAR, 730, 400)
        RootAR.resizable(0,0)

        #KILL
        buttonAR_KILL = Button(RootAR, text = 'KILL', width = 15, height = 4,command= KILL_AR)
        buttonAR_KILL.place(x = 175, y = 20)
        #SHOW
        buttonPR_SHOW = Button(RootAR, text = 'SHOW', width = 15, height = 4, command= SHOW_AR)
        buttonPR_SHOW.place(x = 290, y = 20)
        #DELETE
        buttonPR_SHOW = Button(RootAR, text = 'DELETE', width = 15, height = 4, command= DELETE_AR)
        buttonPR_SHOW.place(x = 405, y = 20)
        #Start
        buttonPR_SHOW = Button(RootAR, text = 'START', width = 15, height = 4, command= START_AR)
        buttonPR_SHOW.place(x = 520, y = 20)
        #Table
        tree =ttk.Treeview(RootAR, column=("c1", "c2", "c3"), show='headings')
        vsb = ttk.Scrollbar(RootAR, orient="vertical", command=tree.yview)

        #BACK
        Back_button = Button(RootAR, text = "Back", width = 15, height = 4, command = Back)
        Back_button.place(x = 60, y = 20)
        
        tree.bind('<Button-1>', "break")
    
        tree.column("#1", anchor=tk.CENTER, minwidth=0, width=260, stretch= FALSE)
        tree.heading("#1", text="Name Application")
        tree.column("#2", anchor=tk.CENTER, minwidth=0, width=157 ,stretch=FALSE)
        tree.heading("#2", text="ID Application")
        tree.column("#3", anchor=tk.CENTER, minwidth=0, width=157, stretch=FALSE)
        tree.heading("#3", text="Count Thread")
        tree.place(x = 60, y = 100, height = 250)
        vsb.place(x = 635, y = 100, height = 250)
    else:
        mbox.showinfo(None,"No connection established!")


#FixRegistry----------------------------------------------------------------------------------------------
def doFixRegistry():
    global connected
    if connected == True:
        # current_function ={1 : Get value
        #                    2 : Set value
        #                    3 : Delete value
        #                    4 : Create key
        #                    5 : Delete key }
        
        def doBrowser():
            global filepath
            filepath = filedialog.askopenfilename()
            try:
                file_directory.delete(0,'end')
                file_directory.insert('end', filepath)
                with open(filepath,'r') as file:
                    content = file.read()
                    textBox.delete('1.0','end')
                    textBox.insert('end',content)
                    
            except Exception:
                pass
        def doSendMessenger():
            send(SEND_REG_FILE)
            msg = textBox.get('1.0','end-1c')
            send1(client,msg)

        global current_function
        current_function = 0

        def dataType_switcher(string):
            switcher = {
                'String': 'REG_SZ',
                'Binary': 'REG_BINARY',
                'DWORD' : 'REG_DWORD',
                'QWORD' : 'REG_QWORD',
                'Multi-String' : 'REG_MULTI_SZ',
                'Expandable String' : 'REG_EXPAND_SZ'
            }
            return switcher.get(string)

        def Send():
            NoticeBox.config(state = 'normal')
            NoticeBox.delete('1.0','end')
            # Get key value
            if current_function == 1:
                send(GET_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                send1(client,path)
                send1(client,value)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                NoticeBox.insert('end',ans)
                NoticeBox.config(state = 'disabled')

            #Set key value
            if current_function == 2:
                send(SET_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                data = Data.get('1.0','end-1c')
                data_type = DataType.get()
                data_type = dataType_switcher(data_type)
                
                send1(client,path)
                send1(client,value)
                send1(client,data)
                send1(client,data_type)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            


            # Delete key value
            if current_function == 3:
                send(DELETE_KEY_VALUE)
                path = path_entry.get('1.0','end-1c')
                value = NameValue.get('1.0','end-1c')
                send1(client,path)
                send1(client,value)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            # Create key
            if current_function == 4:
                send(ADD_NEW_KEY)
                path = path_entry.get('1.0','end-1c')
                send1(client,path)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')

            
            # Delete key
            if current_function == 5:
                send(DELETE_KEY)
                path = path_entry.get('1.0','end-1c')
                send1(client,path)
                ans = recv1(client)
                NoticeBox.config(state = 'normal')
                if ans == '0':
                    NoticeBox.insert('end','The operation completed successfully.')
                else:
                    NoticeBox.insert('end','The system was unable to find the specified registry key or value.')
                NoticeBox.config(state = 'disabled')
        def Delete():
            NoticeBox.config(state = 'normal')
            NoticeBox.delete('1.0','end')
            NoticeBox.config(state = 'disabled')
        def SelectFunction(event):
            
            
            def GetValue():
                global current_function
                current_function = 1
                Data.place_forget()
                DataType.place_forget()
                
                

            def SetValue():
                global current_function
                current_function = 2
                Data.place(x = 170, y = 215, width = 150, height = 20 )
                DataType.place(x = 330, y =215, width = 150, height =20)

            def DltValue():
                global current_function
                current_function = 3
                Data.place_forget()
                DataType.place_forget()

            def CreateKey(): 
                global current_function
                current_function = 4   
                NameValue.place_forget()
                Data.place_forget()
                DataType.place_forget()
            def DltKey():
                global current_function
                current_function = 5
                pass
            
            s= FunctionChoosen.get()
            if  s == " Set value": SetValue()
            if  s == " Get value": GetValue()
            if  s == " Delete value": DltValue()
            if  s == " Create key": CreateKey()
            if  s == " Delete key": DltKey()

        def Back():
            CloseWindow(RootFR)            


        RootFR = Toplevel(Client_windows)
        RootFR.title("Fix Keystroke")
        RootFR.grab_set()
        PlaceWindow(RootFR, 500, 420)
        RootFR.resizable(0,0)


        #Browser---------------
        file_directory = Entry(RootFR)
        file_directory.place(x = 10, y = 10, width = 370)
        file_directory.insert('end', 'Path...')

        Button_Browser = Button(RootFR, text = "Browser", command= doBrowser)
        Button_Browser.place(x = 390, y = 10, width = 100)
        

        #SendMessage-----------
        textBox = Text(RootFR)
        textBox.place(x = 10, y = 40, width = 370, height = 100)
        textBox.insert('end', "Message")
        
        Button_SendMessage = Button(RootFR, text = "Send Message", command= doSendMessenger)
        Button_SendMessage.place(x = 390, y = 40, width = 100, height = 100)

        #Fix------------------
        Label_Fix = Label(RootFR, text  = "Fix Value " + 85*'-')
        Label_Fix.place(x = 10, y = 145)

        #ChooseFunction
        FunctionChoosen = ttk.Combobox(RootFR,state="readonly")
        FunctionChoosen.set("Select function") 
        FunctionChoosen['values'] = (' Get value',' Set value',' Delete value',' Create key', ' Delete key')
        FunctionChoosen.place(x = 10, y =165, width = 477)
        FunctionChoosen.bind('<<ComboboxSelected>>', SelectFunction)

        #Path
        path_entry = Text(RootFR)
        path_entry.place(x = 10, y = 190, width = 477, height = 20)
        path_entry.insert('end', "Path")

        

        #NoticeBox
        NoticeBox = Text(RootFR,state = 'disabled')

        NoticeBox.place(x = 10, y = 240, width = 477, height = 100)

        #NameValue
        NameValue = Text(RootFR)
        NameValue.place(x = 10, y = 215, width = 150, height = 20)
        NameValue.insert('end', "Name Value")

        #Value
        Data = Text(RootFR)
        Data.place(x = 170, y = 215, width = 150, height = 20)
        Data.insert('end', "Data")

        #ChooseType
        DataType = ttk.Combobox(RootFR,state="readonly")
        DataType.set("Select Value Type") 
        DataType['values'] = ('String','Binary','DWORD','QWORD', 'Multi-String', 'Expandable String')
        DataType.place(x = 330, y =215, width = 150, height =20)
        DataType.bind('<<ComboboxSelected>>', SelectFunction)

        #Send, delete button
        Button_Send = Button(RootFR, text = 'Send', command=Send)
        Button_Send.place (x = 200, y = 360, width = 100)

        Button_Delete = Button(RootFR, text = 'Delete', command= Delete)
        Button_Delete.place (x = 320, y = 360, width = 100) 

        #Back
        Button_Back = Button(RootFR, text = 'Back', command = Back)
        Button_Back.place(x = 80, y = 360, width = 100 )

    else:
        mbox.showinfo(None,"No connection established!")

#LiveScreen-----------------------------------------------------------------------------------------------
def doLiveScreen():
    global connected
    if connected == True:

        send(LIVE_SCREEN)

        def Back():
            client.send('N'.encode(FORMAT))
            CloseWindow(RootLS)

        
        
    
        RootLS = Toplevel(Client_windows)
        RootLS.title("LiveScreen")

        windowWidth = 1100
        windowHeight = 700

        PlaceWindow(RootLS, windowWidth, windowHeight)        #Scale the window here
        RootLS.resizable(0, 0)
        RootLS.grab_set()

        
        app = Frame(RootLS, bg="white")
        app.grid()
        app.place(x= 200, y = 60)
        # Create a label in the frame
        lmain = Label(app)
        lmain.grid()

        lmain = Label(app)
        lmain.grid()

        def disable_event():
            pass

        # function for video streaming
        def video_stream():
            RootLS.protocol("WM_DELETE_WINDOW", disable_event)


                
            data = b""
            payload_size = struct.calcsize("Q")

            client.send('Y'.encode(FORMAT))


            while len(data) < payload_size:
                packet = client.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += client.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            


            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = PIL.Image.fromarray(cv2image)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream) 


        

        Back_button = Button(RootLS, text = "Back", width = 25, height = 2, command = Back)
        Back_button.place(x = 200, y = 30)
        
        

        thread = threading.Thread(target=video_stream)
        thread.start()
        # video_stream()
        
                
                
        
        RootLS.mainloop()
    else:
        mbox.showinfo(None,"No connection established!")


    
    
    
    

#ShowFileManager------------------------------------------------------------------------------------------
current_file=""
current_directory=""
def doShowFileExplorer():
    global connected
    if connected == True:

        def BackToMenu():
            CloseWindow(RootFE)
        def Delete():
            send(DELETE_FILE)
            dir=""
            if(current_file ==""):
                dir = current_directory
            else: dir = current_file
            send1(client,dir)
            print(dir)
            reply = recv1(client)
            if reply == "DONE":
                tv.delete(*tv.get_children())

                send(VIEW_FOLDER)
                send(current_directory)

                list_len = int(recv1(client))
                
                for i in range(list_len):
                    name = recv1(client)
                    is_dir = int(recv1(client))
                    if is_dir == 1:
                        tv.insert('','end', text='> '+name)
                    else:
                        tv.insert('','end', text=name)
                mbox.showinfo(None,f"Deleted {dir}.")
            elif reply == "FAIL":
                mbox.showinfo(None,f"Error occurred while trying to delete {dir}.")

        def Add():
            pass

        def Edit():
            pass

        def Send():
            pass

        def Copy():
            send(COPY_DIR)
            dir=""
            if(current_file ==""):
                dir = current_directory
            else: dir = current_file
            send1(client,dir)
            reply = recv1(client)
            if reply == "DONE":
                tv.delete(*tv.get_children())

                send(VIEW_FOLDER)
                send(current_directory)

                list_len = int(recv1(client))
                
                for i in range(list_len):
                    name = recv1(client)
                    is_dir = int(recv1(client))
                    if is_dir == 1:
                        tv.insert('','end', text='> '+name)
                    else:
                        tv.insert('','end', text=name)
                mbox.showinfo(None,f"Copied {dir}.")
            elif reply == "FAIL":
                mbox.showinfo(None,f"Error occurred while trying to copy {dir}.")

        def Backf():
            global current_directory
            if(current_directory==""):
                return
            elif (current_directory=='C:/' or current_directory == "D:/"):
                tv.delete(*tv.get_children())
                current_directory=""
                SearchBox.config(state="normal")
                SearchBox.delete('1.0','end')
                SearchBox.config(state="disabled")
                tv.insert('','end', text='> C:', open=True)
                tv.insert('','end', text='> D:', open=True)

            else:
            
                current_directory = current_directory[:(len(current_directory)-1)]
                current_directory = current_directory[:(current_directory.rfind("/")+1)]
                SearchBox.config(state="normal")
                SearchBox.delete('1.0','end')
                SearchBox.insert('end',current_directory)
                SearchBox.config(state="disabled")

                tv.delete(*tv.get_children())

                send(VIEW_FOLDER)
                send(current_directory)

                list_len = int(recv1(client))
                
                
                
                for i in range(list_len):
                    name = recv1(client)
                    is_dir = int(recv1(client))
                    if is_dir == 1:
                        tv.insert('','end', text='> '+name)
                    else:
                        tv.insert('','end', text=name)

    

        
        
        def OnDoubleClick(event):
            global current_file
            global current_directory
            current_directory =SearchBox.get("1.0","end-1c")
            item = tv.selection()[0]
            dir = tv.item(item,"text")
            
            if dir[0]=='>':     #Is folder
                current_file =""
                dir = dir[2:]
                tv.delete(*tv.get_children())
            
                current_directory = current_directory + dir + "/"

                send(VIEW_FOLDER)
                send(current_directory)

                list_len = int(recv1(client))
                
                
                SearchBox.config(state="normal")
                SearchBox.insert('end',dir)
                if(list_len!=0):
                    SearchBox.insert('end','/')
                SearchBox.config(state="disabled")
                

                for i in range(list_len):
                    name = recv1(client)
                    is_dir = int(recv1(client))
                    if is_dir == 1:
                        tv.insert('','end', text='> '+name)
                    else:
                        tv.insert('','end', text=name)
            else:
                current_file = current_directory + dir
            
        
        #Init TreeView
        RootFE = Toplevel(Client_windows)
        RootFE.title("FileManager")
        PlaceWindow(RootFE,800, 550)
        RootFE.resizable(0, 0)
        RootFE.grab_set()

        tv = ttk.Treeview(RootFE,show='tree')
        ybar = tk.Scrollbar(RootFE,orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscroll = ybar.set)

        
        
        tv.bind("<Double-1>", OnDoubleClick)
        directory='> C:'                                        #Change directory here 
        tv.insert('','end', text=directory, open=True)
        directory='> D:'                                        #Change directory here 
        tv.insert('','end', text=directory, open=True)
        
        
        
        tv.place(x = 50, y = 150, height= 350, width= 700)
        ybar.place(x = 750, y = 150, height = 350)

        #Delete    
        Del_button = Button(RootFE, text = "Delete", width = 15, height = 3, command = Delete)
        Del_button.place(x = 165, y = 20)

        #Add
        Add_button = Button(RootFE, text = "Add", width = 15, height = 3, command = Add)
        Add_button.place(x = 280, y = 20)

        #Edit
        Edit_button = Button(RootFE, text = "Edit", width = 15, height = 3, command = Edit)
        Edit_button.place(x = 395, y = 20)

        #Send
        Edit_button = Button(RootFE, text = "Send", width = 15, height = 3, command = Send)
        Edit_button.place(x = 510, y = 20)

        #Copy
        Edit_button = Button(RootFE, text = "Copy", width = 15, height = 3, command = Copy)
        Edit_button.place(x = 625, y = 20)

        # <--
        Edit_button = Button(RootFE, text = "<<", width = 15, height = 1, command = Backf)
        Edit_button.place(x = 50, y = 100)

        #Dỉrectory
        SearchBox = Text(RootFE, height = 1, width = 65)
        SearchBox.config(state="disabled")
        SearchBox.place(x = 200, y = 100)

        #Back
        Back_button = Button(RootFE, text = "Back", width = 15, height = 3, command = BackToMenu)
        Back_button.place(x = 50, y = 20)
    else:
        mbox.showinfo(None,"No connection established!")

        
# Logout
def doLogout():
    global connected
    if connected == True:
        ans = mbox.askquestion("Server user profile log off","Do you really want to log off server user profile?")
        if ans =='yes':
            send(LOG_OUT)
            mbox.showinfo(None,"Lost connection!")

        else: pass
    else:
        mbox.showinfo(None,"No connection established!")

    

# Shutdown
def doShutDown():
    global connected
    if connected == True:
        ans = mbox.askquestion("Server user profile log off","Do you really want to log off server user profile?")
        if ans =='yes':
            send(client,SHUTDOWN)
            info = recv1(client)
            mbox.showinfo(None,info)
        else:
            pass
    else:
        mbox.showinfo(None,"No connection established!")
        
#ShowMac        
def doShowMac():
    global connected
    if connected == True:
        send(SHOW_MAC_ADDR)
        mac = recv1(client)
        
        def Back():
            CloseWindow(RootSM)

        #--------------------------
        RootSM = Toplevel(Client_windows)
        RootSM.title("MAC address")
        PlaceWindow(RootSM,500,200)
        RootSM.grab_set()

        #View  (write Key Value here)
        ViewKey = Text(RootSM)
        ViewKey.insert("end",f"SERVER MAC ADDRESS: {mac}")
        ViewKey.configure(state='disabled')
        ViewKey.place(x = 50, y = 60, width = 400, height = 100)

        #BACK
        Back_button = Button(RootSM, text = "Back", width = 15, height = 1, command = Back)
        Back_button.place(x = 50, y = 20)
    else:
        mbox.showinfo(None,"No connection established!")



# CONNECT TO SERVER------------------------------------------------
def connect():
    global connected
    IP_server = InputField.get()
    address = (IP_server,PORT)
    try:
        client.connect(address)
        connected = True
        mbox.showinfo(None,f"Connection establish!\n Server IP: {IP_server}")
    except Exception:
        connected =False
        print(Exception)
        mbox.showinfo(None,"Server not found.")

# EXIT == DISCONNECT FROM SERVER------------------------------------
def exit(): 
    try:
        send(DISCONNECT_MESSAGE)
    except Exception as e:
        print(e)
    Client_windows.destroy()
    




#INIT WINDOW
Client_windows = Tk()
Client_windows.title(TITLE)
PlaceWindow(Client_windows, 730, 400)
Client_windows.resizable(0, 0)

#Create menu
InputField = Entry(Client_windows,width = 50)
InputField.place(x = 150,y=50)


Connect_button = Button(Client_windows,text = "Connect",width = 15, pady=1, command= connect)
Connect_button.place(x = 500, y = 50)

ProcessRunning_button = Button(Client_windows, text = "Process Running", width = 15, height = 11, command= doProcessRunning)
ProcessRunning_button.place(x =50, y =100)

Registry_button = Button(Client_windows, text = "KeyStroke", width = 32, height = 5, command= doKEYSTROKE)
Registry_button.place(x =185, y =100)

Shutdown_button =  Button(Client_windows, text = "Shutdown", width = 14, height = 4, command= doShutDown)
Shutdown_button.place(x =185, y =200)

Logout_button =  Button(Client_windows, text = "Logout", width = 15, height = 4, command= doLogout)
Logout_button.place(x =305, y =200)

MA_button =  Button(Client_windows, text = "MAC address", width=15, height = 5, command= doShowMac)
MA_button.place(x =305, y =285)

LiveScreen_button = Button(Client_windows, text = "LiveScreen", width = 32, height = 5, command= doLiveScreen)
LiveScreen_button.place(x = 435, y = 100)

FileManager_button = Button(Client_windows, text = "File Explorer", width = 33, height = 5, command= doShowFileExplorer)
FileManager_button.place(x = 50, y = 285)

Exit_button = Button(Client_windows, text="Exit", width = 14, height = 11, command= exit)
Exit_button.place(x = 560, y = 195)

AppRunning_button = Button(Client_windows, text = "App Running", width = 15, height = 4, command= doAPPRunning)
AppRunning_button.place(x = 435, y = 200)

RegistryOverwrite_button = Button(Client_windows, text = "Fix Registry", width = 15, height = 5, command= doFixRegistry)
RegistryOverwrite_button.place(x = 435, y = 285)



Client_windows.mainloop()