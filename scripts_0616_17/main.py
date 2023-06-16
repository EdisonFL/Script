import threading,multiprocessing
import time

from SerialPortCommunication import SerialPort, get_port, get_port_name_from_location_id
from low_stress import pre_command, loop_command, post_command, wait_command


class LoopTest:
    def __init__(self, port=None):
        if port is None:
            self.port = get_port('/dev/cu.usbmode*')
        else:
            self.port = port
        self.dut = SerialPort(self.port, flag=True)
        self.startTime = time.time()

    def send_command(self, times: int):
        self.dut.log.logger.info('====================DUT IN PRE====================')
        print(f'{self.port}  PRE 测试开始')
        for cmd in pre_command:
            if cmd in wait_command:
                if self.dut.write_cmd(cmd, delay=wait_command.get(cmd, 0.5)):
                    break
            else:
                if self.dut.write_cmd(cmd, delay=0.5):
                    break
            yield self.dut.read_with_logging()
            self.dut.log.logger.info('')

        for j in range(times):
            self.dut.log.logger.info(f'====================DUT IN LOOP: {j + 1}====================')
            print(f'{self.port}   当前Loop为{j + 1}')
            for cmd in loop_command:
                if cmd in wait_command:
                    if self.dut.write_cmd(cmd, delay=wait_command.get(cmd, 0.5)):
                        break
                else:
                    if self.dut.write_cmd(cmd, delay=0.5):
                        break
                yield self.dut.read_with_logging()

                current_time = time.time()

                elapsed_time = current_time - self.startTime

                if elapsed_time >= 72 * 3600:  # 如果已经过去的时间超过72小时（秒）
                    # TODO
                    # 
                    # Cmd = 0x20

                    # 发送：
                    # 55 AA + 长度位 + 命令位 + 参数位 + CRC8
                    # 55 AA 04 20 [ch] [value] CRC8

                    # 参数：
                    # ch：表示哪一路，值0x01 – 0x04，
                    # value：表示新的状态，0x00-关；0x01-开
                    # 
                    # hex_code = "55AA04200100CRC8"

                    # 返回：55 AA 03 [错误码] CRC8 

                    # byte_code = bytes.fromhex(hex_code) 
                    break
                    # byte_data = bytes.fromhex(data.replace(' ', ''))
                    # voltage_bytes = byte_data[3:5]  
                    # voltage = int.from_bytes(voltage_bytes, byteorder='little')
                    # voltage_mV = voltage * 10 

                # if "batman data" in cmd:
                #     if res:
                #         soc_str = int(re.search(r"UISOC:(\d+)%",res).group(1))
                #         if soc_str > 90:

                #     else:
                #         pass
                self.dut.log.logger.info('')

        self.dut.log.logger.info('====================DUT IN POST====================')
        print(f'{self.port}    POST 测试开始')
        for cmd in post_command:
            if cmd in wait_command:
                if self.dut.write_cmd(cmd, delay=wait_command.get(cmd, 0)):
                    break
            else:
                if self.dut.write_cmd(cmd, delay=0.5):
                    break
            data = self.dut.read_with_logging()
            if bool(data) is False:
                self.dut.log.logger.info(cmd)
            yield data
            self.dut.log.logger.info('')

    def start(self):
        s = self.send_command(20)
        for val in s:
            if 'ft:fail link not available' in val and 'left' in val:
                print(f'\033[1;31m {self.port} left bud 连接不上\033[0m')
                s.close()
            if 'ft:fail link not available' in val and 'right' in val:
                print(f'\033[1;31m {self.port} right bud 连接不上\033[0m')
                s.close()
            if 'Device not configured' in val:
                print(f'\033[1;31m {self.port}已断开连接\033[0m')
                s.close()
            # print(val)


def main(p):
    threads = []
    ports = get_port_name_from_location_id(p)

    for ser in ports:
        print("Port Name:", ser)
        t = threading.Thread(target=startProcess, args=(ser,))
        print(t)
        threads.append(t)
        t.start()
def startProcess(p):
    loop_test = LoopTest(p)
    loop_test.start()




if __name__ == '__main__':
    # ser_ports =
    # for p in ports:
    p = "/dev/tty.usbmodemH36_H37_211"
    t = multiprocessing.Process(target=main, args=(p,))
    t.start()
    #     
