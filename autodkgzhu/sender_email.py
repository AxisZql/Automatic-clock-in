import smtplib  # 发邮件的模块
from email.mime.text import MIMEText  # 定义邮件内容
from email.header import Header
import logging

logger = logging.getLogger('django')
def send_mail(receives,mail_content):
    # 发送邮箱服务器
    smtp_server = 'smtp.163.com'
    # 发送邮箱用户名和密码
    user = '发送方邮箱'
    password = '邮箱密钥'  # 设置的邮件服务独立密码
    # 发送和接收邮箱
    sender = '发送方邮箱'
    # 发送邮件主题和内容
    subject = "自动打卡通知"

    # 构建发送和接收信息
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(receives)

    # SSl协议端口号要使用465
    smtp = smtplib.SMTP_SSL(smtp_server, 465)

    # HELO向服务器标识用户的身份
    smtp.helo(smtp_server)

    # EHLO 服务器返回结果确认
    smtp.ehlo(smtp_server)

    # 登录邮箱服务器用户名和密码
    smtp.login(user, password)

    logger.info("Start send Email....")

    smtp.sendmail(sender, receives, msg.as_string())
    smtp.quit()
    logger.info("Send End!")
