import os
import platform





def shutdown(time):
    OS_type = platform.system()
    OS_type = OS_type.lower()
    shutdown_str=""
    if OS_type == 'linux':
        time = time /60
        shutdown_str = 'shutdown -t '+ str(time)
    elif OS_type == 'windows':
        #time = time * 60
        shutdown_str = 'shutdown -s -t ' + str(time)
    else:
        print('Sorry this feature is not available in ', OS_type)
        return

    os.system(shutdown_str)

def cancel_shutdown():
    OS_type = platform.system()
    OS_type = OS_type.lower()
    if OS_type == 'linux':
        cancel_str = 'shutdown -c'
    elif OS_type == 'windows':
        cancel_str = 'shutdown -a'
    else:
        return
    os.system(cancel_str)

def log_out():
    log_out_str = 'shutdown /l'
    os.system(log_out_str)

