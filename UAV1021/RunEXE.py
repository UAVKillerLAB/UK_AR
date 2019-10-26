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
    choice = input("请输入操作：（以回车结束）\n1.定标\n2.查表")
    if choice == 1:
        while True:
            if isRunning("UDP_ser_10140059.exe") == 0:
                win32api.ShellExecute(0, 'open', r'D:\OneDrive\Python_project\UAV\UDP_ser_10140059.exe', '', '', 1)
    elif choice == 2:
        while True:
            if isRunning("SelectData.exe") == 0:
                win32api.ShellExecute(0, 'open', r'D:\OneDrive\Python_project\UAV\SelectData.exe', '', '', 1)
    else:
        print("输入有误请重新输入")