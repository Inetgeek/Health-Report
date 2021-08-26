# Health-Report
Health report on the clock，健康上报自动打卡，代码仅适用于作者的学校网站，使用需在源代码基础上进行修改适配。
作者突发奇想创造了此物，仅供学习研究！版权归作者inetgeek所有，使用或引用请注明来源。
# 食用方法
## 工具
1. 能访问网络且24小时在线的服务器(centOS或Ubuntu系统)
2. python3.+环境
3. chorme浏览器+chrome驱动(Chrome-Driver)
4. python包(selenium、pyvirtualdisplay)及第三方工具(xvfb)
## 步骤
1. 在服务器(centOS或Ubuntu系统)上配置好python3.0+环境并建立软链接，因为代码基于python3编写，不支持python2.x
2. 下载chrome浏览器和配置好对应版本驱动，自行查阅资料
3. 在终端(terminal)根目录下载安装python包
```shell
pip3 install selenium
pip3 install pyvirtualdisplay
```
4. 在终端(terminal)根目录下载安装第三方工具(xvfb)
- Ubuntu系统
```shell
sudo apt-get install xvfb
```
- centOS
```shell
yum install xvfb
```
5. 根据自己所需调试代码及DEBUG即可。
# 邮件效果
![8(A`K0~2%~~_1U06WC 7}Y](https://user-images.githubusercontent.com/42563262/131002196-838b27c2-b068-4bc1-90bb-6628e34588ee.png)

![HG`S1}K(~3 5NYZLL4OKB}4](https://user-images.githubusercontent.com/42563262/130967581-f82889c1-5705-4206-963e-185252ca9c82.png)
