from django.core.management.base import BaseCommand
from utils.dk_spider import DkSpider
from autodkgzhu.sender_email import send_mail
import datetime
from autodkgzhu.models import User
import logging

logger = logging.getLogger('django')
class Command(BaseCommand):#必须继承

    def handle(self, *args, **options):
        a = str(datetime.datetime.now())
        logger.info("当前时间：{}".format(a))
        a = a.split(' ')[1].split(':')
        h = int(a[0])
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
            send_mail(user.email, '打卡成功 test is ok')
            logger.info("成功打卡:{}".format(user.username))