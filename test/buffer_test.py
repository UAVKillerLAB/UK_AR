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

'''
if len(process_buff) >= size:
    buff_std = np.std(process_buff)
    buff_mean = np.mean(process_buff)

    count_b = count_b + 1

    loss = abs(data[i] - buff_mean)
    #                     print('buff_std',buff_std)
    #                     print('buff_mean', buff_mean)
    nS = round(np.sqrt(size), 0) * buff_std

    #                     print('loss',loss)               
    #                     print('nS:',nS)

    if loss > 10:
        #                         print('++++++++\n++++++++\n')

        if data[i] - np.mean(process_buff) < 0:
            process_buff.pop()

            process_buff.append(process_buff[-1] - 1)
'''