import glob
import re
import sys
import time

import serial


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


port = get_port('/dev/cu.usbmode*')
device = serial.Serial(port=port, baudrate=230400, timeout=0.1)


def write_cmd(dut, cmd, delay=0.5, is_return=True):
    cmd = f'{cmd}\n'.encode('utf-8', errors='ignore')
    dut.write(cmd)
    if delay:
        time.sleep(delay)
    if is_return:
        return read_data(dut)


def read_data(dut):
    msg = ''
    while True:
        line = dut.readline().decode('utf-8', errors='ignore')
        if line.strip():
            msg += f'{line.strip()}\n'
        else:
            break
    return msg


# 获取case的SN
case_sn = re.findall(r'SrNm: "(\w+)"', write_cmd(device, 'syscfg print SrNm'))[0]
print(f'case SN: {case_sn}')
# case进行reset
# write_cmd(device, 'ft reset', delay=5, is_return=False)
# del device
# device = serial.Serial(port=port, baudrate=230400, timeout=0.1)

print(write_cmd(device, 'bud state both disable'))
print(write_cmd(device, 'buckboost enable out'))
print(write_cmd(device, 'locust_mgr pp left enable'))
# 打开左耳通道
print(write_cmd(device, 'ft tunnel open left finite', delay=2))
# 获取左耳的SN
left_sn = re.findall(r'syscfg:ok "(\w+)"', write_cmd(device, 'syscfg print SrNm'))[0]
if left_sn != case_sn:
    print('\033[0;32m left bud tunnel open ok!\033[0m')
print(write_cmd(device, 'ft reset', delay=20))
print('\033[0;32m left bud reset ok!\033[0m')

# 打开右耳通道
print(write_cmd(device, 'locust_mgr pp right enable'))
# 打开右耳通道
print(write_cmd(device, 'ft tunnel open right finite', delay=2))
# 获取右耳的SN
right_sn = re.findall(r'syscfg:ok "(\w+)"', write_cmd(device, 'syscfg print SrNm'))[0]
if right_sn != case_sn and right_sn != left_sn:
    print('\033[0;32m right bud tunnel open ok!\033[0m')
print(write_cmd(device, 'ft reset', delay=20))
print('\033[0;32m right bud reset ok!\033[0m')
