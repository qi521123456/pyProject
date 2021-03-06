# encoding=utf-8

def do_telnet(Host, username, password, finish, commands):
    import telnetlib
    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host, port=23, timeout=10)
    tn.set_debuglevel(2)

    # 输入登录用户名
    tn.read_until('login: '.encode())
    tn.write(username + '\n')

    # 输入登录密码
    tn.read_until('password: '.encode())
    tn.write(password + '\n')

    # 登录完毕后执行命令
    tn.read_until(finish)
    for command in commands:
        tn.write('%s\n' % command)

        # 执行完毕后，终止Telnet连接（或输入exit退出）
    tn.read_until(finish)
    tn.close()  # tn.write('exit\n')


if __name__ == '__main__':
    # 配置选项
    Host = '192.168.205.67'  # Telnet服务器IP
    username = 'root'  # 登录用户名
    password = '123456'  # 登录密码
    finish = ':~$ '  # 命令提示符
    commands = ['echo "test"']
    do_telnet(Host, username, password, finish, commands)