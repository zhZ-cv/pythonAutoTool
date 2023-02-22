# -*- codeing = utf-8 -*-
# @Time : 2022/8/31 15:19
# @Author : MOTR
# @File : AutoWork.py
# @Software : PyCharm
from PIL import Image
import os
import sys
import zipfile

# 防止字符串乱码
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def pic2pdf():
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pdf_name = x.split('.')[0]
            im1 = Image.open(os.path.join(currentPath, x))
            im1.save(currentPath + '\\' + pdf_name + '.pdf', "PDF")
            print(f'\033[0;33;48m图片：{x}已经转换为pdf\033[0m')


def zipFiles():
    handle = zipfile.ZipFile('图片.zip', 'w')
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            handle.write(x)
            print(f'\033[0;33;48m图片：{x} 已经加入压缩包\033[0m')
    handle.close()


def deleteFiles():
    method1 = input('输入1删除所有图片；输入2删除所有pdf；输入3删除所有zip；输入4删除所有图片、pdf和zip；输入0取消本次操作\n请输入想要的数字：')
    if method1 == '1':
        for x in file_list:
            if ".jpg" in x or '.png' in x or '.jpeg' in x:
                os.remove(currentPath + '\\' + x)
                print(f'\033[0;33;48m文件：{x}已经删除\033[0m')
    elif method1 == '2':
        for x in file_list:
            if '.pdf' in x:
                os.remove(currentPath + '\\' + x)
                print(f'\033[0;33;48m文件：{x}已经删除\033[0m')
    elif method1 == '3':
        for x in file_list:
            if '.zip' in x:
                os.remove(currentPath + '\\' + x)
                print(f'\033[0;33;48m文件：{x}已经删除\033[0m')
    elif method1 == '4':
        for x in file_list:
            if ".jpg" in x or '.png' in x or '.jpeg' in x or '.pdf' in x or '.zip' in x:
                os.remove(currentPath + '\\' + x)
                print(f'\033[0;33;48m文件：{x}已经删除\033[0m')


if __name__ == '__main__':
    if os.name == 'nt':
        os.system('')
    print('\033[0;34;48m 自动化办公小助手-version1.0 \033[0m'.center(99, '='))
    currentPath = os.path.dirname(sys.executable)
    # currentPath = os.path.dirname(os.path.abspath(__file__))
    while True:
        print('\033[0m输入1将所有图片转为pdf；输入2将所有图片压缩到图片.zip；输入3删除所有的图片或pdf或zip文件；输入0退出本软件')
        method = input('请输入本次操作的数字：')
        if method == '0':
            exit(0)
        file_list = os.listdir(currentPath)
        if method == '1':
            pic2pdf()
        elif method == '2':
            zipFiles()
        elif method == '3':
            deleteFiles()
        else:
            print('\033[0;31;48m无效的操作模式，请重新输入\033[0m')
        print('\033[0;34;48m', end='')
        print(' 本次操作完成！可以重新选择其他操作方式！'.center(77, '-'))
