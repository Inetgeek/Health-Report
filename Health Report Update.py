#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import Select
"""
学校填表页面新增栏目,这里支持最新的表单,同步更新源码
"""
url = '打卡内网链接,需要请联系作者InetGeek(ranshens@foxmail.com)'
id = "学号"
key = "密码"

def get_code(url):
    display = Display(visible=0, size=(800, 800))
    display.start()
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[1]/input').send_keys(id)
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]').send_keys(key)
    driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div/form/p[5]/button').click()
    time.sleep(15)
    try:
        driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div/span")
        display.stop()
        driver.quit()
        return 2
    except:
        try:
            Select(driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[9]/td[2]/div/select')).select_by_value("35.5")#选择下拉列表35.5
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[11]/td[6]/div/font/font/div/font/font/strong/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[41]/td[2]/font/div/strong[2]/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[42]/td[2]/font/div/strong[2]/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="V1_CTRL142"]').click()#勾选承诺
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[3]/ul/li/a').click()#点击提交按钮
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/button[1]').click()#点击“好”，完成提交
            display.stop()
            driver.quit()
            return 1
        except:
            display.stop()
            driver.quit()
            return 0

status = get_code(url)

import smtplib
from email import (header)
from email.mime import (text, multipart)
import time
import datetime

def getNowDate():
    now_time = datetime.datetime.now()
    yes_time = now_time+datetime.timedelta(days=-0)
    current_time = yes_time.strftime('%Y-%m-%d')
    return current_time

def sender_mail():
    smtp_Obj = smtplib.SMTP_SSL('smtp.qq.com',465)
    sender_addrs = '服务器邮箱号'
    password = "授权码"
    smtp_Obj.login(sender_addrs, password)
    receiver_addrs = ['收件邮箱']
    for email_addrs in receiver_addrs:
        try:
            msg = multipart.MIMEMultipart()
            msg['From'] = "Digran"
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
    send_head = '<p style="color:#507383">亲爱的主人：</p>'
    content_0 = send_head+'<p style="font-size:34px;color:#3095f1;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">今日已上报，无需进行任何操作！</span></p>'+date
    content_1 = send_head+'<p style="font-size:34px;color:#5fa207;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡成功，无需进行任何操作！</span></p>'+date
    content_2 = send_head+'<p style="font-size:34px;color:#ca1b0f;"><span style="border-bottom: 1px dashed #ccc; z-index: 1; position: static;">打卡失败，请及时手动打卡！</span></p>'+date
    if status == 2:
        send_content = content_0
        sender_mail()
        print("今日已上报，无需进行任何操作！")
    elif status == 1:
        send_content = content_1
        sender_mail()
        print("打卡成功，无需进行任何操作！")
    elif status == 0:
        send_content = content_2
        sender_mail()
        print("打卡失败，请及时手动打卡！")
    else:
        send_content = content_2
        sender_mail()
        print("打卡失败，请及时手动打卡！")
