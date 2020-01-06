import random
import time

buff = []
buff_ave = []
while True:
    x = random.randint(1, 10)
    print(x)

    buff.append(x)
    print('len(buff):', len(buff))

    if len(buff) >= 5:
        print("Before pop:", buff)
        buff_ave.append(sum(buff) / len(buff))
        buff.pop(0)

        print('After pop:', buff)

    else:
        buff_ave.append(x)

    print('Averge:', buff_ave[-1])

    time.sleep(1)
