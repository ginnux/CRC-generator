from tkinter import *
from tkinter import messagebox

msg0 = '请输入数据与生成多项式!'


def crc(data, poly):
    # 去掉前缀0b，求解数据与余数的二进制长度
    data_len = len(bin(data)) - 2
    remainder_len = len(bin(poly)) - 3
    # 数据左移补零，低位储存余数
    data = data << remainder_len
    # 模拟手工除法，检测数据最高位是否为1，为1则与余数对齐进行异或运算，随后右移余数进行下一位的计算，直至数据不足以被除，此时数据即为余数
    for i in range(data_len):
        if (data >> data_len + remainder_len - 1 - i) == 1:
            data = data ^ (poly << data_len - 1 - i)

    return data, remainder_len


def safe_bin_string(str):
    if len(str) == 0:
        return False
    # 检测字符串是否为正确的二进制表示字符串
    for char in str:
        if char != '0' and char != '1':
            return False
    return True


def eval_bin_str(str):
    return int(str, 2)


def safe_hex_string(str):
    if len(str) == 0:
        return False
    # 检测字符串是否为正确的十六进制表示字符串
    for char in str:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c',
                        'd', 'e', 'f']:
            return False
    return True


def eval_hex_str(str):
    return int(str, 16)


def bin_crc():
    # 读取输入框输入的原始数据
    data = entry_data.get()
    # 根据选择的工作模式判断生成多项式选取自定义输入的还是预设的
    if mode.get() == 0:
        poly = entry_poly.get()
    elif mode.get() == 1:
        poly = '1101'
        entry_poly.delete(0, END)
        entry_poly.insert(0, '1101')
    elif mode.get() == 2:
        poly = '11000000000000101'
        entry_poly.delete(0, END)
        entry_poly.insert(0, '11000000000000101')
    # 检查字符串是否符合输入规范
    if safe_bin_string(data) == 1 and safe_bin_string(poly) == 1:
        # 将字符串转化为整数
        data_int = eval_bin_str(data)
        poly_int = eval_bin_str(poly)
        # 计算CRC校验码
        out, remainder_len = crc(data_int, poly_int)
        # 截取二进制码
        msg = bin(out)[2:]
        # 将高位的0补全
        for i in range(max(remainder_len - len(msg), 0)):
            msg = '0' + msg
        msg = '0b' + msg
        # 输出
        output.delete('1.0', END)
        output.insert('1.0', msg)
    else:
        msg = '请确认输入的值为正确的二进制数'
        output.delete('1.0', END)
        output.insert('1.0', msg)
    return


def hex_crc():
    # 读取输入框输入的原始数据
    data = entry_data.get()
    # 根据选择的工作模式判断生成多项式选取自定义输入的还是预设的
    if mode.get() == 0:
        poly = entry_poly.get()
    elif mode.get() == 1:
        poly = 'D'
        entry_poly.delete(0, END)
        entry_poly.insert(0, 'D')
    elif mode.get() == 2:
        poly = '18005'
        entry_poly.delete(0, END)
        entry_poly.insert(0, '18005')
    # 检查字符串是否符合输入规范
    if safe_hex_string(data) == 1 and safe_hex_string(poly) == 1:
        # 将字符串转化为整数
        data_int = eval_hex_str(data)
        poly_int = eval_hex_str(poly)
        # 计算CRC校验码
        out, remainder_len = crc(data_int, poly_int)
        # 截取二进制码
        msg = bin(out)[2:]
        # 将高位的0补全
        msg_len = len(msg)
        if remainder_len - msg_len >= 4:
            msg = hex(int(msg, 2))[2:]
            for i in range(int((remainder_len - msg_len) / 4)):
                msg = '0' + msg
            msg = '0x' + msg
        else:
            msg = hex(int(msg, 2))
        # 输出
        msg = '0x' + msg.upper()[2:]
        output.delete('1.0', END)
        output.insert('1.0', msg)
    else:
        msg = '请确认输入的值为正确的十六进制数'
        output.delete('1.0', END)
        output.insert('1.0', msg)
    return


# 创建窗口：实例化一个窗口对象。
root = Tk()

# 窗口大小
width = 600
height = 372
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int(screen_width / 2 - width / 2)
y = int(screen_height / 2 - height / 2)
size = '{}x{}+{}+{}'.format(width, height, x, y)
root.geometry(size)

#  窗口标题
root.title("CRC校验码生成")

# 添加标签控件
label_title = Label(root, text="CRC校验码生成", font=("黑体", 24))
# 定位
label_title.grid(row=0, column=0, columnspan=3, padx=(10, 0), pady=(10, 0), sticky='news')

# 添加标签控件
label_data = Label(root, text="原始数据：", font=("宋体", 12))
# 定位
label_data.grid(row=1, column=0, padx=(10, 0), pady=10, sticky='E')

# 添加输入框
entry_data = Entry(root, font=("宋体", 12), width=40)
entry_data.grid(row=1, column=1, columnspan=2, padx=(0, 10), ipadx=60, sticky=E)

# 添加标签控件
label_poly = Label(root, text="完整生成多项式：", font=("宋体", 12))
# 定位
label_poly.grid(row=2, column=0, padx=(10, 0), pady=10)

# 添加输入框
entry_poly = Entry(root, font=("宋体", 12), width=40)
entry_poly.grid(row=2, column=1, columnspan=2, padx=(0, 10), ipadx=60, sticky=E)

# 添加标签控件
label_output = Label(root, text="CRC校验码结果：", font=("宋体", 12))
# 定位
label_output.grid(row=3, column=0, padx=(10, 0), pady=10, sticky=E)

# 添加输入框
output = Text(root, height=1, width=40, font=("宋体", 12))
output.grid(row=3, column=1, columnspan=2, padx=(0, 10), ipadx=60)
output.insert('1.0', msg0)

# IntVar() 用于处理整数类型的变量
mode = IntVar()
# 根据单选按钮的 value 值来选择相应的选项
mode.set(0)
# 使用 variable 参数来关联 IntVar() 的变量
Radiobutton(root, text="以自定义的生成多项式运行", variable=mode, value=0).grid(row=4, column=1, columnspan=2, sticky=W,
                                                                              padx=(58, 5), pady=(5, 5))
Radiobutton(root, text="以预设：G(x)=x³+x²+1运行", variable=mode, value=1).grid(row=5, column=1, columnspan=2, sticky=W,
                                                                               padx=(58, 5), pady=(5, 5))
Radiobutton(root, text="以预设：G(x)=x¹⁶+x¹⁵+x²+1运行", variable=mode, value=2).grid(row=6, column=1, columnspan=2,
                                                                                    sticky=W, padx=(58, 5), pady=(5, 5))

# 添加点击按钮
but1 = Button(root, text="以二进制运行", command=bin_crc)
but1.grid(row=7, column=0, columnspan=3, sticky='news', padx=(10, 10), pady=(5, 5))
but2 = Button(root, text="以十六进制运行", command=hex_crc)
but2.grid(row=8, column=0, columnspan=3, sticky='news', padx=(10, 10), pady=(5, 10))

root.resizable(False, False)

# 显示窗口
root.mainloop()
