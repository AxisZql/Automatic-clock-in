import requests
from utils.request_handle import *
from urllib import parse
import logging

logger = logging.getLogger('django')

url = {
    'login': 'https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fyqtb.gzhu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttps%253A%252F%252Fyqtb.gzhu.edu.cn%252Finfoplus%252Foauth2%252Fauthorize%253Fx_redirected%253Dtrue%2526scope%253Dprofile%252Bprofile_edit%252Bapp%252Btask%252Bprocess%252Bsubmit%252Bprocess_edit%252Btriple%252Bstats%252Bsys_profile%252Bsys_enterprise%252Bsys_triple%252Bsys_stats%252Bsys_entrust%252Bsys_entrust_edit%2526response_type%253Dcode%2526redirect_uri%253Dhttps%25253A%25252F%25252Fyqtb.gzhu.edu.cn%25252Ftaskcenter%25252Fwall%25252Fendpoint%25253FretUrl%25253Dhttps%2525253A%2525252F%2525252Fyqtb.gzhu.edu.cn%2525252Ftaskcenter%2525252Fworkflow%2525252Findex%2526client_id%253D1640e2e4-f213-11e3-815d-fa163e9215bb',
    'dk': 'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start',
    'first': 'https://yqtb.gzhu.edu.cn/infoplus/interface/listNextStepsUsers',  # 第一次提交数据
    'second': 'https://yqtb.gzhu.edu.cn/infoplus/interface/doAction',  # 第二次提交

}
headers = {
    'Referer': 'https://yqtb.gzhu.edu.cn/infoplus/form/XNYQSB/start',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}


class DkSpider(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = requests.session()

    def login(self):
        count = 4  # 重试登陆次数
        while count != 0:
            try:
                resp = self.client.get(url=url['login'])
                req = get_login_form(
                    resp.content, self.username, self.password)
                resp = self.client.post(url['login'], data=req)
                if "统一身份认证" in resp.text:
                    logger.error(
                        "登录错误，请到新版数字广大登录检查是否正常，如果改过密码请重新输入:连续登录失败5次，账号将被锁定5分钟")
                    return False
                else:
                    return True
            except requests.RequestException as e:
                count -= 1

    def get_dk_url(self):
        # 打卡需要流水号,获取打卡链接
        try:
            resp = self.client.get(url=url['dk'], headers=headers)
            selector = etree.HTML(resp.content)
            resp = self.client.post(url='https://yqtb.gzhu.edu.cn/infoplus/interface/start', headers=headers, data={
                'idc': 'XNYQSB',
                'release': '',
                'csrfToken': selector.xpath("//meta[@itemscope='csrfToken']/@content")[0],
                'lang': 'zh',
            })

            js = json.loads(resp.text)
            dk_url = js.get('entities')[0]
            return dk_url
        except requests.RequestException as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

    # 打卡
    def dk(self):
        try:
            dk_url = self.get_dk_url()
            form1, form2 = get_listNextStepsUsers_form(self.client, headers, dk_url=dk_url)
            resp1 = self.client.post(url=url['first'], headers=headers, data=parse.urlencode(form1))
            resp1 = json.loads(resp1.text)

            if resp1.get('errno') != 0 and resp1.get('ecode') != 'SUCCEED':
                logger.error(resp1.get('error'))
                return False

            resp2 = self.client.post(url=url['second'], headers=headers, data=parse.urlencode(form2))
            resp2 = json.loads(resp2.text)

            if resp2.get('errno') != 0 and resp2.get('ecode') != 'SUCCEED':
                logger.error(resp2.get('error'))
                return False
            return True
        except requests.RequestException as e:
            logger.error(e)
            return False
        except Exception as e:
            logger.error(e)
            return False
