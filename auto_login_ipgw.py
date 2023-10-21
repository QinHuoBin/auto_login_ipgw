import time
import requests
import config
import traceback
from login_ipgw import login

# 获取格式化时间的函数
t = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def check_online():
    """检查是否登录ipgw"""
    login_status = requests.get('https://ipgw.neu.edu.cn/cgi-bin/rad_user_info?callback=%20',timeout=1).text
    if '"error":"not_online_error"' in login_status:
        return False
    if '"error":"ok"' in login_status:
        return True

    # 有时候会出现504 Gateway Time-out错误，一般是校园网卡了，忽略之
    if '504 Gateway Time-out' in login_status:
        return False

    raise ValueError(login_status)


def main():
    """每过一段时间检测检测有没有登录，如果没有就登录"""
    while True:
        is_online = False
        try:
            is_online = check_online()
            if not is_online:
                print(f'{t()} 未登录校园网，尝试登录中...')
                is_success, reason = login(config.student_id, config.password)
                if is_success:
                    print(f'{t()} 登录成功')
                else:
                    print(f'{t()} 尝试登录失败，原因:', reason)
            else:
                print(f'{t()} online')
        except requests.exceptions.ConnectionError:
            print(f'{t()} 未连接校园网wifi')
        except Exception:
            print(f'{t()} 发生了其他错误')
            traceback.print_exc()

        # 如果没登录，下次检测间隔就更短
        if not is_online:
            time.sleep(1)
        else:
            time.sleep(10)


if __name__ == '__main__':
    main()
