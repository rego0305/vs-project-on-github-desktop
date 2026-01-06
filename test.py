#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pip install requests
填入自己的 KEY 即可用：python weather.py 北京
"""
import sys, requests, json
# pip install requests
# API_KEY = "YOUR_KEY_HERE"          # 到 https://openweathermap.org/ 免费注册拿 key

API_KEY = "北京"          # 到 https://openweathermap.org/ 免费注册拿 key
URL = "https://api.openweathermap.org/data/2.5/weather"

def weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "zh_cn"}
    try:
        r = requests.get(URL, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        print(f"{city} 当前气温：{temp}℃ ，天气：{desc}")
    except requests.exceptions.RequestException as e:
        print("网络请求出错：", e)
    except (KeyError, IndexError):
        print("未找到该城市，请检查拼写！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python weather.py 城市名")
    else:
        weather(" ".join(sys.argv[1:]))


# 完全可以在 PyCharm 里跑，而且更方便——只需要把「运行参数」填好就行，步骤如下：
#
# 1. 新建/打开项目
#    把 `weather.py` 拖进项目根目录。
#
# 2. 装依赖
#    右下角状态栏点 「Python Packages」→ 搜索 `requests` → Install；或者
#    在 PyCharm 自带的 Terminal 里敲 `pip install requests` 也行。
#
# 3. 告诉 PyCharm 要传什么参数
#    右上角「当前脚本」小三角旁边 → 下拉选 Edit Configurations…
#    - Script path: 选中你的 `weather.py`
#    - Parameters: 填城市名，比如 `北京`（想查多个就填 `Shanghai` 或 `New York`）
#    - OK 保存。
#
# 4. 运行
#    直接点绿色 ▶ 按钮，Run 窗口里就会输出：
#    ```
#    北京 当前气温：28℃ ，天气：晴
#    ```
#
# 以后换城市只需改一下 Parameters 再点 ▶ 即可，根本不用离开 PyCharm。



# pycharm最顶部的第一横栏是什么
# 第一横栏就是「主菜单栏」（Menu Bar），从左到右依次是：
# File  Edit  View  Navigate  Code  Refactor  Run  Tools  VCS  Window  Help
# 它纯粹是文字菜单，没有任何图标；下面那排带图标的才叫「工具栏」。
# 要找 Edit Configurations… 得去工具栏（第二横栏）绿色 ▶ 左边的下拉框，或者直接在主菜单里点 Run → Edit Configurations…。


# 然后呢，parameters在哪
# 把「Edit Configurations…」点开后，会弹出一个标题为 Run/Debug Configurations 的窗口。
# 在这个窗口里找参数区域，分两步：
# 左侧栏确认选中的是你的脚本（名字通常是 weather 或 Python）。
# 右侧主面板里往下瞄一眼，会看到两行：
# Script path:（已经填好 weather.py）
# Parameters: 后面的输入框就是！
# 把城市名填进去，例如
# 北京
# 或带空格的城市用双引号包起来
# "Los Angeles"