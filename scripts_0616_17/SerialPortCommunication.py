import glob
import sys
import time
from queue import Queue
from typing import Union

import json
import re
import serial
import subprocess

from log import MyLog


class SerialPort:

    def __init__(self, port, flag=True, ensure_queue=False):
        self.dut = serial.Serial(port=port, baudrate=230400, timeout=0.1)
        assert self.dut.isOpen(), '\033[0;31m当前串口无法打开，请检查串口的连接\033[0m'
        self.dut.reset_output_buffer()
        self.dut.reset_input_buffer()
        self.flag = flag
        self.ensure_queue = ensure_queue
        if ensure_queue:
            self._queue = Queue()
        self.log = MyLog(f'{port.split(".")[-1]}')


    def write_cmd(self, cmd, delay: Union[int, float] = 0):
        cmd = f'{cmd}\n'.encode('utf-8', errors='ignore')
        try:
            self.dut.write(cmd)
        except serial.serialutil.SerialException as e:
            self.log.logger.error(f'当前串口连接已断开: {e.args[0]}')
            return e.args[0]
        else:
            if delay:
                time.sleep(delay)

    def read_data_queue(self):
        while self.flag:
            t = time.time()
            current_time = self.get_current(t)
            try:
                line = self.dut.readline()
            except serial.serialutil.SerialException as e:
                self.log.logger.error(f'当前串口连接已断开: {e.args[0]}')
                return e.args[0]
            else:
                if line:
                    self.log.logger.info(line.strip().decode('utf-8', errors='ignore'))
                    msg = f'{current_time}| '.encode('utf-8', errors='ignore') + line.strip() + b'\n'
                    if self.ensure_queue:
                        self._queue.put(msg.decode('utf-8', errors='ignore'))

    def read_command(self, prefix=True):
        """
        :param prefix: 是否在每一行返回值前面添加时间
        :return: 返回字符串结果
        """
        msg = b''
        while True:
            try:
                line = self.dut.readline()
            except serial.serialutil.SerialException as e:
                return e.args[0]
            else:
                if line:
                    if prefix:
                        t = time.time()
                        current_time = self.get_current(t)
                        msg += f'{current_time}| '.encode('utf-8', errors='ignore') + line.strip() + b'\n'
                    else:
                        msg += line.strip() + b'\n'
                else:
                    break
        return msg.decode('utf-8', errors='ignore')

    def read_with_logging(self):
        msg = ''
        while True:
            try:
                line = self.dut.readline()
            except serial.serialutil.SerialException as e:
                self.log.logger.error(f'当前串口连接已断开: {e.args[0]}')
                msg = e.args[0]
                break
            else:
                if line:
                    line_str = line.strip().decode('utf-8')
                    msg += line_str + '\n'
                    self.log.logger.info(line_str)
                else:
                    break
        return msg

    @staticmethod
    def get_current(t: float):
        # t = time.time()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        mirco_second = str(t - int(t))[2:6]
        current_time = '{}.{}'.format(time_str, mirco_second)
        return current_time

    def get(self):
        if self.ensure_queue:
            try:
                value = self._queue.get(timeout=0.5)
            except TimeoutError as e:
                print(e.args[0])
                return
            else:
                return value
        raise Exception('当前串口没有使用队列')


def get_port(key='/dev/cu.chimp*'):
    ports = glob.glob(key)
    if len(ports) == 0:
        print('\n\033[1;31m No Device is detected ☹️ !\n \033[94mTry again😊,please.\033[0m\n')
        sys.exit(100)
    if len(ports) == 1:
        return ports[0]

    for i, port in enumerate(ports):
        print(f'{i}  {port}')
    choice = input('请选择串口前面的序号：')
    try:
        port = ports[int(choice)]
    except IndexError:
        raise IndexError(f'输入的值超出了允许的范围，只能输入0-{len(ports) - 1}之间的数字')
    except ValueError:
        raise ValueError('输入的值的类型不正确')
    else:
        return port


def get_ports(key='/dev/cu.chimp*'):
    ports = glob.glob(key)

    if len(ports) == 0:
        print('\n\033[1;31m No Device is detected ☹️ !\n \033[94mTry again😊,please.\033[0m\n')
        sys.exit(100)

    return ports


def get_port_name_from_location_id(controlBox="/dev/tty.usbmodemH36_H37_211"):
    ports = []
    with open('DutInfo.json', 'r') as file:
        dut_config = json.load(file)
    print(dut_config)
    ioreg_output = subprocess.check_output(['ioreg', '-Src', 'IOUSBDevice']).decode('utf-8')
    usb_devices = re.split(' }', ioreg_output)

    for device in usb_devices:
        for index in range(4):
            location_id_match = re.search(r'"locationID" = (\w+)', device)
            if location_id_match and (dut_config[controlBox]['Unit{}'.format(index+1)] == int(
                    location_id_match.group(1))):
                sn_match = re.search(r'"USB Serial Number" = "(.*)"', device)
                # sn_match = re.search(r'"USB Vendor Name" = "(.*)"', device)
                if sn_match:
                    sn = sn_match.group(1)
                    port_name = "/dev/cu.usbmodem{}2".format(sn)
                    ports.append(port_name)
                    print("======== portName =========" + port_name)
    return ports
# get_port_name_from_location_id()