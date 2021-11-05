import wmi
import win32process
import win32gui




def enum_running_process():
    f=wmi.WMI()
    list_proc=[]
    
    for process in f.Win32_Process():
        list_proc.append([process.Name,str(process.ProcessID),str(process.ThreadCount)])
    return list_proc






def kill_process_by_id(process_id):
    f=wmi.WMI()
    cnt = 0
    
    for process in f.Win32_Process():
        if process.ProcessId == process_id:
            process.Terminate()
            cnt+= 1 
    if cnt == 0:
        return False
    else:
        return True

is_app = False
def enumWindowsProc(hwnd, lParam):
    global is_app
    if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam)):
        if win32gui.GetWindowText(hwnd) and win32gui.IsWindowVisible(hwnd):
            is_app = True

def enum_running_app():
    global is_app
    list_app = []
    f = wmi.WMI()

    for process in f.Win32_Process():
        win32gui.EnumWindows(enumWindowsProc, process.ProcessID)
        
        if is_app:
            # print(f"{process.Name}\t{process.ProcessID}\t{process.ThreadCount}")
            list_app.append([process.Name,str(process.ProcessID),str(process.ThreadCount)])
            is_app = False
    
    return list_app






