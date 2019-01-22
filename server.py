# -*- coding:utf-8 -*-
__author__ = 'daming.ge'

import time, datetime
import json, requests
import hashlib
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def get_now():
    return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def gethash1(content):
    shaa1 = hashlib.sha1()
    shaa1.update(content.encode('utf-8'))
    res = shaa1.hexdigest()
    # print(res)
    return (res)


def generate_group_hash_string(user_id, nowtime_13, x_mt_token):
    ret = '''/v2/account/userinfo/listall
page=1&page_size=30&user_id=''' + str(user_id) + '''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:''' + x_mt_token + str(nowtime_13) + '''
x-mt-token:''' + x_mt_token + '''
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''

    return (gethash1(ret))


def generate_group_user_hash_string(group_id, nowtime_13, x_mt_token):
    ret = '''/v2/msg/group/info
group_id=''' + group_id + '''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:''' + x_mt_token + str(nowtime_13) + '''
x-mt-token:''' + x_mt_token + '''
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''

    return (gethash1(ret))


def generate_group_header(user_id, nowtime_13, x_mt_token):
    header = {':authority': 'api.mtoilet.com',
              'x-mt-token': x_mt_token,
              'x-mt-appid': 'mtoilet',
              'x-mt-devtype': 'Redmi Note 3',
              'x-mt-channel': 'ringle',
              'x-mt-version': '2.0.27',
              'x-mt-platform': 'android',
              'x-mt-devid': '742344B46C61',
              'x-mt-rid': x_mt_token + str(nowtime_13),
              'x-mt-sign': generate_group_hash_string(user_id, nowtime_13, x_mt_token),
              'referer': 'http://android.mtoilets.com',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/3.10.0'
              }
    return (header)


def generate_group_user_header(group_id, nowtime_13, x_mt_token):  # hash 根据group id得到user list header
    header = {':authority': 'api.mtoilet.com',
              'x-mt-token': x_mt_token,
              'x-mt-appid': 'mtoilet',
              'x-mt-devtype': 'Redmi Note 3',
              'x-mt-channel': 'ringle',
              'x-mt-version': '2.0.27',
              'x-mt-platform': 'android',
              'x-mt-devid': '742344B46C61',
              'x-mt-rid': x_mt_token + str(nowtime_13),
              'x-mt-sign': generate_group_user_hash_string(group_id, nowtime_13, x_mt_token),
              'referer': 'http://android.mtoilets.com',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/3.10.0'
              }
    return (header)


def get_new_group(user_id, x_mt_token):
    nowtime_13 = int(round(time.time() * 1000))
    url = 'https://api.mtoilet.com/v2/account/userinfo/listall?user_id=' + str(user_id) + '&page=1&page_size=30'
    s = requests.Session()
    aaa = s.get(url, headers=generate_group_header(user_id, nowtime_13, x_mt_token))
    content = aaa.content.decode().translate(non_bmp_map)
    bbb = json.loads(content)
    # print(bbb)

    if len(bbb['data']['data']) > 0:
        print(user_id, '用户发现了这么多Group', len(bbb['data']['data']))
        for each_one in bbb['data']['data']:
            each = each_one['res_info']
            # print(each)
            if each['expire_time'] > int(time.time()):
                g_list[each['group_id']] = [each['name'], each['expire_time'], each['user_count'], each['redpkg_money'],
                                            each['vote']]
                time.sleep(1)
        print('-----------------------------------------------------------------------------------------------------')
        print(get_now(), '当前待领红包群数量是 %d 个' % (len(g_list)))
        for key in list(g_list.keys()):  # 由 result 变为 result.keys()
            # print(g_list[key][1])
            print(get_now(), '红包ID为%s' % key, '红包金额 %d 元' % (g_list[key][3] / 100), '当前人数 %d 个' % (g_list[key][2]),
                  '剩余时间 %d 秒' % (g_list[key][1] - int(time.time())))
            if int(time.time()) > g_list[key][1]:
                print(get_now(), key, g_list[key], '已过时')
                g_list.pop(key)
                # continue
        with open('information.txt', mode='w', encoding='utf-8') as f0:
            f0.write((json.dumps(g_list, ensure_ascii=False, indent=4)))
    else:
        print(user_id, '用户没有Group')
def get_user_of_group(group_id, x_mt_token):
    nowtime_13 = int(round(time.time() * 1000))
    url = 'https://api.mtoilet.com/v2/msg/group/info?group_id=' + group_id
    s = requests.Session()
    aaa = s.get(url, headers=generate_group_user_header(group_id, nowtime_13, x_mt_token))
    content = aaa.content.decode().translate(non_bmp_map)
    bbb = json.loads(content)
    try:
        users = bbb['data']['group_info']['users']
        print(get_now(), group_id, '发现了%d个用户' % (len(users)))
        return (users)
    except:
        return (0)

g_list = {}
u_list={}
while (1):


    x_mt_token = 'T1g0NwatZMFmtaOJbeLDIGXTwMabENI0u3Ew==.d7b'

    with open('userlist.txt',mode='r',encoding='utf-8') as f_user:
        a=f_user.read()
        user_content=json.loads(a)
        print('当前用户库数量为%d'%len(user_content))
        if len(user_content)>1000:
            for every_user in list(user_content.keys())[0:1000]:
                get_new_group(every_user, x_mt_token)
        else:
            for every_user in list(user_content.keys()):
                get_new_group(every_user, x_mt_token)

    #time.sleep(2)


        # with open('information.txt', mode='r', encoding='utf-8') as f2:
        #     content = json.loads(f2.read())
        #                 for every_user in sss:
        #                     try:
        #                         get_new_group(every_user, x_mt_token)
        #                     except:
        #                         print('error happen')
