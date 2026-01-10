from tkinter import Label, Button, Text, Tk, LEFT, RIGHT
from tkinter import Frame
import platform
import socket
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import threading
from datetime import datetime
import random
import hashlib

# 服务器端

# GUI界面就是两部分，第一部分就是写界面，就是一大堆self.代码那个    第二个部分就是写功能函数。
class SocketGUI:
    # event = threading.Event()
    def __init__(self, root):
        self.root = root
        self.root.title("Socket GUI6_1")
        self.root.geometry("700x700")  # 设置窗口大小固定为 900x700
        self.event = threading.Event()

        # 创建顶部面板
        self.top_panel = tk.Frame(root)
        self.top_panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # 设置填充和边距

        # 添加 IP 地址标签和文本框，    这是两个标签
        self.label_ip = Label(self.top_panel, text="IP地址：")
        self.label_ip.pack(side=tk.LEFT, padx=5)
        self.label_ip2 = Label(self.top_panel, text=" VOID ")
        self.label_ip2.pack(side=tk.LEFT, padx=5)
        # self.textfield_ip = Text(self.top_panel, height=1, width=20)
        # self.textfield_ip.pack(side=tk.LEFT)    padx参数牛逼。
        self.get_ip_button = Button(self.top_panel, text="获取本机IP地址", command=self.update_ip)
        self.get_ip_button.pack(side=tk.LEFT)
        self.get_ip_button.pack(side=tk.LEFT, padx=10)  # 调整水平间距为 10 像素
        # 添加主机名称标签和文本框，放在右侧

        self.top_panel0 = tk.Frame(root)
        self.top_panel0.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # 设置填充和边距
        self.label_name = Label(self.top_panel0, text="主机名称：")
        self.label_name.pack(side=tk.LEFT, padx=5)
        self.label_na2 = Label(self.top_panel0, text=" VOID ")
        self.label_na2.pack(side=tk.LEFT, padx=5)
        self.get_ip_button = Button(self.top_panel0, text="获取本机名称", command=self.get_hostname)
        self.get_ip_button.pack(side=tk.LEFT, padx=10)  # 调整水平间距为 10 像素
        # 添加主机名称标签和文本框，放在右侧

        self.connect_button = Button(self.top_panel, text="连接目标主机", command=self.connect_ip)
        self.connect_button.pack(side=tk.RIGHT)
        self.connect_button.pack(side=tk.RIGHT, padx=15)  # 调整水平间距为 10 像素
        # 代码位置越靠前，则越在左边
        self.entry_hostIP = Entry(self.top_panel)
        self.entry_hostIP.pack(side=tk.RIGHT, padx=5)
        # 这是处于中间位置的文本框，用于输入连接的ip地址
        self.label_hostname = Label(self.top_panel, text="客户机连接目标主机IP： ")
        self.label_hostname.pack(side=tk.RIGHT, )
        ###############

        self.top_panel1 = tk.Frame(root)
        self.top_panel1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)  # 设置填充和边距
        self.start_button = tk.Button(self.top_panel1, text="开始监听", command=self.start_listening, width=10)
        self.start_button.pack(side=tk.RIGHT, padx=15)

        # self.start_button1 = tk.Button(self.top_panel1, text="产生挑战值", command=self.generate_challenge , width=10)
        # self.start_button1.pack(side=tk.LEFT,padx = 15)
        self.challengeEntry = Entry(self.top_panel1)     # ？？？
        self.challengeEntry.pack(side=tk.LEFT, padx=10)  # Authentication
        # self.challenge
        # self.start_button2 = tk.Button(self.top_panel1, text="验证挑战值", command=self.send_challenge , width=10)
        self.start_button2 = tk.Button(self.top_panel1, text="输入密码，计算并发送响应值", command=self.password_client,width=30, state = tk.DISABLED)
        # ？？？ start_button2对于的command是password_client而不是authentication 一开始的时候禁用按钮，在发出连接请求后启动。

        self.start_button2.pack(side=tk.LEFT, padx=25)

        # self.ServerRun_button = Button(self.top_panel1, text="  服务器开机  ", command=self.RunServer)
        # # 在创建按钮时，将 command 参数设置为 self.RunServer，而不是 self.RunServer() 为什么？？？
        # self.ServerRun_button.pack(side=tk.RIGHT, padx=15)  # 调整水平间距为 15 像素

        ###############
        self.line = Frame(self.root, height=2, bd=1, relief="groove")
        self.line.pack(fill="x", padx=5, pady=5)

        # 已经使用了pack布局管理器的容器中使用grid布局管理器。pack和grid不能同时用在同一个容器上。你需要在使用grid之前确保该容器没有被其他组件使用pack管理器占用。
        self.top_panel2 = tk.Frame(root)
        self.top_panel2.pack(side=tk.RIGHT, fill=tk.Y)

        self.textfield_info1 = Text(self.top_panel2, height=20, width=25)
        self.textfield_info1.pack(side=tk.TOP, padx=5, pady=15)  # 注意是TOP不是RIGHT   padx横向间隔，pady纵向间隔.
        self.textfield_info2 = Text(self.top_panel2, height=20, width=25)
        self.textfield_info2.pack(side=tk.TOP, padx=5, pady=5)
        # info1 是服务器信息  info2是客户端信息

        ######
        self.top_panel3 = tk.Frame(root)
        self.top_panel3.pack(side=tk.LEFT, fill=tk.Y)

        self.textfield_message1 = Text(self.top_panel3, height=30, width=70)
        self.textfield_message1.pack(side=tk.TOP, padx=5, pady=15)  # 注意是TOP不是RIGHT   padx横向间隔，pady纵向间隔.
        self.textfield_message2 = Text(self.top_panel3, height=7, width=50)
        self.textfield_message2.pack(side=tk.LEFT, padx=5, pady=5)  # 左对齐
        # mess1是消息记录 mess2是发送消息

        # 第二个文本框的按钮，生成的一个容器   用tk.Frame() 在panel3里面生成的
        container_message2 = tk.Frame(self.top_panel3)
        container_message2.pack(side=tk.TOP, padx=5, pady=5, anchor='w')  # 左对齐 anchor = 'w'
        # self.button_message2 = Button(container_message2, text="发送消息", width=15 , padx= 5, command=self.send)
        # self.button_message2 = Button(container_message2, text="发送消息", width=15 , padx= 5, command=self.send)
        self.button_message2 = Button(container_message2, text="发送消息", width=15, padx=5, command=self.send,
                                      state=tk.DISABLED)

        self.button_message2.pack(side=tk.RIGHT)  # 右对齐

        self.addr = None  # 地址初始化为None

        # self.user_response1 = None
        self.user_input = None

        self.conn = None  # 初始化为None
        self.client_socket = None  # 初始化[ 一个实例变量 ]为None ,以便在整个类的方法中都可以访问它。
        self.Tempsock = None  # 临时套接字

        self.MYname = None
        self.localIP = None
        self.confirm1 = None
        self.confirm2 = None
        self.button1_clicked = None
        self.button2_clicked = None

        self.challenge_recv = None

        self.password = "lyh87311615"
        self.client_challenge = None
        # self.event = threading.Event()

    # def run_server(self):
    #     threading.Thread(target=self.RunServer).start()
    # def RunServer(self):
    #     self.textfield_info1.insert(tk.END, "服务器开机...\n")
    #
    #     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     host = '0.0.0.0'  # 允许来自任何主机的连接
    #     port = 40000
    #     server_socket.bind((host, port))
    #     server_socket.listen(1)  # 最大连接数为1
    #     self.textfield_info1.insert(tk.END, f"Server listening on {host}:{port}\n")
    #
    #     while True:
    #         conn, addr = server_socket.accept()
    #         self.textfield_info1.insert(tk.END, f"Connected by {addr}\n")
    #     # with conn:
    #     # #         print(f"Connected by {addr}")

    # IF 这里要判断一下 是否获取了本机的IP 和 主机名字
    def start_listening(self):
        if self.button1_clicked and self.button2_clicked:
            threading.Thread(target=self.listen_for_connection).start()
            self.connect_button.config(state=tk.DISABLED)
            # 使用self.connect_button.config()方法来禁用按钮，让它不能再点击。
        else:
            messagebox.showwarning("提示", "请先获取本机IP和本机主机名")

    # self.conn  self.confirm1
    def listen_for_connection(self):  # 开始监听 就是 开放连接
        # 创建服务器套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置主机和端口
        host = '0.0.0.0'  # 允许来自任何主机的连接
        port = 12345
        # 绑定主机和端口
        server_socket.bind((host, port))
        # 开始监听
        server_socket.listen(1)  # 最大连接数为1
        print(f"Server listening on {host}:{port}")
        self.textfield_info1.insert(tk.END, "开始监听...\n")
        self.textfield_info1.insert(tk.END, f"服务器正在监听： {host}:{port}\n")
        # tk.END 不能少!!
        # 等待连接
        # conn, addr = server_socket.accept()
        # print(f"Connected by {addr}")
        # 关闭服务器套接字
        # server_socket.close()

        self.conn, self.addr = server_socket.accept()  # .accept()方法返回两个参数，self.conn返回套接字，self.addr返回连接地址
        self.textfield_info1.insert(tk.END, f"接收到连接： {self.addr}")
        print(f"Connected by {self.addr}")

        # threading.Thread(target=self.receive_messages).start()  # 他妈的，之前在connect_ip()那一块忘记加了这一行代码。
        # ？？？这里做了修改

        threading.Thread(target=self.authentication).start()  # 开始身份验证阶段
        self.confirm1 = 1;  # 表示程序作为服务器运行
        # threading.Thread(target=self.name_exchange).start()
        # self.HISname = self.conn.recv(1024).decode() #建立连接后，接收对方发送给自己的主机名
        # self.conn.send(self.MYname.encode())

    # self.client_socket  self.confirm2    #IF 这里要判断一下 是否获取了本机的IP 和 主机名字
    def connect_ip(self):
        # ip_address = self.entry_hostIP.get()
        if self.entry_hostIP.get():
            # Entry 不为空，执行相应操作
            pass
        else:
            # Entry 为空，执行其他操作或者给出提示信息
            messagebox.showwarning("提示", "输入IP不能为空")

        if self.button1_clicked and self.button2_clicked:
            self.start_button.config(state=tk.DISABLED)  # 开始监听按钮禁用，防止重复连接
            self.start_button2.config(state=tk.NORMAL)  # 验证响应启用，因为这是客户机不是服务器    # 输入密码并计算响应值
            ip_address = self.entry_hostIP.get()   #从输入框获取IP地址
            port = 12345;
            # 在这里实现连接到服务器的逻辑，使用输入的IP地址(ip_address)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_address, 12345))  # 发出连接请求。

            self.textfield_info2.insert(tk.END, "正在连接...\n")
            self.textfield_info2.insert(tk.END, f"连接到 {ip_address}:{port}\n")
            # threading.Thread(target=self.receive_messages).start()  # ？？？这里修改一下
            threading.Thread(target=self.authentication_client).start()
            # 开始身份验证阶段  ？？？  connect 之后，就开始客户端 client 的认证 authentication
            # self.event = threading.Event()

            self.confirm2 = 1;  # 表示程序作客户端运行
            # threading.Thread(target=self.name_exchange).start()
        else:
            messagebox.showwarning("提示", "请先获取本机IP和本机主机名")

        # self.client_socket.send(self.MYname.encode())  #建立连接后，向对方发送自己的主机名，.send() 和 .sendall() 方法都用于发送数据，但它们有一些不同。
        # self.HISname = self.client_socket.recv(1024).decode()

    # 客户端的认证
    # ？？？ 这里的代码还没写
    def password_client(self):
        # self.user_response1 = self.challenge.get()  # 点一次发送一次响应
        self.user_input = self.challengeEntry.get()

        # challenge_str = self.client_socket.recv(1024).decode()   # ？？？这里做了修改

        # if not challenge_str:
        #     break  # 服务器关闭连接，结束循环

        # self.challenge_recv = int(challenge_str)                       # ？？？这里做了修改，这三行应该是在authentication_client里面的，删了注释之后就不会再有卡顿了。
        # print(f"Received challenge: {self.challenge_recv}")
        # self.textfield_info2.insert(tk.END, f"\n收到挑战challenge :{self.challenge_recv}\n")

        # 好煞笔，之前才发现，我现时定义了self.challenge 是一个Entry,后面又定义了self.challenge = None
        # threading.Thread(target=self.authentication_client).start()  # 开始身份验证阶段 这段代码放在这会出错
        print(f"your input: {self.user_input}")

        if self.user_input != None:
            user_response = hashlib.sha256((self.user_input + str(self.challenge_recv)).encode()).hexdigest()
        else:
            user_response = 'new'   # ？？？瞎填了个
        pass

        print("\n")
        print(self.challenge_recv)      # ？？？ 测试用的代码
        print(user_response)

        self.client_socket.send(user_response.encode())

    # 线程运行到步骤A，则暂停，当按下按钮，则继续运行。运行到最后判断if(条件B)，若条件B为真，则退出循环，否则继续循环。
    # Event对象允许线程之间进行信号通信，一个线程可以等待另一个线程发送信号。
    def authentication_client(self):
        while True:
            # 接收服务器发来的挑战
            challenge_str = self.client_socket.recv(1024).decode()
            # if not challenge_str:
            #     break  # 服务器关闭连接，结束循环

            challenge = int(challenge_str)
            print(f"Received challenge: {challenge}")

            self.challenge_recv = int(challenge_str)
            # ？？？ 少了这一行代码，那么当test6_1做客户端即使输入了正确的password，也会认证失败，因为在Line254中，self.challenge_recv是None

            self.textfield_info2.insert(tk.END, f"\n收到挑战challenge :{challenge}\n")
            # 用户手动输入响应
            # 客户机和服务器用的都是sha256哈希算法
            # user_response1 = input("Enter the correct password: ")  #从输入框输入密码
            # self.user_response1 = self.challenge.get()  # 点一次发送一次响应

            # self.event.wait()  # 等待Event对象被设置
            # self.event.clear()  # 清除Event对象，以便下次等待

            # user_response = hashlib.sha256((self.user_response1 + str(challenge)).encode()).hexdigest()  # ？？？修改了
            # user_response = hashlib.sha256((self.user_input + str(challenge)).encode()).hexdigest()  # ？？？修改了
            ###
            ###
            # self.client_socket.sendall(user_response.encode()) # 这里注释掉了
            # 接收服务器对响应的验证结果
            server_response = self.client_socket.recv(1024).decode()
            if server_response == "Authentication success. 身份认证成功":  # 回应信息该显示在何处？
                print(server_response)
                print("Yes")
                self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证成功\n")
                # self.start_button.config(state=tk.NORMAL)  # 启用信息发送按钮 tk.NORMAL !!!
                self.button_message2.config(state=tk.NORMAL)  # button_message2才是真正的发送信息按钮

                break  # 输入正确，结束循环
                # threading.challenge_listen.close
            else:
                self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证失败\n")
                # self.textfield_info2.insert("Authentication success. 身份认证成功")
        # client_socket.close()
        pass
    #     这是一个生成随机数方法，返回一个随机数值到成员变量名为self.client_challenge

    # self.textfield_message1.insert(tk.END, f"\n[  Him  ]:        \n{message}\n")

    # Traceback是报错时候，从大的地方，细分到到小的地方报错
    # 这里的client_socket是直到connect_ip函数被调用，才会被创建变量，
    # 所以报错AttributeError: 'SocketGUI' object has no attribute 'client_socket'

    # 服务器端的认证  这里似乎不需要用到信号灯
    def authentication(self):
        # 产生随机挑战值
        while True:
            # 生成随机数作为挑战
            # challenge = self.generate_challenge()
            challenge = random.randint(1, 9999)  # ？？？ None  不使用self.generate_challenge()了，直接生成随机数，客户端就不会报错了

            self.conn.sendall(str(challenge).encode())
            expect_response = hashlib.sha256((self.password + str(challenge)).encode()).hexdigest()
            # 等待客户端响应
            received_response = self.conn.recv(1024).decode()  # 这里用的套接字是listen服务器创建的
            # while True:
            self.textfield_info1.insert(tk.END, f"\n收到响应response :{received_response}\n")

            if received_response == expect_response:
                print("Authentication success.")
                self.conn.sendall("Authentication success. 身份认证成功".encode())        # ？？？发送
                self.textfield_info1.insert(tk.END, "\nAuthentication success. 对方身份认证成功\n")
                # self.start_button.config(state=tk.NORMAL)  # 启用信息发送按钮 !!!!
                self.button_message2.config(state=tk.NORMAL)  # button_message2才是真正的发送信息按钮

                threading.Thread(target=self.receive_messages).start()  # ？？？
                # server_socket.close()
                #####
                break  # 输入正确，结束循环
            else:
                print("Authentication failed.")
                # self.conn.sendall("Authentication failed. 身份认证失败".encode())
                self.conn.sendall("Authentication failed. 身份认证失败".encode())    # ？？？ 要是删了这行，客户机会出现奇怪的结果。找了好久才发现这一行没有，我也不知道为什么上面这行会被注释
                self.textfield_info1.insert(tk.END, "\nAuthentication failed. 对方身份认证失败\n")

    # def challenge_listen(self):
    #     text = challenge.receive
    #     self.cha = text.get()
    #
    #     while True:
    #         # 接收服务器发来的挑战
    #         challenge_str = self.client_socket.recv(1024).decode()
    #         # if not challenge_str:
    #         #     break  # 服务器关闭连接，结束循环
    #
    #         challenge = int(challenge_str)
    #         print(f"Received challenge: {challenge}")
    #         self.textfield_info2.insert(tk.END, f"\n收到挑战challenge :{challenge}\n")
    #         # 用户手动输入响应
    #         # 客户机和服务器用的都是sha256哈希算法
    #         # user_response1 = input("Enter the correct password: ")  #从输入框输入密码
    #         user_response1 = self.challenge.get()  # 点一次发送一次响应
    #         user_response = hashlib.sha256((user_response1 + str(challenge)).encode()).hexdigest()
    #         ###
    #         ###
    #         self.client_socket.sendall(user_response.encode())
    #         # 接收服务器对响应的验证结果
    #         server_response = self.client_socket.recv(1024).decode()
    #         if server_response == "Authentication success. 身份认证成功":  # 回应信息该显示在何处？
    #             print(server_response)
    #             print("Yes")
    #             self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证成功\n")
    #             self.start_button.config(state=tk.NORMAL)  # 启用信息发送按钮
    #             break  # 输入正确，结束循环
    #             # threading.challenge_listen.close
    #         else:
    #             self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证失败\n")
    #             # self.textfield_info2.insert("Authentication success. 身份认证成功")
    #     # client_socket.close()
        pass

    def generate_challenge(self):
        self.client_challenge = random.randint(1, 9999)
        return self.client_challenge
    ########################################
    def get_hostname(self):
        self.MYname = socket.gethostname()
        self.label_na2.config(text=f"{self.MYname}")
        self.button1_clicked = True

    def update_ip(self):
        label_ip2 = self.get_local_ip()
        self.label_ip2.config(text=label_ip2)
        self.localIP = label_ip2
        self.button2_clicked = True

    def get_local_ip(self):
        try:
            # 创建一个UDP套接字
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(("8.8.8.8", 80))  # 连接到一个公共的IP地址，如Google的DNS服务器
            local_ip2 = temp_socket.getsockname()[0]  # 获取本地IP地址
            temp_socket.close()
            return local_ip2
        except socket.error:
            return "Unable to get local IP"

    ########################################
    # self.conn和self.client_socket中有一个是None，有一个是非空的，把非空的赋值给self.Tempsock
    def receive_messages(self):
        # if self.confirm1 == 1:
        #     self.Tempsock = self.conn
        # if self.confirm2 == 1:
        #     self.Tempsock = self.client_socket
        if self.conn is not None:
            self.Tempsock = self.conn
        elif self.client_socket is not None:
            self.Tempsock = self.client_socket
        while True:
            try:
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # self.textfield_info1.insert(tk.END, f"\n[ Client ]:        {current_time}\n{message}\n")
                message = self.Tempsock.recv(1024).decode()  # client_socket是之前创建的套接字，用于传递消息。
                # self.textfield_message1.insert(tk.END, f"\n[ {self.HISname}_1 ]:        \n{message}\n")
                self.textfield_message1.insert(tk.END, f"\n[  Him  ]:        \n{message}\n")
                # 获取主机名称？
                # connect_to_server方法连接到服务器并启动一个循环，该循环接收来自服务器的消息并将其显示在文本框中。
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send(self):  # message2是发送消息框
        # if self.confirm1 == 1:
        #     self.Tempsock = self.conn
        # if self.confirm2 == 1:
        #     self.Tempsock = self.client_socket
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.conn is not None:
            self.Tempsock = self.conn
        elif self.client_socket is not None:
            self.Tempsock = self.client_socket

        message1 = self.textfield_message2.get("1.0", END)  # 获取消息内容,END是一个参数,from tkinter import *
        message = f"{self.localIP}\t\t{self.MYname}\t\tTime: {self.current_time}\n {message1}"
        self.textfield_message2.delete("1.0", END)  # 清空消息输入框
        try:
            # self.conn.send(message.encode())  # 发送消息给客户端
            # 两边时间不一样，时间戳协议？？
            # 在许多情况下，时间戳是一个长整型数字，表示自1970年1月1日（称为UNIX纪元）以来的秒数或毫秒数。这种表示方式被称为UNIX时间戳或UNIX时间。
            # 例如，当前时间的UNIX时间戳可能是类似于1616490146这样的数字。
            # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.Tempsock.send(message.encode())
            # 在之前的代码里面self.client_socket = None
            # self.text_message1.insert(tk.END, f"\n[ Server ]:        {current_time}\n{message}\n")  # 在消息记录框中显示发送的消息
            # self.textfield_message1.insert(tk.END, f"\n[ {self.MYname}_1 ]:        \n{message}\n")
            self.textfield_message1.insert(tk.END, f"\n[ You ]:        \n{message}\n")
            # self.textfield_message1.insert(tk.END, f" \n{message}\n")
        except Exception as e:
            print("Error sending message:", e)
            self.textfield_message1.insert(tk.END, "Error sending message\n")

    def generate_challenge(self):
        pass

    def send_challenge(self):
        pass


if __name__ == "__main__":
    root = Tk()
    app = SocketGUI(root)
    root.mainloop()

#
# 在GUI应用程序中，当你执行一些耗时操作（例如创建网络套接字并监听连接）时，如果在主线程中执行，可能会导致界面卡死或没有响应。这是因为主线程被阻塞，无法处理用户交互或刷新界面。
# 为了避免这种情况，你可以使用多线程或异步操作来执行耗时任务，以确保主线程保持响应性。在这种情况下，你可以将服务器的启动过程放在一个单独的线程中进行，这样就不会阻塞主线程。
# 下面是一个示例，展示了如何在Python的tkinter应用程序中使用多线程启动服务器：