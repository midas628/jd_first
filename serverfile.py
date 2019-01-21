# -*- coding:utf-8 -*-
__author__ = 'daming.ge'

import time
import json, requests
import hashlib
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


def gethash1(content):
    shaa1 = hashlib.sha1()
    shaa1.update(content.encode('utf-8'))
    res = shaa1.hexdigest()
    # print(res)
    return (res)


def generate_group_hash_string(user_id,nowtime_13,x_mt_token):
    ret = '''/v2/account/userinfo/listall
page=1&page_size=30&user_id=''' + str(user_id) + '''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:'''+x_mt_token+str(nowtime_13) + '''
x-mt-token:'''+x_mt_token+'''
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''

    return (gethash1(ret))


def generate_group_user_hash_string(group_id,nowtime_13,x_mt_token):
    ret = '''/v2/msg/group/info
group_id=''' + group_id + '''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:'''+x_mt_token+str(nowtime_13) + '''
x-mt-token:'''+x_mt_token+'''
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''

    return (gethash1(ret))


def generate_group_header(user_id,nowtime_13,x_mt_token):
    header = {':authority': 'api.mtoilet.com',
              'x-mt-token': x_mt_token,
              'x-mt-appid': 'mtoilet',
              'x-mt-devtype': 'Redmi Note 3',
              'x-mt-channel': 'ringle',
              'x-mt-version': '2.0.27',
              'x-mt-platform': 'android',
              'x-mt-devid': '742344B46C61',
              'x-mt-rid': x_mt_token+str(nowtime_13),
              'x-mt-sign': generate_group_hash_string(user_id,nowtime_13,x_mt_token),
              'referer': 'http://android.mtoilets.com',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/3.10.0'
              }
    return (header)


def generate_group_user_header(group_id,nowtime_13,x_mt_token):  # hash 根据group id得到user list header
    header = {':authority': 'api.mtoilet.com',
              'x-mt-token': x_mt_token,
              'x-mt-appid': 'mtoilet',
              'x-mt-devtype': 'Redmi Note 3',
              'x-mt-channel': 'ringle',
              'x-mt-version': '2.0.27',
              'x-mt-platform': 'android',
              'x-mt-devid': '742344B46C61',
              'x-mt-rid': x_mt_token+str(nowtime_13),
              'x-mt-sign': generate_group_user_hash_string(group_id,nowtime_13,x_mt_token),
              'referer': 'http://android.mtoilets.com',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/3.10.0'
              }
    return (header)


def get_new_group(user_id,x_mt_token):
    nowtime_13=int(round(time.time() * 1000))
    url = 'https://api.mtoilet.com/v2/account/userinfo/listall?user_id=' + str(user_id) + '&page=1&page_size=30'
    s = requests.Session()
    aaa = s.get(url, headers=generate_group_header(user_id,nowtime_13,x_mt_token))
    content = aaa.content.decode().translate(non_bmp_map)
    bbb = json.loads(content)
    #print(bbb)

    if len(bbb['data']['data'])>0:
        print(user_id, '用户发现了这么多Group', len(bbb['data']['data']))
        for each_one in bbb['data']['data']:
            each = each_one['res_info']
            if each['expire_time'] > int(time.time()):
                g_list[each['group_id']]=[each['name'],each['expire_time']]
                #print(json.dumps(g_list))
                #
                time.sleep(1)
        print((json.dumps(g_list)))
        print(g_list.keys())
        for key in g_list.keys():  # 由 result 变为 result.keys()
            print(g_list[key][1])
            if g_list[key][1]<int(time.time()):
                print('已过时')
                del g_list[key]
                continue
        with open('information.txt',mode='w',encoding='utf-8') as f0:
            f0.write((json.dumps(g_list,ensure_ascii=False,indent=4)))
                        # print([each['group_id'],each['name'],str(each['expire_time'])])
                        # if [each['group_id'],each['name'],str(each['expire_time'])] not in all_group:
                        #
                        #     print(222)
                        #     with open('group.txt', mode='a', encoding='utf-8') as f1:
                        #         f1.writelines(each['group_id']+'||||'+each['name']+'||||'+str(each['expire_time'])+'||||\n')
                        #         print(333,all_group)




                    # txt_content=json.loads(json_content,encoding='utf-8')
                    # for every_group in txt_content:
                    #     g_id,g_name,g_expire_time=every_group['group_id'],every_group['name'],every_group['expire_time']
                    #     if every_group['expire_time']- int(time.time())<0:
                    #         txt_content.remove(every_group)
                    #     print(g_id,g_name,g_expire_time)





            # group_list = []
            # with open('group.txt', mode='r') as f0:
            #     for i in f0:
            #         group_list.append(i.replace('\n', ''))
            #
            # if each['group_id'] not in group_list:
            #     with open('group.txt', mode='a') as f1:
            #         f1.writelines(each['group_id'] + '\n')
            #         # f1.writelines(er_id='+str(user_id))
            #     if each['expire_time'] > int(time.time()):
            #         print(len(group_list))
            #         print(each)
            #         print(each['group_id'], each['expire_time'] - int(time.time()), each['vote'], each['name'],
            #               each['content'], '人数', each['user_count'])


# print(generate_hash_string(90810))

def get_user_of_group(group_id,x_mt_token):
    nowtime_13 = int(round(time.time() * 1000))
    url = 'https://api.mtoilet.com/v2/msg/group/info?group_id=' + group_id
    s = requests.Session()
    aaa = s.get(url, headers=generate_group_user_header(group_id,nowtime_13,x_mt_token))
    content = aaa.content.decode().translate(non_bmp_map)
    bbb = json.loads(content)
    users = bbb['data']['group_info']['users']
    print(group_id, '发现了这么多用户', len(users))
    return (users)


# while (1):
#     x_mt_token='T1g0NwatZMFmtaOJbeLDIGXTwMabENI0u3Ew==.d7b'
#     print('------------------------------------------------------------------------')
#     group_list = []
#
#     with open('group.txt', mode='r') as f:
#         for i in f:
#             group_list.append(i.replace('\n', ''))
#     print(group_list)
#     group_list.reverse()
#     print(group_list[0:10])
g_list={}
x_mt_token='T1g0NwatZMFmtaOJbeLDIGXTwMabENI0u3Ew==.d7b'

with open('information.txt',mode='r',encoding='utf-8') as f2:
    content=json.loads(f2.read())
    # for key in content.keys():
    #     print(key,type(key))

    for each_group_id in content.keys():
        for every_user in get_user_of_group(each_group_id,x_mt_token):

                get_new_group(every_user,x_mt_token)



