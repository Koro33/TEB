# #Tongji# 电费自动查询预警脚本
<!-- TOC -->

- [#Tongji# 电费自动查询预警脚本](#tongji-电费自动查询预警脚本)
    - [配置环境](#配置环境)
    - [使用说明](#使用说明)
    - [问题](#问题)
    - [更新记录](#更新记录)

<!-- /TOC -->

实在搞不懂学校为什么不能做一个电费提醒的功能，每次断电都断的猝不及防，只能自力更生

于是就诞生了这个脚本

这个脚本能够实现(~~对我的宿舍~~)电费的查询，并且在电费低于10块钱的时候，发邮件通知该充钱了。


## 配置环境

- Ubuntu 16.04
- python 3.5
- 第三方包 requests, lxml

注：lmxl 包在用 `pip` 安装的时候需要编译，对某些小设备比如Raspberry来说可能不太友好（时间可能需要半个小时以上）可以用软件包的形式来安装

```bash
sudo apt-get install python3-lxml
```

## 使用说明

使用 **crontab** 功能定期(比如每天上午8点)执行一次脚本

在 **Terminal** 中键入 `crontab -e`，然后在文件的最后加入

```bash
0 15 * * *  bash /home/pi/TEB/TEB.sh
```

**ps**: 不要忘了给 `.sh` 文件加可执行属性

```bash
chmod +x TEB.sh
```

## 问题

学校能源中心的网站 [http://202.120.163.129:88/](http://202.120.163.129:88/) 只能在校内的ip段访问，我还没有想到怎么在云服务器上挂这个脚本。

~~也许我应该常年在宿舍挂一个树莓派~~
目前真的是这样干的

## 更新记录

v1.2.0  _2017-07-21_

1. 因网站使用了某些反爬措施，导致前一个版本失效，所以修改了爬网站的模式，更加接近人类操作，一般不会被 ban 掉了，但是同时代码量变得很大（一个网页要 post 6次），速度也变慢了
2. 大面积重构（包括 JSON 文件结构，邮件的发送逻辑等）
3. 某些功能的预支持（管理员模式，异常通知，日志等）

v1.1.2  _2017-06-08_

1. 完善注释
2. 修改 JSON 文件结构，增加 `alarm_threshold` 字段

v1.1.1  _2017-05-14_

1. 修复多人接收收件人显示不正确的问题
2. 添加 `.sh` 文件来执行计划任务，防止因环境变量问题造成执行失败

v1.1.0  _2017-05-14_

1. 修改了json文件的结构
2. 允许添加多个房间，每个房间可以有多个接收通知的人
3. 修改了邮件的标题，便于设置分类和免打扰

v1.0.0  _2017-05-13_

1. 实现对固定宿舍的电费查询
2. 实现电费低时邮件提醒

