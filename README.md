### 广州大学疫情自动打卡
* 项目说明
>本项目基于django框架和python的request库实现

* 使用方法
>1. 构建docker镜像
> ```shell
> docker-compose build
>```
> 2.启动docker容器
> ```shell
> docker-compose up -d
>```
> 3.查看容器是否启动成功
> ```shell
> docker ps
>```

* 温馨提示：本项目使用的是sqlit3数据库，在使用本系统前需要将本人的账号、密码、邮箱信息录入sqlit3数据库
> sqlit3数据库是完全离线的，你不必担心账号信息泄露的问题。

PS: sqlit3数据库的基本使用方法请自行百度