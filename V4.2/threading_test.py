import threading
import time


def read_time():
    nts = [0, 0]
    global run_flag
    while True:
        # 获取当前时间
        nts[1] = int(time.strftime('%S', time.localtime(time.time())))
        # 如果秒钟突变
        if nts[1] != nts[0]:
            run_flag = 1
            # print(nts)
        nts[0] = nts[1]
        # 延时30ms
        time.sleep(0.03)


run_flag = 0
t = threading.Thread(target=read_time)
t.start()
while True:
    if run_flag == 1:
        run_flag = 0
        print("run program")