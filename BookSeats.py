# /usr/bin/python3
# -*- codeing = utf-8 -*-
# @Time : 2020/11/2 10:52
# @Author : MOTR
# @File : BS.py
# @Software : PyCharm
import time
import requests


def login():
    url = f'{baseUrl}bundle'
    data = f'account={account}&password={psw}&weChat=&linkSign=currentBook&type=currentBook&msg='
    response = s.post(url, data)
    time.sleep(2)
    if 'true' in response.text:
        print('登陆成功！')
    else:
        print(f'登陆失败，原因：\n{response.text}')


def bookSeat():
    while True:
        Time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        if Time == '22:45:00' or Time == '22:45:01':
            url = f'{baseUrl}saveBook?seatId={seatID}&date={Date}&start={beginTime}&end={endTime}&type=1&captchaToken='
            time.sleep(bookTime)
            response = s.get(url)
            print(response.text)
            if 'success' in response.text:
                print('座位预约成功！')
            else:
                print(f'座位预约失败！{response.text}')
            break
        else:
            print('等待...')
            time.sleep(1)


if __name__ == '__main__':
    baseUrl = 'https://system.lib.whu.edu.cn/libseat-wechat/'
    s = requests.session()
    account = ''  # 填学号
    psw = ''  # 填图书馆密码
    seatID = '54774'  # 填座位号
    beginTime = 480
    endTime = 1320
    bookTime = 0.5
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123b) NetType/WIFI Language/ja',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    login()
    Date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    bookSeat()

