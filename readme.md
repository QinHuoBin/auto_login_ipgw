## 自动登录东北大学ipgw
keywords: **neu ipgw auto login**  
基于python3与requests库实现东北大学IPGW的自动登录。  
使用场景：
* 开机自动登录ipgw
* ipgw断连后自动重连
### 安装requests库:
`pip install requests`
### 填写学号与密码
在config.py中填写自己的学号与密码。
### 开机自启动:
win10任务计划程序->创建任务，然后
* 新建“触发器”，“开始任务”选择“登陆时”
* 新建“操作”，“程序或脚本”选择start.bat  
成功运行的标志是：开机后有一个在运行脚本的命令行窗口。
### wifi设置:
连接NEU的无线网络时，要勾选"自动连接"，这样wifi偶尔断开后系统可以自动重新连接wifi，然后脚本自动登录ipgw。
### 程序说明:
* auto_login_ipgw.py: 实现ipgw登陆状态检测
* login_ipgw.py: 实现ipgw登录