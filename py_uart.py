import serial
import time
import modbus_crc16
from servo_config import MOTOR_ADDR, SIGIN_ADDR, SIGIN_REG, UART_PORT, UART_BAUDRATE, UART_BYTESIZE, UART_PARITY, \
    UART_STOPBITES

try:
    uart = serial.Serial(port=UART_PORT, baudrate=UART_BAUDRATE, bytesize=UART_BYTESIZE, parity=UART_PARITY,
                         stopbits=UART_STOPBITES)
    print(uart.portstr)
except WindowsError:
    print("The port has been opened by another program, please check and try again.")


def uart_send(data):
    if uart.is_open:
        print("port opened.")
    else:
        uart.open()

    uart.write(data.encode())


def modbus_build_frame(addr, cmd, reg, data):
    tx_msg = bytearray(8)
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
    print(f"TX: {tx_msg}")


def set_pulses(p_num):
    is_positive = True
    if p_num < 0:
        is_positive = False
        p_num = 0 - p_num
    p_num_h = p_num // 10000
    p_num_l = p_num % 10000
    if is_positive:
        pass
    else:
        if p_num_h == 0:
            pass
        else:
            p_num_h = 65536 - p_num_h
        if p_num_l == 0:
            pass
        else:
            p_num_l = 65536 - p_num_l
    print(f"{p_num_h},{p_num_l}")
    modbus_build_frame(MOTOR_ADDR, 6, 0x78, p_num_h)
    time.sleep(0.1)
    modbus_build_frame(MOTOR_ADDR, 6, 0x79, p_num_l)


def sigin_init():
    modbus_build_frame(SIGIN_ADDR, 6, int(SIGIN_REG, 16), 0x0000)


def motor_run_once():
    modbus_build_frame(SIGIN_ADDR, 6, int(SIGIN_REG, 16), 0xFF00)
    time.sleep(0.1)
    modbus_build_frame(SIGIN_ADDR, 6, int(SIGIN_REG, 16), 0x0000)


def cmd_input():
    str = input()
    cmd = str.split(' ')
    print(cmd[0])
    if cmd[0] == 'set':
        try:
            if int(cmd[1]) > 99999999 or int(cmd[1]) < -99999999:
                print("Out of range! Number of pulse must in range -99999999~99999999.")
            else:
                set_pulses(int(cmd[1]))
                print("set succeed.")
        except ValueError:
            print("Type error! Please input a number after \"set\".")

    elif cmd[0] == 'motor':
        motor_run_once()
        print('motor move')
    else:
        pass


if __name__ == "__main__":
    sigin_init()
    while True:
        cmd_input()
        if uart.in_waiting:
            rx_msg = uart.read(uart.in_waiting)
            print(f"RX: {rx_msg}")
