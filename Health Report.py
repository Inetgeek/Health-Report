#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select

url = 'xxxxxx' #需要登陆的网页
id = "xxxxxx" #你的学号
key = "xxxxxx" #你的密码

def get_code(url):
    display = Display(visible=0, size=(800, 800))
    display.start()
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(4) #因为测试网站需要先认证才能进入填表页面，因此下面到time.sleep(15)处均为自动登录验证网站操作
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[1]/input').send_keys(id) #注入学号
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]').send_keys(key) #注入密码
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[5]/button').click() #点击登录按钮
    time.sleep(15)
    code = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div/span') #判断是否已经打过卡
    if code: #打过卡则返回2
        return 2
    else: #没打过卡则进行下一步填表操作
        Select(driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[9]/td[2]/div/select')).select_by_value("35.5")#选择下拉列表35.5
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="V1_CTRL142"]').click()#勾选承诺
        time.sleep(5)
        driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[3]/ul/li/a').click()#点击提交按钮
        time.sleep(5)
        driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/button[1]').click()#点击“好”，完成提交
        display.stop()
        driver.quit() #退出操作
        return 1 #进行到这一步则说明正常提交，未抛出异常，返回1

status = get_code(url) #获得填表情况的状态

import smtplib
from email import (header)
from email.mime import (text, multipart)
import time
import datetime

def getNowDate(): #获取当前日期
    now_time = datetime.datetime.now()
    yes_time = now_time+datetime.timedelta(days=-0)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time

def sender_mail(): #构造并发送邮件
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465)
    sender_addrs = 'xxxxxx' #作为邮件发送服务器的邮箱号，此处须为开通pop3/smtp服务的邮箱
    password = "xxxxxx" #该邮箱的授权码
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['xxxxxx'] #用来接收打卡反馈情况邮件的邮箱，最好为常用邮箱
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "DingDang"
            msg['To'] = email_addrs
            msg['subject'] = header.Header(send_title, 'utf-8')
            msg.attach(text.MIMEText(send_content, 'html', 'utf-8'))
            smtp_Obj.sendmail(sender_addrs, email_addrs, msg.as_string())
        except Exception as e:
            continue
    smtp_Obj.quit()

Now_Date = getNowDate()
date = '<span style="color:#FC5531">'+Now_Date+'</span>'

if __name__ == "__main__":
    send_title = "向“理”报平安打卡状态"
    content_0 = '<p style="color:#507383">亲爱的主人：</p><p style="font-size:34px;color:#3095f1;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">今日已上报，无需进行任何操作！</span></p>'+date
    content_1 = '<p style="color:#507383">亲爱的主人：</p><p style="font-size:34px;color:#5fa207;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡成功，无需进行任何操作！</span></p>'+date
    content_2 = '<p style="color:#507383">亲爱的主人：</p><p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡失败，请及时手动打卡！</span></p>'+date
    if status == 2:
        send_content = content_0
        sender_mail()
        print("今日已上报，无需进行任何操作！")
    elif status == 1:
        send_content = content_1
        sender_mail()
        print("打卡成功，无需进行任何操作！")
    else:
        send_content = content_2
        sender_mail()
        print("打卡失败，请及时手动打卡！")
