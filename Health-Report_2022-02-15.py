#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
:code: Colyn
:date: 2022-02-15
:lib_url: https://github.com/inetgeek

:intro: 本代码是基于作者所在学校健康上报系统编写，若外校同学使用则在本代码基础上二次修改即可。本项目默认follower为有基础的coder，没有详细说明怎么具体使用该小项目，因此请用户根据import所导入的库进行安装、配置环境，此处给出简单教程:
        - 运行环境：python 3.x及相应modules/packages(e.g. selenium/pyvirtualdisplay etc.)
        - 浏览器环境：chrome-linux版
        - 驱动：chromedriver-linux版
        - 作为发送邮件的邮箱号 代码基于pop3/smtp的smtp.qq.com服务器编写(即qq邮箱)
        收件邮箱若为多个，则在下方的['收件邮箱']列表里添加新的邮箱号即可，此处邮箱可以不为qq邮箱
        可以根据自己的需求增加、删除及修改所注入的信息、栏目，比如温度此处写的为35.5，用户可更改为其他温度
"""

import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# 正常请求页rul: http://xxxx.xxxx.edu.cn/xxx # 此链接若为本校同学请联系作者获取

url = '学校健康打卡表单链接'  # 即正常请求页url
uid = "学号"
pwd = "密码"


def get_code(url):
    """
    开始进行爬取网页并注入信息
    :param url: target_url
    :return: state_code
    """
    # 启动虚拟环境
    display = Display(visible=0, size=(800, 800))
    display.start()

    # 启动 Headless Chrome by ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    # 登录 target_url
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(uid)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(pwd)
    driver.find_element_by_xpath('//*[@id="login_submit"]').click()
    time.sleep(5)

    """
    异常处理, 进行信息填报
    """
    try:
        # 若显示: 您今日已报过平安，请明日再来打卡哦！
        driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div/span")

        # return state_code
        return 2

    # 否则就继续打卡, 并记录异常内容
    except Exception as step_1:
        print(step_1)

        try:
            time.sleep(2)

            # 栏目: 填报时体温，此处为35.5°
            Select(driver.find_element_by_xpath('//*[@id="V1_CTRL173"]')).select_by_value("35.5")
            time.sleep(1)

            # 栏目: 最近一次核酸检测时间，此处为2022-02-12
            driver.find_element_by_xpath('//*[@id="V1_CTRL212"]').send_keys("2022-02-12")
            time.sleep(1)

            # 栏目: 所在地是否为中高风险地区？此处选的是"否"
            driver.find_element_by_xpath('//*[@id="V1_CTRL167"]').click()
            time.sleep(1)

            # 栏目: 离开南京时间（新生不填），此处为此处为2022-01-10
            driver.find_element_by_xpath('//*[@id="V1_CTRL83"]').send_keys("2022-01-10")
            time.sleep(1)

            # 按钮: 本人承诺以上填写内容均真实可靠！
            driver.find_element_by_xpath('//*[@id="V1_CTRL142"]').click()
            time.sleep(1)

            # 按钮: 确认填报
            driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[3]/ul/li/a').click()
            time.sleep(1)

            # 确认提交 "好"
            driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/button[1]').click()

            # return state_code
            return 1

        # 否则就结束, 并记录异常内容
        except Exception as step_2:
            print(step_2)

            # return state_code
            return 0

    # 退出Virtual WebView
    finally:
        display.stop()
        driver.quit()


# 获取填写状态码，具体说明见下方参数@param
status = get_code(url)

import smtplib
from email import (header)
from email.mime import (text, multipart)
import datetime


def getNowDate():
    """
    获取当前日期
    :return: current_time
    """
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-0)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time


def sender_mail():
    """
    发送状态邮件
    邮箱服务器: smtp.qq.com
    """
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com', 465)
    sender_addrs = '发送邮箱号(必须是qq邮箱且开通pop3/smtp服务)'
    password = "发送邮箱授权码(上述邮箱的授权码)"
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['收件邮箱']
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "发送人昵称"
            msg['To'] = email_addrs
            msg['subject'] = header.Header(send_title, 'utf-8')
            msg.attach(text.MIMEText(send_content, 'html', 'utf-8'))
            smtp_Obj.sendmail(sender_addrs, email_addrs, msg.as_string())
        except Exception as e:
            continue
    smtp_Obj.quit()


Now_Date = getNowDate()
date = '<span style="color:#FC5531">' + Now_Date + '</span>'

if __name__ == "__main__":

    send_title = "向“理”报平安打卡状态"
    send_head = '<p style="color:#507383">亲爱的主人：</p>'
    content_0 = send_head + '<p style="font-size:34px;color:#3095f1;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">今日已报，无需进行任何操作！</span></p>' + date
    content_1 = send_head + '<p style="font-size:34px;color:#5fa207;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡成功，无需进行任何操作！</span></p>' + date
    content_2 = send_head + '<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡失败，设置失效！</span></p>' + date
    content_3 = send_head + '<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡失败，未知原因！</span></p>' + date

    if status == 2:
        send_content = content_0
        sender_mail()
        print("今日已报，无需进行任何操作！")
    elif status == 1:
        send_content = content_1
        sender_mail()
        print("打卡成功，无需进行任何操作！")
    elif status == 0:
        send_content = content_2
        sender_mail()
        print("打卡失败，设置失效！")
    else:
        send_content = content_3
        sender_mail()
        print("打卡失败，未知原因！")
