import serial


def USB_recv():
    ser = serial.Serial("COM5", 115200)
    ser.close()
    ser.open()
    num = 66
    # while True:
    for i in range(2):
        USB_recv_data = ((ser.read(num)).decode('ASCII')).replace("\r\n", "")
        # data = data.replace("\r", "")
        # data = data.replace("\n", "")
        USB_recv_data = bytes(USB_recv_data, encoding="utf8")
        print(USB_recv_data)
        data = []
        data.append(int(("0x" + (USB_recv_data[0: 16].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[16: 32].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[32: 48].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[48: 64].decode())), 16))
        print(data)
        # InsertAngelData(angle, 1, data[0], data[1], data[2], data[3])
    ser.close()

USB_recv()