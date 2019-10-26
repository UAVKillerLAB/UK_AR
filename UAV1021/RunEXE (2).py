import os
import win32api


def isRunning(process_name):
    try:
        print('tasklist | findstr ' + process_name)
        process = len(os.popen('tasklist | findstr ' + process_name).readlines())
        print(process)
        if process >= 1:
            return 1
        else:
            return 0
    except:
        print("程序错误")
        return 0


while True:
    if isRunning("UDP_ser_10140059.exe") == 0:
        win32api.ShellExecute(0, 'open', r'C:\Users\Administrator\Desktop\UAV\UDP_ser_10140059.exe', '', '', 1)
