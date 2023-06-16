import csv
import os
import re
import threading
import time
from subprocess import Popen, PIPE
import pyvisa
from SerialPortCommunication import SerialPort, get_port


def tunnel():
    with Popen('astrisctl relay adam 1', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as res:
        while 1:
            result = res.stdout.readline().decode('utf-8')
            if result:
                print(result)
            else:
                break


class Battery:
    def __init__(self):
        self.command = ['ft module clr all', 'ft auto ship disable', 'syscfg print MLB#', 'ft version']
        port = get_port()
        self.device = SerialPort(port, ensure_queue=True)

        rm = pyvisa.ResourceManager()
        interfaces = rm.list_resources('USB0?*::INSTR')
        print(interfaces)
        # todo 需要填入两个DMM的识别码
        self.dmm_voltage = rm.open_resource('')
        self.dmm_current = rm.open_resource('')
        self.voltage = []
        self.current = []
        self.data = []
        self.data_dict = {}

        path = os.path.expanduser('~/desktop/Battery/') + time.strftime('%Y-%m-%d')
        if not os.path.exists(path):
            os.mkdir(path)
        txt_file = os.path.join(path, 'read_battery_information.txt')
        csv_file = os.path.join(path, 'read_battery_information.csv')
        self.txt = open(txt_file, 'w')

        fieldnames = ['Time', 'Voltage(mV)', 'Current(mA)', 'Tbatt(dC)', 'Vbatt(mV)', 'Ibatt(mA)', 'GGSOC', 'UISOC',
                      'pmid(mV)']
        self.csv = open(csv_file, 'w')
        self.csv_writer = csv.DictWriter(self.csv, fieldnames=fieldnames)
        self.csv_writer.writeheader()

    def read_voltage(self):
        return round(float(self.dmm_voltage.query('MEASUre:VOLTage:DC?')) * 1000, 0)

    def read_current(self):
        return round(float(self.dmm_current.query('MEASUre:CURRent:DC?')) * 1000, 2)

    def cls(self):
        self.dmm_voltage.write('*CLS')
        self.dmm_voltage.write('SYSTem:LOCal')
        self.dmm_current.write('*CLS')
        self.dmm_current.write('SYSTem:LOCal')

    def send_cmd(self, cmd):
        self.device.write_cmd(cmd)

    def write(self):
        while True:
            line = self.device.get()
            self.data.append(line)
            self.txt.write(line)

    @staticmethod
    def get_data(line):
        if re.search('batman data', line):
            return {'Time': line.split('|')[0]}
        elif re.search('Tbatt:', line):
            return {'Tbatt(dC)': re.findall(r'\d+', line)[0]}
        elif re.search('Vbatt:', line):
            return {'Vbatt(mV)': re.findall(r'\d+', line)[0]}
        elif re.search('Ibatt:', line):
            return {'Ibatt(mA)': re.findall(r'\d+', line)[0]}
        elif re.search('GGSOC:', line):
            return {'GGSOC': re.findall(r'\d+', line)[0]}
        elif re.search('UISOC:', line):
            return {'UISOC': re.findall(r'\d+', line)[0]}
        elif re.search('pmid:', line):
            return {'pmid(mV)': re.findall(r'\d+', line)[0]}
        else:
            return {}

    def handle_data(self):
        while True:
            if self.data:
                line = self.data.pop(0)
                data = self.get_data(line)
                if 'Time' in data.keys():
                    self.data_dict.update({'Voltage(mV)': self.voltage.pop(0)})
                    self.data_dict.update({'Current(mA)': self.current.pop(0)})
                self.data_dict.update(data)
                if len(self.data_dict) == 9:
                    self.csv_writer.writerow(self.data_dict)
                    self.data_dict.clear()

    def multi_process(self):
        # 将结果一行一行的加入队列里面
        t1 = threading.Thread(target=self.device.read_data_queue)
        t1.start()
        # 将结果从队列里一个一个取出，追加到里一个列表里，并写入文件里
        t2 = threading.Thread(target=self.write)
        t2.start()
        # 提取数据，并写入csv里面
        t3 = threading.Thread(target=self.handle_data)
        t3.start()

    def start(self):
        # 多线程实现读，写，提取数据，需要三个线程
        self.multi_process()
        try:
            while True:
                self.send_cmd('batman data')
                self.send_cmd('adc read pmid')
                self.voltage.append(self.read_voltage())
                self.current.append(self.read_current())
        except Exception as e:
            print(e)
        finally:
            self.txt.close()
            self.csv.close()
            self.cls()


if __name__ == '__main__':
    tunnel()
    b = Battery()
    b.start()
