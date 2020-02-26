import serial
import time
import modbus_crc16

try:
    uart = serial.Serial(port='COM7', baudrate=115200, bytesize=8, parity="N", stopbits=2)
    print(uart.portstr)
except WindowsError:
    print("The port has been opened by another program, please check and try again.")


tx_msg = [0, 0, 0, 0, 0, 0, 0, 0]


def uart_send(data):
    if uart.is_open:
        print("port opened.")
    else:
        uart.open()

    uart.write(data.encode())


def modbus_build_frame(addr, cmd, reg, data):
    tx_msg[0] = addr
    tx_msg[1] = cmd
    tx_msg[2] = reg // 256
    tx_msg[3] = reg % 256
    tx_msg[4] = data // 256
    tx_msg[5] = data % 256
    check = modbus_crc16.modbus_crc(tx_msg, 6)
    tx_msg[6] = check % 256
    tx_msg[7] = check // 256

    uart.write(tx_msg)
    print(tx_msg)


def set_pulses(p_num):
    p_num_h: bytes = p_num // 10000
    p_num_l: bytes = p_num % 10000
    modbus_build_frame(1, 6, 0x78, p_num_h)
    modbus_build_frame(1, 6, 0x79, p_num_l)


def motor_run_once():
    modbus_build_frame(2, 6, 0x31, 0x0000)
    time.sleep(0.1)
    modbus_build_frame(2, 6, 0x31, 0xFF00)


def cmd_input():
    str = input()
    cmd = str.split(' ')
    print(cmd[0])
    if cmd[0] == 'set':
        if cmd[1].isdigit():
            set_pulses(int(cmd[1]))
            print("set succeed.")
        else:
            pass

    elif cmd[0] == 'motor':
        motor_run_once()
        print('motor move')


if __name__ == "__main__":
    while True:
        cmd_input()
        if uart.in_waiting:
            rx_msg = uart.read(uart.in_waiting)
            print(rx_msg)
