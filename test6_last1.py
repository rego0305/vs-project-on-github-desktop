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
from Crypto.PublicKey import RSA

# # 最终版本代码，test6_last0当客户端，test6_last1当服务器

# GUI界面就是两部分，第一部分就是写界面，就是一大堆self.代码那个    第二个部分就是写功能函数。
class SocketGUI:
    # event = threading.Event()
    def __init__(self, root):
        self.root = root
        self.root.title("自定义协议_聊天应用程序")
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
        self.get_name_button = Button(self.top_panel0, text="获取本机名称", command=self.get_hostname)
        self.get_name_button.pack(side=tk.LEFT, padx=10)  # 调整水平间距为 10 像素
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
        self.challengeEntry = Entry(self.top_panel1)
        self.challengeEntry.pack(side=tk.LEFT, padx=10)  # Authentication
        # self.start_button2 = tk.Button(self.top_panel1, text="验证挑战值", command=self.send_challenge , width=10)
        self.start_button2 = tk.Button(self.top_panel1, text="输入口令密码，计算响应值并发送之", command=self.password_client,
                                       width=30, state=tk.DISABLED)  # 一开始的时候禁用按钮，在发出连接请求后启动。
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
        self.button_send = Button(container_message2, text="发送消息", width=15, padx=5, command=self.send,
                                      state=tk.DISABLED)

        self.button_send.pack(side=tk.RIGHT)  # 右对齐

        self.addr = None  # 地址初始化为None
        self.user_response1 = None

        self.conn = None  # 初始化为None
        self.client_socket = None  # 初始化[ 一个实例变量 ]为None ,以便在整个类的方法中都可以访问它。
        self.Tempsock = None  # 临时套接字

        self.MYname = None
        self.localIP = None
        self.confirm1 = None
        self.confirm2 = None
        self.button1_clicked = None
        self.button2_clicked = None

        self.password = "lyh87311615"
        self.client_challenge = None
        self.challenge_recv = None
        # self.event = threading.Event()


    # IF 这里要判断一下 是否获取了本机的IP 和 主机名字
    def start_listening(self):
        if self.button1_clicked and self.button2_clicked:
            threading.Thread(target=self.listen_for_connection).start()
            self.connect_button.config(state=tk.DISABLED)
            # 使用self.connect_button.config()方法来禁用按钮，让它不能再点击。
            # 点过一次开始监听后，就不能再点了。self.start_button.config(state=tk.DISABLED)
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
        self.textfield_info1.insert(tk.END, f"\n服务器正在监听： {host}:{port}\n")
        # tk.END 不能少!!
        # 等待连接
        # conn, addr = server_socket.accept()
        # print(f"Connected by {addr}")
        # 关闭服务器套接字
        # server_socket.close()

        self.conn, self.addr = server_socket.accept()  # .accept()方法返回两个参数，self.conn返回套接字，self.addr返回连接地址
        self.textfield_info1.insert(tk.END, f"\n接收到连接： {self.addr}\n")
        print(f"Connected by {self.addr}")
        # threading.Thread(target=self.receive_messages).start()  # 他妈的，之前在connect_ip()那一块忘记加了这一行代码。

        threading.Thread(target=self.authentication).start()  # 开始身份验证阶段
        self.confirm1 = 1;  # 表示程序作为服务器运行

        # threading.Thread(target=self.name_exchange).start()
        # self.HISname = self.conn.recv(1024).decode() #建立连接后，接收对方发送给自己的主机名
        # self.conn.send(self.MYname.encode())

    # self.client_socket  self.confirm2    #IF 这里要判断一下 是否获取了本机的IP 和 主机名字

    def authentication(self):
        # 产生随机挑战值
        while True:
            # 生成随机数作为挑战
            challenge = random.randint(1, 9999)
            self.conn.sendall(str(challenge).encode())
            expect_response = hashlib.sha256((self.password + str(challenge)).encode()).hexdigest()
            # 等待客户端响应
            received_response = self.conn.recv(1024).decode()  # 这里用的套接字是listen服务器创建的
            # while True:
            self.textfield_info1.insert(tk.END, f"\n收到响应response :{received_response}\n")

            if received_response == expect_response:
                print("Authentication success.")
                self.conn.sendall("Authentication success. 身份认证成功".encode())
                self.textfield_info1.insert(tk.END, "\nAuthentication success. 对方身份认证成功\n")
                self.button_send.config(state=tk.NORMAL)  # 启用信息发送按钮 !!!!
                # server_socket.close()
                #####
                # threading.Thread(target=self.receive_messages).start()
                threading.Thread(target=self.key_exchange).start()
                # 臭傻逼，不对！我记得之前是对的，现在毕设快交了发现这个错误
                # threading.Thread(target=self.rsa_key_generate).start()
                break  # 输入正确，结束循环

            else:
                print("Authentication failed.")
                # self.conn.sendall("Authentication failed. 身份认证失败".encode())
                self.conn.sendall("Authentication failed. 身份认证失败".encode())
                self.textfield_info1.insert(tk.END, "\nAuthentication failed. 对方身份认证失败\n")
        pass

    def connect_ip(self):
        # ip_address = self.entry_hostIP.get()
        if self.entry_hostIP.get():
            # Entry 不为空，执行相应操作
            pass
        else:
            # Entry 为空，执行其他操作或者给出提示信息
            messagebox.showwarning("提示", "输入IP不能为空")

        if self.button1_clicked and self.button2_clicked:
            self.start_button.config(state=tk.DISABLED)   #  开始监听按钮禁用，防止重复连接
            self.start_button2.config(state=tk.NORMAL)    #  验证响应启用，因为这是客户机不是服务器    # 输入密码并计算响应值
            ip_address = self.entry_hostIP.get()   #从输入框获取IP地址
            port = 12345;
            # 在这里实现连接到服务器的逻辑，使用输入的IP地址(ip_address)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_address, 12345))  # 发出连接请求。

            self.textfield_info2.insert(tk.END, "正在连接...\n")
            self.textfield_info2.insert(tk.END, f"\n连接到 {ip_address}:{port}\n")
            # threading.Thread(target=self.receive_messages).start()
            threading.Thread(target=self.authentication_client).start()  # 开始身份验证阶段
            # self.event = threading.Event()
            self.confirm2 = 1;  # 表示程序作客户端运行
            # threading.Thread(target=self.name_exchange).start()
        else:
            messagebox.showwarning("提示", "请先获取本机IP和本机主机名")
        # self.client_socket.send(self.MYname.encode())  #建立连接后，向对方发送自己的主机名，.send() 和 .sendall() 方法都用于发送数据，但它们有一些不同。
        # self.HISname = self.client_socket.recv(1024).decode()

    # 客户端的认证
    def password_client(self):
        # self.user_response1 = self.challenge.get()
        # 点一次发送一次响应
        # self.event.set()
        self.user_input = self.challengeEntry.get()
        # 好煞笔，之前才发现，我现时定义了self.challenge 是一个Entry,后面又定义了self.challenge = None
        # threading.Thread(target=self.authentication_client).start()  # 开始身份验证阶段 这段代码放在这会出错
        print(f"your input: {self.user_input}")
        if self.user_input != None:
            user_response = hashlib.sha256((self.user_input + str(self.challenge_recv) ).encode()).hexdigest()
        else:
            user_response = 'new'
        ###
        ###
        # self.client_socket.send(user_response.encode())

        # #我要是不写try:  就会报错'SocketGUI' object has no attribute 'client_socket'
        # 事实上就算写了try, 还是会在命令行报错Exception as e:

        # 本质原因是 command=self.password_client()这里错了,应该是 command=self.password_client

        self.client_socket.send(user_response.encode())
        # try:
        #     self.client_socket.send(user_response.encode())
        # except Exception as e:
        #     print("Error sending message:", e)

        # 接收服务器对响应的验证结果
        # self.event.set()

    # 线程运行到步骤A，则暂停，当按下按钮，则继续运行。运行到最后判断if(条件B)，若条件B为真，则退出循环，否则继续循环。
    # Event对象允许线程之间进行信号通信，一个线程可以等待另一个线程发送信号。
    def authentication_client(self):
        while True:
            # 接收服务器发来的挑战
            challenge_str = self.client_socket.recv(1024).decode()
            # if not challenge_str:
            #     break  # 服务器关闭连接，结束循环
            self.challenge_recv = int(challenge_str)
            print(f"Received challenge: {self.challenge_recv}")
            self.textfield_info2.insert(tk.END, f"\n收到挑战challenge :{self.challenge_recv}\n")
            # 用户手动输入响应
            # 客户机和服务器用的都是sha256哈希算法
            # user_response1 = input("Enter the correct password: ")  #从输入框输入密码
            # self.user_response1 = self.challenge.get()  # 点一次发送一次响应

            # self.event.wait()  # 等待Event对象被设置
            # self.event.clear()  # 清除Event对象，以便下次等待

            # user_response = hashlib.sha256((self.user_response1 + str(challenge)).encode()).hexdigest()
            # self.client_socket.sendall(user_response.encode())
            # 接收服务器对响应的验证结果
            # ？？？这里 self.client_socket.recv(1024).decode() 了两次
            server_response = self.client_socket.recv(1024).decode()   # 这里recv了两次

            print(f"认证结果: {server_response}")
            self.textfield_info2.insert(tk.END, f"\n认证结果: {server_response}\n")

            if server_response == "Authentication success. 身份认证成功":  # 回应信息该显示在何处？
                print(server_response)
                print("Yes")
                # self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证成功\n")
                self.button_send.config(state=tk.NORMAL)  # 启用信息发送按钮 tk.NORMAL !!!
                ####
                # threading.Thread(target=self.receive_messages).start()  #重要！！！
                threading.Thread(target=self.key_exchange).start()
                # threading.Thread(target=self.rsa_key_generate).start()

                break  # 输入正确，结束循环
                # threading.challenge_listen.close
            else:
                # self.textfield_info2.insert(tk.END, "\nAuthentication success. 客户端身份认证失败\n")
                print(server_response)
                # self.textfield_info2.insert("Authentication success. 身份认证成功")
        # client_socket.close()
        pass
    #     这是一个生成随机数方法，返回一个随机数值到成员变量名为self.client_challenge

    # self.textfield_message1.insert(tk.END, f"\n[  Him  ]:        \n{message}\n")

    # Traceback是报错时候，从大的地方，细分到到小的地方报错
    # 这里的client_socket是直到connect_ip函数被调用，才会被创建变量，
    # 所以报错AttributeError: 'SocketGUI' object has no attribute 'client_socket'

    # 服务器端的认证  这里似乎不需要用到信号灯
    def rsa_key_generate(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        with open("private_key8.pem", "wb") as private_file:
            private_file.write(private_key)
        with open("public_key8.pem", "wb") as public_file:
            public_file.write(public_key)
        # public_key_data = public_key.pem.read().read()是文件对象的方法，而不是属性。
        # public_key_data = public_key.read()
        self.textfield_info1.insert(tk.END, "\nRSA公钥产生完毕\n")

        threading.Thread(target=self.key_exchange).start()
        # key.publickey()和key.publickey().export_key()区别：
        # 返回类型：
        # key.publickey()返回一个Crypto.PublicKey.RSA.RsaKey对象，该对象表示RSA密钥的公钥部分。
        # key.publickey().export_key()返回公钥的字节字符串形式，可以直接保存到文件或通过网络发送。
        # 使用：
        # key.publickey()返回的对象可以直接用于加密操作，例如使用encrypt方法加密数据。
        # key.publickey().export_key()返回的字节字符串需要进一步处理，通常是保存到文件或发送给其他实体。

    def key_exchange(self):
        if self.conn is not None:
            self.Tempsock = self.conn
        elif self.client_socket is not None:
            self.Tempsock = self.client_socket
        # if confirm == 1  服务器：先send后receive

        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        with open("private_key8.pem", "wb") as private_file:
            private_file.write(private_key)
        with open("public_key8.pem", "wb") as public_file:
            public_file.write(public_key)

        if self.confirm1 == 1:
            threading.Thread(target=self.key_send).start()
            threading.Thread(target=self.key_receive).start()
            self.textfield_info1.insert(tk.END, "\nRSA公钥交换完成，开始对话\n")
            threading.Thread(target=self.receive_messages).start()
        # if confirm == 2  服务器：先receive后send
        if self.confirm2 == 1:
            threading.Thread(target=self.key_receive).start()
            threading.Thread(target=self.key_send).start()
            self.textfield_info1.insert(tk.END, "\nRSA公钥交换完成，开始对话\n")
            threading.Thread(target=self.receive_messages).start()

    def key_send(self):
        # if confirm == 1  服务器：先send后receive
        # if confirm == 2  服务器：先receive后send
        # public_key_data = RSA.import_key(self.public_file.read())
        with open("public_key8.pem", "rb") as public_file:
            my_public_key_data = RSA.import_key(public_file.read())
        # public_key_data = my_public_key_data.export_key()
        self.Tempsock.sendall(my_public_key_data.export_key())

        print("已发送公钥文件给客户端")
        self.textfield_info1.insert(tk.END, "\n已发送公钥文件给客户端：public_key8.pem\n")
        pass

    def key_receive(self):
        his_public_key_data = self.Tempsock.recv(4096)
        # 使用 import_key() 方法将接收到的数据转换为 RSA 密钥对象
        his_public_key = RSA.import_key(his_public_key_data)
        # 将 RSA 密钥对象导出为 .pem 格式的字符串
        received_pem_key = his_public_key.export_key()
        # 将 .pem 格式的字符串写入文件
        with open("received_public_key81.pem", "wb") as file:
            file.write(received_pem_key)
        # 将公钥文件内容保存到本地    1.先接收字节byte数据 2.再import  3.再export  4.将导出的.pem写入文件
        # with open("received_public_key8.pem", 'wb') as file:
        #     file.write(his_public_key_data)
        print("已接收并保存公钥文件")
        self.textfield_info1.insert(tk.END, "\n已接收并保存对方的公钥文件: received_public_key81.pem\n")
        pass

    ########################################
    def get_hostname(self):
        self.MYname = socket.gethostname()
        self.label_na2.config(text=f"{self.MYname}")
        self.button1_clicked = True     # 说明这个按钮已经按过了

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
# python生成exe命令程序： pyinstaller your_script.py 在终端输入这个命令
# 删除 _internal 文件夹可能会导致生成的可执行文件无法正确运行，或者在生成可执行文件时出现错误。
# 在test6文件夹下面有_internal文件夹和exe程序，删除_internal文件夹会导致exe就没法运行了