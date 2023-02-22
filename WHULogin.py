# -*- codeing = utf-8 -*-
# @Time : 2020/8/20 19:07
# @Author : MOTR
# @File : WHULogin.py
# @Software : PyCharm
import random
import sys
import time
import requests
from bs4 import BeautifulSoup
import re
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from urllib.parse import quote


class PwdEncrypt(object):

    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')

    def encrypt(self, data):
        cryptor = AES.new(self.key, self.mode, self.iv)
        data = data.encode('utf-8')
        data = self.pkcs7_padding(data)
        self.ciphertext = cryptor.encrypt(data)
        return base64.b64encode(self.ciphertext).decode('utf-8')

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)
        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise Exception('无效的加密信息!')
        else:
            return uppadded_data


findValue = re.compile(r'<input name="(.*?)" type="hidden" value="(.*?)"/>')
findMoocValues = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"/>')
findpwdDefaultEncryptSalt = re.compile(r'<input id="pwdDefaultEncryptSalt" type="hidden" value="(.*?)">')
findCASTGC = re.compile(r'CASTGC=(.*?);')
findiPlanetDirectoryPro = re.compile(r'iPlanetDirectoryPro=(.*?);')
findMOD_AUTH_CAS = re.compile(r'MOD_AUTH_CAS=(.*?);')
findasessionid = re.compile(r'asessionid=(.*?);')
findURL = re.compile(r'<form action="(.*?)" id="userLogin" method="post">')
findName = re.compile(r'<p class="personalName" style="text-align:center;display:block;overflow:hidden;word-break'
                      r':keep-all;white-space:nowrap;text-overflow:ellipsis;" title="(.*?)">')
findMoocCourseURL = re.compile(r'<a class="currentpage" href="javascript:switchM\(\'zne_hjhx_icon\',\'(.*?)\'\)" '
                               r'id="zne_hjhx_icon" target="_top">')
findCourseInformation = re.compile(r'<a class="courseName" href="/visit/stucoursemiddle\?courseid=(.*?)&amp;clazzid=('
                                   r'.*?)&amp;vc=1&amp;cpi=(.*?)" target="_blank" title="(.*?)">')
findCourseInformation1 = re.compile(r'<p title="(.*?)">')
findCourseInformation2 = re.compile(r'<p class="">(.*?)</p>')
findChooseCourses = re.compile(r'<input type="hidden" name="(.*?)" id="(.*?)" value="(.*?)"/>')
rule = re.compile(r'/(^\s+)|(\s+$)/g')
xxmhURL = 'https://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.whu.edu.cn%2Flogin%3Fservice%3Dhttp%3A' \
          '%2F%2Fehall.whu.edu.cn%2Fnew%2Findex.html'
jwxtURL = 'https://cas.whu.edu.cn/authserver/login?service=https%3A%2F%2Fbkxk.whu.edu.cn%2Fsso%2Fjznewsixlogin'
moocURL = 'https://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fwww1.mooc.whu.edu.cn%2Fsso%2Fwhu%3Bjsessionid' \
          '%3D9B498ADB02972E8A616E951164B5A34A'


def get_key():
    url = URL
    response = s.get(url=url)
    content = response.text
    html = BeautifulSoup(content, 'html.parser')
    values = html.find_all('form', id="casLoginForm")
    values = str(values)
    Lt = re.findall(findValue, values)[0][1]
    PwdDefaultEncryptSalt = re.findall(findpwdDefaultEncryptSalt, values)[0]
    return Lt, PwdDefaultEncryptSalt


def _res(length):
    char = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    a = len(char) - 1
    retStr = ''
    i = 0
    while i < length:
        b = round(random.random() * a)
        Str = char[b]
        retStr = retStr + Str
        i += 1
    return retStr


def _gas(data, key, iv):
    key = re.sub(rule, '', key, 0)
    pwdEncrypt = PwdEncrypt(key, iv)
    encrypted = pwdEncrypt.encrypt(data)
    return encrypted


def login():
    data = _res(64) + password
    key0 = pwdDefaultEncryptSalt
    iv0 = _res(16)
    encrypted = quote(_gas(data, key0, iv0), 'utf-8')
    url = URL
    data = 'username=' + username + '&password=' + encrypted + '&lt=' + lt + '&dllt=userNamePasswordLogin&execution' \
                                                                             '=e1s1&_eventId=submit&rmShown=1 '
    response = s.post(url=url, data=data, allow_redirects=False)
    response = redirects(response)
    if URL == xxmhURL:
        pass
    elif URL == jwxtURL:
        get_HomePage()
    elif URL == moocURL:
        get_mooc(response)


def get_mooc(response):
    content = response.text
    html = BeautifulSoup(content, 'html.parser')
    values = html.find_all('form', id="userLogin")
    values = str(values)
    fid = re.findall(findValue, values)[0][1]
    uname = re.findall(findValue, values)[1][1]
    enc = re.findall(findValue, values)[2][1]
    refer = re.findall(findValue, values)[3][1]
    refer = quote(refer, 'utf-8')
    authurl = re.findall(findValue, values)[4][1]
    authurl = quote(authurl, 'utf-8')
    time = re.findall(findValue, values)[5][1]
    expires = re.findall(findValue, values)[6][1]
    url = re.findall(findURL, values)[0]
    data = 'fid=' + fid +'&uname=' + uname + '&enc=' + enc + '&refer=' + refer + '&authurl=' + authurl + '&time=' + time + '&expires=' + expires
    response = s.post(url=url, data=data)
    content = response.text
    html = BeautifulSoup(content, 'html.parser')
    html = str(html)
    Name = re.findall(findName, html)[0]
    print(f'学生姓名：{Name}')
    CourseURL = re.findall(findMoocCourseURL, html)[0]
    response = s.get(url=CourseURL)
    content = response.text
    html = BeautifulSoup(content, 'html.parser')
    print('正在查询课程信息：')
    m = 1
    for Course in html.find_all('div', class_='Mconright httpsClass'):
        Course = str(Course)
        try:
            courseId = re.findall(findCourseInformation, Course)[0][0]
            classId = re.findall(findCourseInformation, Course)[0][1]
            cpi = re.findall(findCourseInformation, Course)[0][2]
            title = re.findall(findCourseInformation, Course)[0][3]
        except IndexError:
            courseId = '暂无相关信息'
            classId = '暂无相关信息'
            cpi = '暂无相关信息'
            title = '暂无相关信息'
        try:
            teacher = re.findall(findCourseInformation1, Course)[0]
        except IndexError:
            teacher = '暂无相关信息'
        try:
            courseTime = re.findall(findCourseInformation2, Course)[0]
        except IndexError:
            courseTime = '暂无相关信息'
        print(f'-----第{m}门课程信息-----')
        print(f'课程名称：{title}')
        print(f'授课老师：{teacher}')
        print(f'课程开放时间：{courseTime}')
    add_views(courseId, classId, cpi)


def add_views(courseId, classId, cpi):
    url = f'http://mooc1.mooc.whu.edu.cn/visit/stucoursemiddle?courseid={courseId}&clazzid={classId}&vc=1&cpi={cpi}'
    response = s.get(url=url)
    content = response.text
    findUrl = re.compile(r'("https://fystat-ans.*?")')
    a = re.findall(re.compile(r"(openc : '\w+')"), content)[0]
    b = re.findall(re.compile(r"('\w+')"), a)[0]
    openc = b.replace("'", '')
    url = re.findall(findUrl, content)[0]
    url = url.replace('"', '')
    for i in range(30):
        headers = {
            'Host': 'fystat-ans.chaoxing.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        content = response.text
        print(content)
        query_views(courseId, classId, cpi, openc)


def query_views(courseId, classId, cpi, openc):
    url = f'http://mooc1.mooc.whu.edu.cn/moocAnalysis/progressStatisticData?courseId={courseId}&classId={classId}&userId={cpi}&debug=false&rank=0&pageSize=30&pageNum=1&ut=s&cpi={cpi}&preRank=&preJobFinshCount=&preStuCount=&statisticSystem=0&openc={openc}'
    response = s.get(url=url)
    content = response.text
    num = re.findall(re.compile(r'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;章节学习次数：\d+'), content)[0]
    print(num)


def redirects(response):
    while True:
        Headers = response.headers
        Location = Headers['Location']
        url = Location
        response = s.get(url=url, allow_redirects=False)
        Code = response.status_code
        if Code == 302:
            continue
        elif Code == 200:
            break
    return response


def get_HomePage():
    gndm1 = 'N1056'  # 重修报名
    gndm2 = 'N100808'  # 学生个人信息维护
    gndm3 = 'N253508'  # 学生课表查询
    gndm4 = 'N2151'  # 学生课表查询
    gndm5 = 'N253512'  # 自主选课
    gndm6 = 'N305005'  # 学生成绩查询
    gndm7 = 'N254477'  # 选退课情况查询
    gndm8 = 'N2154'  # 学生课表查询（按周次）
    gndm9 = 'N253517'  # 自主选课(列表)
    print('操作序号：\n[1]重修报名\n[2]学生个人信息维护\n[3]学生课表查询\n[4]自主选课\n[5]学生成绩查询\n[6]选课退课情况')
    while True:
        order = input('请输入需要进行的操作序号：')
        if order == '1':
            gndm = gndm1
            break
        elif order == '2':
            gndm = gndm2
            break
        elif order == '3':
            gndm = gndm3
            break
        elif order == '4':
            gndm = gndm4
            break
        elif order == '5':
            gndm = gndm5
            break
        elif order == '6':
            gndm = gndm6
            break
        else:
            print('输入操作序号不存在，请重新输入！！！')
    url = 'http://bkxk.whu.edu.cn/xtgl/index_cxBczjsygnmk.html?gnmkdm=index&su=' + username
    data = 'gndm=' + gndm
    response = s.post(url=url, data=data)
    print(response.json())
    url = 'https://bkxk.whu.edu.cn/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=' + gndm + '&layout=default&su=' + username
    response = s.get(url=url)
    content = response.text
    Values = re.findall(findChooseCourses, content)
    xkxnm = Values[7][2]
    xkxqm = Values[8][2]
    jg_id_1 = Values[13][2]
    zyh_id = Values[14][2]
    zyfx_id = Values[16][2]
    njdm_id = Values[17][2]
    bh_id = Values[19][2]
    xslbdm = Values[22][2]
    ccdm = Values[23][2]
    xsbj = Values[24][2]
    jxbzb = Values[55][2]
    firstKklxdm = Values[56][2]
    zyjykc = 'AD9AED7571618644E0534500A8C09FE0'
    tsxxk = 'AD9AED7571818644E0534500A8C09FE0'
    ty = 'AD9AED7571978644E0534500A8C09FE0'
    yy = 'AD9AED7571B58644E0534500A8C09FE0'
    # 获取课程
    url = 'https://bkxk.whu.edu.cn/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=' +gndm + '&su=' + username
    data = 'tjbj_list%5B0%5D=1&njdm_id_list%5B0%5D=' + njdm_id + '&rwlx=1&xkly=1&bklx_id=0&xqh_id=1&jg_id=' + jg_id_1 + '&zyh_id=' + zyh_id + '&zyfx_id=' + zyfx_id + '&njdm_id=' + njdm_id + '&bh_id=' +bh_id + '&xbm=1&xslbdm=' + xslbdm + '&ccdm=' + ccdm + '&xsbj=' + xsbj + '&sfkknj=0&sfkkzy=0&sfznkx=0&zdkxms=0&sfkxq=0&sfkcfx=0&kkbk=0&kkbkdj=0&sfkgbcx=0&sfrxtgkcxd=0&tykczgxdcs=0&xkxnm=' + xkxnm + '&xkxqm=' + xkxqm + '&kklxdm=' + firstKklxdm + '&rlkz=0&xkzgbj=0&kspage=1&jspage=10&jxbzb=' + jxbzb
    response = s.post(url=url, data=data)
    content = response.json()
    tmpList = content['tmpList']
    m = 1
    for i in tmpList:
        date = i['dateDigit']
        jxb_id = i['jxb_id']
        kch_id = i['kch_id']
        kcmc = i['kcmc']
        print(f'-----课程{m}-----')
        print(f'课程名称：{kcmc}')
        print(f'时间：{date}')
        m += 1
    # 获取相关课程详细信息
    while True:
        order = int(input('请输入需要查看的课程序号：'))
        kch_id = tmpList[order - 1]['kch_id']
        kcmc = tmpList[order - 1]['kcmc']
        url = 'https://bkxk.whu.edu.cn/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=' + gndm + '&su=' + username
        data = 'tjbj_list%5B0%5D=1&njdm_id_list%5B0%5D=' + njdm_id + '&rwlx=1&xkly=1&bklx_id=0&xqh_id=1&jg_id=' + jg_id_1 + '&zyh_id=' + zyh_id + '&zyfx_id=' + zyfx_id + '&njdm_id=' + njdm_id + '&bh_id=' +bh_id + '&xbm=1&xslbdm=' + xslbdm + '&ccdm=' + ccdm + '&xsbj=' + xsbj + '&sfkknj=0&sfkkzy=0&sfznkx=0&zdkxms=0&sfkxq=0&sfkcfx=0&kkbk=0&kkbkdj=0&xkxnm=2020&xkxqm=3&rlkz=0&kklxdm=01&kch_id=' + kch_id + '&xkkz_id=' + zyjykc + '&cxbj=0&fxbj=0'
        response = s.post(url=url, data=data)
        content = response.json()
        for i in content:
            jsxx = i['jsxx']
            jsxx = jsxx.split('/')[1]
            jxbrl = i['jxbrl']
            jxdd = i['jxdd']
            jxdd = jxdd.replace('<br/>', ',')
            kcxzmc = i['kcxzmc']
            kkxymc = i['kkxymc']
            sksj = i['sksj']
            sksj = sksj.replace('<br/>', ',')
            print(f'-----课程{order}详细信息-----')
            print(f'课程名称：{kcmc}')
            print(f'授课老师：{jsxx}')
            print(f'课程容量：{jxbrl}')
            print(f'教学地点：{jxdd}')
            print(f'授课时间：{sksj}')
            print(f'课程性质：{kcxzmc}')
            print(f'开课学院：{kkxymc}')
        choice = input('请决定是否继续查看其他课程信息(是输入1，否输入2)：')
        if choice == '1':
            pass
        else:
            input('请按回车键退出')
            sys.exit()


def choose_course(gndm, jxb_ids, kch_id):
    url = 'https://bkxk.whu.edu.cn/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=' + gndm + '&su=' + username
    data = 'jxb_ids=' + jxb_ids + '&kch_id' + kch_id + '&kcmc=(3350330011062)%E6%9D%90%E6%96%99%E5%8C%96%E5%AD%A6+-+2+%E5%AD%A6%E5%88%86&rwlx=1&rlkz=0&rlzlkz=0&sxbj=0&xxkbj=0&qz=0&cxbj=0&xkkz_id=AD991D903C958CF5E0534500A8C0C043&njdm_id=2018&zyh_id=150&kklxdm=01&xklc=2&xkxnm=2020&xkxqm=3'


if __name__ == '__main__':
    s = requests.session()
    s.headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.135 Safari/537.36'
    }
    username = input('请输入帐号:')
    password = input('请输入密码:')
    print('[1]信息门户\n[2]教务系统\n[3]珞珈在线')
    way = input('请输入需要前往的网站序号:')
    if way == '1':
        URL = xxmhURL
    elif way == '2':
        URL = jwxtURL
    elif way == '3':
        URL = moocURL
    else:
        print('输入需要不存在！！！')
        input('请按任意键退出')
        sys.exit()
    A = get_key()
    lt = A[0]
    pwdDefaultEncryptSalt = A[1]
    login()
