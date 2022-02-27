import logging
import requests

logging.basicConfig(level=logging.INFO)

# 主号
token = ''  # 抓包 header中的x-rpc-combo_token
device_id = ''  # 抓包 header中的x-rpc-device_id
device_name='' #抓包 header中的x-rpc-device_name
device_model='' #抓包 header中的x-rpc-device_model
app_id = '1953439974'
usetgbot=True #是否使用Telegram机器人
bottoken='' #botfather发的token
chat_id='' #你的chat_id

host = 'https://api-cloudgame.mihoyo.com'

headers = {
    "x-rpc-combo_token": token,
    "x-rpc-client_type": "2",
    "x-rpc-app_version": "1.3.0",
    "x-rpc-sys_version": "11",
    "x-rpc-channel": "mihoyo",
    "x-rpc-device_id": device_id,
    "x-rpc-device_name": device_name,
    "x-rpc-device_model": device_model,
    "x-rpc-app_id": app_id,
    "Referer": "https://app.mihoyo.com",
    "Content-Length": "0",
    "Host": "api-cloudgame.mihoyo.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.14.9"
}


def main_handler(event, context):
    rsp = requests.post(f'{host}/hk4e_cg_cn/gamer/api/login', headers=headers)
    logging.debug(f"Login->{rsp.text}")
    rsp = requests.get(f'{host}/hk4e_cg_cn/wallet/wallet/get', headers=headers)
    coins = rsp.json()['data']['coin']
    free_times = rsp.json()['data']['free_time']
    total_time = rsp.json()['data']['total_time']
    logging.debug(f"Wallet->{rsp.json()}")
    logging.info(f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总时长:{total_time}分钟")
    sendtext=f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总时长:{total_time}分钟"
    rsp = requests.get(f'{host}/hk4e_cg_cn/gamer/api/listNotifications?status=NotificationStatusUnread'
                       f'&type=NotificationTypePopup&is_sort=true', headers=headers)
    logging.debug(f"ListNotifications->{rsp.text}")
    rewards = rsp.json()['data']['list']
    logging.info(f"总共有{len(rewards)}个奖励待领取。")
    sendtext=sendtext+"\r\n"+f"总共有{len(rewards)}个奖励待领取。"

    for reward in rewards:
        reward_id = reward['id']
        reward_msg = reward['msg']
        rsp = requests.post(f'{host}/hk4e_cg_cn/gamer/api/ackNotification',
                            json={
                                "id": reward_id
                            },
                            headers=headers)
        logging.info(f"领取奖励,ID:{reward_id},Msg:{reward_msg}")
        sendtext=sendtext+"\r\n"+f"领取奖励,ID:{reward_id},Msg:{reward_msg}"
        logging.debug(f"AckNotification->{rsp.text}")

    rsp = requests.get(f'{host}/hk4e_cg_cn/wallet/wallet/get', headers=headers)
    coins = rsp.json()['data']['coin']
    free_times = rsp.json()['data']['free_time']
    total_time = rsp.json()['data']['total_time']
    logging.debug(f"Wallet->{rsp.json()}")
    logging.info(f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总时长:{total_time}分钟")
    sendtext=sendtext+"\r\n"+f"米云币:{coins['coin_num']},免费时长:{free_times['free_time']}分钟,总时长:{total_time}分钟"
    logging.debug("处理成功")
    if usetgbot:
        send(sendtext)
    return "处理成功"

def send(message):
    url=r"https://api.telegram.org/bot"+bottoken+"/sendMessage"
    decodedata={}
    decodedata["text"]=message
    decodedata["chat_id"]=chat_id
    logging.debug(f"请求参数:{decodedata}")
    response=requests.post(url=url,data=decodedata)
    logging.debug(f"返回数据:{response.text}")
    logging.info("推送到Telegram成功")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_handler(None, None)
