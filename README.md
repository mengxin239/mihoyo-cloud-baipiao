# 云原神每天签到免费15分钟脚本

由 https://github.com/fves1997/Cloud-Genshin-Impact 修改而来

我做了一些优化，加了点功能

有什么想要的可以发lessue，我看见会回复的

## 使用方法

安装需要的东西 
`pip install requests`

CentOS:

`yum install screen git -y`

Debian&Ubuntu:

`apt install screen git -y`

下面都是一样的

`git clone https://github.com/mengxin239/mihoyo-cloud-baipiao.git
cd mihoyo-cloud-baipiao`

手机打开小黄鸟，打开云原神，找到请求`https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/getUIConfig`的那个

里面的信息填写到mihoyo.py

运行
`screen python mihoyo.py`

如果需要推送到telegram，按照注释填写即可

TG群：https://t.me/mengxblog
