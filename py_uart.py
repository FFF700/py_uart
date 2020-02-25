import serial

uart = serial.Serial('COM2', 115200)
print(uart.portstr)
tx_msg = []


def uart_send(data):
    if uart.is_open:
        print("port opened.")
    else:
        uart.open()

    uart.write(data.encode())


def uart_modbus_read(addr, reg, n):
    tx_msg[0] = addr
    tx_msg[1] = 3
    tx_msg[2] = reg
    tx_msg[3] = n

    uart.write(tx_msg)


def uart_modbus_wirte(addr, reg, data):
    tx_msg[0] = addr
    tx_msg[1] = 6
    tx_msg[2] = reg
    tx_msg[3] = data

    uart.write(tx_msg)


def set_pulses(p_num):
    p_num_h = p_num // 10000
    p_num_l = p_num % 10000


def motor_run_once():
    uart_modbus_wirte(2, 31, 0000)
    uart_modbus_wirte(2, 31, 0xFF00)


def cmd_input():
    cmd = input()
    if cmd == 'set':
        print("set succeed.")
    elif cmd == 'motor':
        print('motor move')


if __name__ == "__main__":
    while True:
        cmd_input()
        if uart.in_waiting:
            rx_msg = uart.read(uart.in_waiting)
            print(rx_msg)
            uart.write(rx_msg)
