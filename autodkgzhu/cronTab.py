from utils.dk_spider import DkSpider
import os, sys
from autodkgzhu.sender_email import send_mail
import datetime

if __name__ == '__main__':
    import django

    BASE_DIR = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE_DIR)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autodk.settings')
    django.setup()

from autodkgzhu.models import User
import logging

logger = logging.getLogger('django')


# 自动打卡定时器
def crontab():
    a = str(datetime.datetime.now())
    logger.info("当前时间：{}".format(a))
    a = a.split(' ')[1].split(':')
    h = int(a[0])
    if h != 7 and h != 6:
        return
    user_list = User.objects.all()
    for user in user_list:
        logger.info(datetime.datetime.now())
        logger.info("开始打卡:{}".format(user.username))
        spider = DkSpider(user.username, user.password)
        if not spider.login():
            logger.error("登陆失败")
            send_mail(user.email,'打卡失败')
            return
        if spider.get_dk_url() is None:
            logger.error("获取流水号链接失败")
            send_mail(user.email, '打卡失败')
            return
        if not spider.dk():
            logger.error("打卡失败")
            send_mail(user.email, '打卡失败')
            return
        send_mail(user.email, '打卡成功')
        logger.info("成功打卡:{}".format(user.username))


if __name__ == '__main__':
    crontab()
