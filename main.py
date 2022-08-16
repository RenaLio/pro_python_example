import time
import base64
import requests
import random
import schedule
from loguru import logger

trace  = logger.add('./logs/runtime.log',retention='3 days')

def update_sub():       # 1 Hour
    global list_sub
    url = 'https://raw.githubusercontent.com/RenaLio/Mux2sub/main/sub_list'
    try:
        with requests.get(url,timeout=5) as resp:
            if resp.status_code==200:
                list_sub = resp.text
                list_sub = list_sub.split()
                list_sub = list_sub[3:]
                logger.info(f'访问sub成功')
            else:
                logger.error(f'访问sub错误，状态码{resp.status_code}')
    except:
        logger.error('访问sub连接超时 | 访问失败')

def update_url():       # 0.5 Hour
    global list_url
    url = 'https://raw.githubusercontent.com/RenaLio/Mux2sub/main/urllist'
    try:
        with requests.get(url,timeout=5) as resp:
            if resp.status_code==200:
                list_url = resp.text
                list_url = list_url.split()
                logger.info(f'访问url_list成功')
            else:
                logger.error(f'访问url_list错误，状态码{resp.status_code}')
    except:
        logger.error('访问url_list连接超时 | 访问失败')

def get_base64():       # 1 Day
    url = 'https://raw.githubusercontent.com/RenaLio/Mux2sub/main/z_textlist'
    try:
        with requests.get(url,timeout=5) as resp:
            if resp.status_code==200:
                base_text = resp.text
                base_text = base_text.encode('utf-8')
                bs64 = base64.b64encode(base_text)
                logger.info(f'访问BS64成功')
                with open(TEXT_PATH,'wb+') as f:
                    f.write(bs64)
                logger.info(f'更新BS64成功')
            else:
                logger.error(f'访问BS64错误，状态码{resp.status_code}')
    except:
        logger.error('访问BS64连接超时 | 访问失败')

def get_num():      # 5min
    global num_sub,num_url
    num_sub = random.randint(0,len(list_sub)-1)
    num_url = random.randint(0,len(list_url)-1)
    # return num_sub,num_url

def get_sub():      # 5min
    global num_sub
    logger.info(f'sub_num is {num_sub}')
    url = list_sub[num_sub]
    try:
        with requests.get(url,headers=headers,timeout=5) as resp:
            if resp.status_code==200:
                url_info = resp.text
                if url_info=='':
                    logger.error(f'访问订阅:{url} 为空')
                    return
                try:
                    with open(SUB_PATH,'w',encoding='utf-8') as f:
                        f.write(url_info)
                    logger.info(f'更新订阅:{url}成功')
                except:
                    logger.debug(f'写入{SUB_PATH}失败')
            else:
                logger.error(f'访问订阅{url}错误，状态码{resp.status_code}')
    except:
        logger.error('访问订阅连接超时 | 访问失败')

def get_url():      # 5min
    global num_url
    logger.info(f'url_num is {num_url}')
    url = list_url[num_url]
    try:
        with requests.get(url,headers=headers,timeout=5) as resp:
            if resp.status_code==200:
                url_info = resp.text
                if url_info=='':
                    logger.error(f'访问订阅:{url} 为空')
                    bot_send(f'访问订阅:{url} 为空')
                    return
                try:
                    with open(URL_PATH,'w',encoding='utf-8') as f:
                        f.write(url_info)
                    logger.info(f'更新订阅:{url}成功')
                except:
                    logger.debug(f'写入{URL_PATH}失败')
            else:
                logger.error(f'访问订阅{url}错误，状态码{resp.status_code}')
    except:
        logger.error('访问订阅连接超时 | 访问失败')
    


@logger.catch
def bot_send(text):
    user_id = 1650055710
    bot_token = 'sadasd:123456'
    params = {
        'chat_id': user_id,
        'text': text
    } 
    url = 'https://api.telegram.org/bot'+bot_token+'/sendMessage'
    with requests.get(url,params=params,timeout=5) as resp:
        if resp.status_code==200:
            logger.info(f'Telegarm Bot 发送消息成功')
        else:
            logger.error(f'Telegarm Bot 发送消息失败')

@logger.catch
def main():
    update_sub()
    update_url()
    get_num()
    get_sub()
    get_url()
    get_base64()
    schedule.every().day.at("12:00").do(get_base64)
    schedule.every(30).minutes.do(update_url)
    schedule.every().hour.do(update_sub)
    schedule.every(5).minutes.do(get_num)
    schedule.every(5).minutes.do(get_sub)
    schedule.every(5).minutes.do(get_url)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__=='__main__':
    SUB_PATH = './temp'
    URL_PATH = './paste'
    TEXT_PATH = './text'
    list_sub = []
    list_url =[]
    num_sub,num_url = 0,0
    headers = {'User-Agent': 'ClashforWindows/0.19.26'}
    main()
