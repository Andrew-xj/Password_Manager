#!python3 - init.py
# -*- coding:utf-8 -*-
# Author: Andrew-xj

import time
import base64


def identify():
	# 判断是否为初次使用
    try:
        with open(r'.\other\identify.txt', 'r', encoding='utf-8') as f:
            word = f.read()
			# 解密
            word = str(base64.b64decode(word[1:]).decode())
            password = input("请输入验证密码：")
			# 验证密码
            if word != password:
                exit("验证失败，无法访问，程序已退出！")
            else:
                print("验证成功！")
    except FileNotFoundError:
        password = input("首次运行，请自行设置验证密码：")
		# 加密
        password = str(base64.b64encode(password.encode()))
		# 存储密码
        with open(r'.\other\identify.txt', 'w', encoding='utf-8') as f:
            f.write(password)
            print("设置成功，请务必牢记该密码，否则以后运行将无法使用密码管理器。")
            time.sleep(2)


def process_data(data):
    n_data = {}    # 用于存储账户信息
    data = data.split('\\n')
    del data[-1]
    for line in data:
        line = line.split(',')
		# 解密
        key = base64.b64decode(line[0][1:]).decode()
        username = base64.b64decode(line[1][1:]).decode()
        password = base64.b64decode(line[2][1:]).decode()
		# 保存
        n_data[str(key)] = {'username': str(username),
                            'password': str(password)}
    return n_data


def init():
	# 验证身份
    identify()
	# 读取数据
    with open(r'.\other\data.csv', 'r', encoding="utf-8") as f:
        data = f.read()    # data格式：平台,账号,密码\n
    if data == '':
        return {}
    else:
		# 字符串转为字典
        data = process_data(data)
    return data
