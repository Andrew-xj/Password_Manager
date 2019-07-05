#!python3 - gui.py
# -*- coding:utf-8 -*-
# Author: Andrew-xj

import tkinter as tk
import tkinter.messagebox as tm
import pyperclip as pc
import base64


# 新增一条数据

def f_stop(tl):
	# 关闭窗口
    tl.destroy()


def f_yes(p, u, pw, data, tl):
    # 更新数据
    data[str(p)] = {"username": str(u),
                    "password": str(pw)}
	# 弹窗提示
    tm.showinfo(title="提示", message="更新成功！")
	# 关闭窗口
    f_stop(tl)


def f_add(data):
	# 新建子窗口
    add_w = tk.Toplevel()
    add_w.title("增加账户")
    add_w.geometry("400x400")
	# 设置输入框变量
    p, u, pw = tk.Variable(), tk.Variable(), tk.Variable()
	# 提示标签
    l1 = tk.Label(add_w,
                  text="账户平台:\n\n输入账号:\n\n输入密码:",
                  width=10,
                  height=10)
    l1.place(x=5, y=50)
	# 3个输入框
    platform = tk.Entry(add_w,
                        textvariable=p,
                        width=40)
    platform.place(x=90, y=93)
    username = tk.Entry(add_w,
                        textvariable=u,
                        width=40)
    username.place(x=90, y=127)
    password = tk.Entry(add_w,
                        textvariable=pw,
                        width=40)
    password.place(x=90, y=161)
	# 确定按钮
    yes = tk.Button(add_w,
                    text="确定",
                    command=lambda: f_yes(p.get(), u.get(), pw.get(), data, add_w),
                    width=10, height=3,
                    anchor="center")
    yes.place(x=60, y=250)
	# 退出按钮
    stop = tk.Button(add_w,
                     text="关闭",
                     command=lambda: f_stop(add_w),
                     width=10, height=3,
                     anchor="center")
    stop.place(x=260, y=250)


# 查询已有数据的密码

def lookup(p, datum):
	# 复制到剪贴板
    pc.copy(datum["password"])
	# 提示信息
    tm.showinfo(title="提示",
                message="已成功复制"+p+"的密码到剪贴板！")


def f_lookup(data):
	# 新建子窗口
    lookup_w = tk.Toplevel()
    lookup_w.geometry("400x400")
    lookup_w.title("查询密码")
	# 渲染按钮：一行4个，逐行增加
    i, j = 0, 0
    for each in data.keys():
        btn = tk.Button(lookup_w,
                        text=each,
                        width=12, height=2,
                        anchor="center",
                        wraplength=80,
                        command=lambda: lookup(each, data[each]))
        btn.place(x=10+100*i, y=10+j*60)
        if i == 3:
            j += 1
            i = 0
        else:
            i += 1


# 删除已有数据

def delete(p, data, tl):
	# 删除确认
    if tm.askyesno(title="删除账户", message="是否确定删除账户？"):
		# 删除数据
        del data[str(p)]
		# 删除成功提示
        tm.showinfo(title="提示", message="删除成功！")
		# 关闭窗口
        f_stop(tl)


def f_delete(data):
	# 新建子窗口
    delete_w = tk.Toplevel()
    delete_w.geometry("400x400")
    delete_w.title("删除账户")
	# 渲染按钮：一行4个，逐行增加
    i, j = 0, 0
    for each in data.keys():
        btn = tk.Button(delete_w,
                        text=each,
                        width=12, height=2,
                        anchor="center",
                        wraplength=80,
                        command=lambda: delete(each, data, delete_w))
        btn.place(x=10+100*i, y=10+j*60)
        if i == 3:
            j += 1
            i = 0
        else:
            i += 1


def main_window(root, data):
    # 提示文字
    text = tk.Label(root,
                    text='记住密码就是这么简单！',
                    fg="red", bg="white",
                    font=("楷体", 20),
                    width=25, height=5,
                    anchor="center")
    text.place(x=22, y=50)
    # 选择按钮：3个
    add = tk.Button(root,
                    text="增加账户",
                    command=lambda: f_add(data),
                    width=10, height=3,
                    anchor="center")
    lookup = tk.Button(root,
                       text="查询密码",
                       command=lambda: f_lookup(data),
                       width=10, height=3,
                       anchor="center")
    delete = tk.Button(root,
                       text="删除账户",
                       command=lambda: f_delete(data),
                       width=10, height=3,
                       anchor='center')
	# 渲染按钮
    add.place(x=20, y=250)
    lookup.place(x=160, y=250)
    delete.place(x=300, y=250)


def close(data, root):
	# 重新写入数据
    with open(r'.\other\data.csv', 'w+', encoding="utf-8") as f:
        f.truncate()
        for key in data.keys():
			# 加密
            username = base64.b64encode(data[key]['username'].encode())
            password = base64.b64encode(data[key]['password'].encode())
            key = base64.b64encode(key.encode())
			# 写入
            f.write('{0},{1},{2}\\n'.format(key, username, password))
	# 关闭主窗口
    root.destroy()


def gui(data):
    # 创建主窗口
    root = tk.Tk()
    # 设置标题
    root.title('密码管理器')
    # 设置大小和位置
    root.geometry("400x400")
    # 渲染交互界面
    main_window(root, data)
    # 监听退出主窗口
    root.protocol("WM_DELETE_WINDOW", lambda: close(data, root))
    root.mainloop()
