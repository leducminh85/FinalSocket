import cv2, pickle,struct,imutils
import pyautogui
import numpy as np

count_frame = 0
def streaming(client_socket):
    global count_frame
    
    while(True):
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame,width=600)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a 
        client_socket.sendall(message)
        
        #cv2.imshow('TRANSMITTING VIDEO',frame)
        count_frame+=1        
        print(count_frame)
        # key = cv2.waitKey(1) & 0xFF
        if cv2.waitKey(1) == ord('q'):
            break





        
