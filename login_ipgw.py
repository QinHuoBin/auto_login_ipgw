import requests

LOGIN_URL = 'https://pass.neu.edu.cn/tpass/login?service=http://ipgw.neu.edu.cn/srun_portal_sso?ac_id=16'


def login(student_id: str, password: str):
    """
    登录ipgw，要点：
    ① 以get方式访问https://pass.neu.edu.cn页面，响应中含有lt (login token)
    ② 以post方式访问https://pass.neu.edu.cn页面，提交学号密码lt等参数，响应中含有用于单点登录(sso)的ticket
    ③ 访问http://ipgw.neu.edu.cn/v1/srun_portal_sso?ac_id=16&ticket=xxx，提交ticket即可上网

    :param student_id: 学号
    :param password: 密码
    :return: (bool,reason) 若第一项为True则登录成功，否则登录失败，此时第二项会说明原因
    """
    # 访问统一登录获取lt
    session = requests.Session()
    get_pass_page = session.get(LOGIN_URL)
    if get_pass_page.status_code != 200:
        return False, f'访问pass.neu.edu.cn失败，状态码：{get_pass_page.status_code}'
    # text = ...<input type="hidden" id="lt" name="lt" value="LT-29360-**********-tpass" />\r\n\t\t\t
    text = get_pass_page.text

    # 获取lt (login token)
    target = '<input type="hidden" id="lt" name="lt" value="'
    # half = LT-29360-**********-tpass" />\r\n\t\t\t
    half = text[text.index(target) + len(target):]
    # lt = LT-29360-**********-tpass
    lt = half[:half.index('"')]

    # 获取execution
    target = '<input type="hidden" name="execution" value="'
    half = text[text.index(target) + len(target):]
    execution = half[:half.index('"')]

    # 拼接rsa
    rsa = student_id + password + lt
    ul = len(student_id)
    pl = len(password)

    # 获取用于sso链接，其中含有ticket
    get_sso_href = session.post(LOGIN_URL,
                                allow_redirects=False,  # 禁用转跳
                                data={'rsa': rsa,
                                      'ul': ul,
                                      'pl': pl,
                                      'lt': lt,
                                      'execution': execution,
                                      '_eventId': 'submit'})
    text = get_sso_href.text

    # 检测是否账号错误
    if '账号不存在' in text:
        return False, '可能是①账号或密码错误 ③登录流程需要更新'

    # 获取ticket
    target = 'ticket='
    half = text[text.index(target) + len(target):]
    href = half[:half.index('"')]
    sso_login = session.get('http://ipgw.neu.edu.cn/v1/srun_portal_sso?ac_id=16&ticket=' + href)
    if 'success' in sso_login.text:
        return True, None
    else:
        return False, f'sso登录返回{sso_login.text}'
