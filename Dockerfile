FROM python:3.6
RUN apt-get -y update
#安装定时器插件
RUN apt-get install cron -y
# 设置工作目录
WORKDIR /gzhu
ADD . /gzhu
RUN pip3 install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8100
ENV SPIDER=/gzhu
#宿主系统时间和容器时间同步
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
RUN service cron start
