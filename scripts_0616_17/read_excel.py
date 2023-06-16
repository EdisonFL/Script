from openpyxl import load_workbook
import os
base_path = '/Users/RELTEST/command'


def search_file(path):
    folders = [file for file in os.listdir(path) if file != '.DS_Store']
    for index, file in enumerate(folders):
        print(f'{index}\t{file}')
    choice = input('请选择配置文件选项：')
    try:
        c = int(choice)
    except IndexError as e:
        raise IndexError('输入的值超出了选项范围')
    except ValueError as e:
        raise ValueError('输入的类型有误')
    else:
        new_path = os.path.join(path, folders[c])
        if os.path.isdir(new_path):
            return search_file(new_path)
        else:
            return new_path


print(search_file(base_path))
