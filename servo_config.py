import json

with open("servo.json") as f:
    conf = json.load(f)
    UART_PORT = conf["UART_PORT"]
    UART_BAUDRATE = conf["UART_BAUDRATE"]
    UART_BYTESIZE = conf["UART_BYTESIZE"]
    UART_PARITY = conf["UART_PARITY"]
    UART_STOPBITES = conf["UART_STOPBITES"]
    MOTOR_ADDR = conf["MOTOR_ADDR"]
    SIGIN_ADDR = conf["SIGIN_ADDR"]
    SIGIN_REG = conf["SIGIN_REG"]
