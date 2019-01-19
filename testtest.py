
# -*- coding:utf-8 -*-
__author__ = 'daming.ge'

import time,os,subprocess
import urllib.parse,re
import json,sqlite3,requests
import hashlib
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)



import uiautomator2 as u2

d = u2.connect("db32bc40")

def gethash1(content):
    shaa1 = hashlib.sha1()
    shaa1.update(content.encode('utf-8'))
    res = shaa1.hexdigest()
    #print("sha1采用encode转换加密结果:",res)
    return(res)

def generate_group_hash_string(user_id):
    ret='''/v2/account/userinfo/listall
page=1&page_size=30&user_id='''+str(user_id)+'''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474'''+'1547857723304'+'''
x-mt-token:T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''
    
    return(gethash1(ret))


def generate_group_user_hash_string(group_id):
    ret='''/v2/msg/group/info
group_id='''+group_id+'''
x-mt-appid:mtoilet
x-mt-channel:ringle
x-mt-devid:742344B46C61
x-mt-devtype:Redmi Note 3
x-mt-platform:android
x-mt-rid:T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474'''+'1547857723304'+'''
x-mt-token:T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474
x-mt-version:2.0.27
x-mt-appid;x-mt-channel;x-mt-devid;x-mt-devtype;x-mt-platform;x-mt-rid;x-mt-token;x-mt-version
da39a3ee5e6b4b0d3255bfef95601890afd80709
c3cfba79efd8f1c0f77473ec4a3818ac'''
    
    return(gethash1(ret))

def generate_group_header(user_id):
    header={':authority':'api.mtoilet.com',
'x-mt-token':'T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474',
'x-mt-appid':'mtoilet',
'x-mt-devtype':'Redmi Note 3',
'x-mt-channel':'ringle',
'x-mt-version':'2.0.27',
'x-mt-platform':'android',
'x-mt-devid':'742344B46C61',
'x-mt-rid':'T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.4741547857723304',
'x-mt-sign':generate_group_hash_string(user_id),
'referer':'http://android.mtoilets.com',
'accept-encoding':'gzip',
'user-agent':'okhttp/3.10.0'
}
    return(header)

def generate_group_user_header(group_id):
    header={':authority':'api.mtoilet.com',
'x-mt-token':'T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.474',
'x-mt-appid':'mtoilet',
'x-mt-devtype':'Redmi Note 3',
'x-mt-channel':'ringle',
'x-mt-version':'2.0.27',
'x-mt-platform':'android',
'x-mt-devid':'742344B46C61',
'x-mt-rid':'T1g0NwatZMFmtaOJbcIGFWC6e9siCoqYBLuA==.4741547857723304',
'x-mt-sign':generate_group_user_hash_string(group_id),
'referer':'http://android.mtoilets.com',
'accept-encoding':'gzip',
'user-agent':'okhttp/3.10.0'
}
    return(header)
    

def get_new_group(user_id):
    #print(userid)
    url='https://api.mtoilet.com/v2/account/userinfo/listall?user_id='+str(user_id)+'&page=1&page_size=30'
    #print(url)
    s=requests.Session()
    aaa=s.get(url,headers=generate_group_header(user_id))
    content=aaa.content.decode().translate(non_bmp_map)
    bbb=json.loads(content)
    print(len(bbb['data']['data']))
    for each_one in bbb['data']['data']:
        each=each_one['res_info']
        print(each['group_id'],each['expire_time']-int(time.time()),each['vote'])
        

        
with open('group.txt',mode='r' ) as f0:
            for i in f0:
                group_list.append(i.replace('\n',''))
            print(len(group_list))
        if each['group_id'] not in group_list:
            with open('group.txt',mode='a') as f1:
                f1.writelines(each['group_id']+'\n')
                f1.writelines(er_id='+str(user_id))
            if each['expire_time']>int(time.time()):
                clip_content='adb shell am broadcast -a clipper.set -e text \"'+each['group_id']+'\"'
                out = os.popen(clip_content)
                print(out)
                time.sleep(3)

                if each['vote']==1:
                    try:
                        d.app_start("com.yunge.mtoilets")

                    
                        if d(resourceId="com.yunge.mtoilets:id/bt_submit").wait(3):
                            print("点击投票")
                            d.click(514, 741)
                            time.sleep(0.5)
                            d(resourceId="com.yunge.mtoilets:id/bt_submit").click()
                            time.sleep(1)
                            if d(resourceId="com.yunge.mtoilets:id/bt_submit").wait(3):
                                d(resourceId="com.yunge.mtoilets:id/bt_submit").click()
                                if d(resourceId="com.yunge.mtoilets:id/iv_close").wait(3):
                                    d(resourceId="com.yunge.mtoilets:id/iv_close").click
                                    
                                    print("搞定1类型")
                                    time.sleep(1)
                                    d.press("home")
                        else:
                            d.press("home")

                    except:
                        pass
                else:

                    try:
                        d.app_start("com.yunge.mtoilets")

                    
                        if d(resourceId="com.yunge.mtoilets:id/tv_late").wait(3):
                            

                            clip_content='adb shell am broadcast -a clipper.set -e text \"0\"'
                            out = os.popen(clip_content)
                            
                            print("点击投票")
                            d(resourceId="com.yunge.mtoilets:id/tv_late").click()
                            time.sleep(2)
                            if d(resourceId="com.yunge.mtoilets:id/embedded_text_editor").wait(3):
                                d(resourceId="com.yunge.mtoilets:id/embedded_text_editor").set_text("大家好呀，欢迎互相关注")
                                
                                time.sleep(0.5)
                                d(resourceId="com.yunge.mtoilets:id/bt_send").click()
                                time.sleep(0.5)
                                d(resourceId="com.yunge.mtoilets:id/bt_send").click()
                                if d(resourceId="com.yunge.mtoilets:id/iv_close").wait(3):
                                    d(resourceId="com.yunge.mtoilets:id/iv_close").click
                                    print("搞定0类型")
                                    time.sleep(1)
                                    d.press("home")
                        else:
                            d.press("home")

                    except:
                        pass

        
#print(generate_hash_string(90810))

def get_user_of_group(group_id):
    url='https://api.mtoilet.com/v2/msg/group/info?group_id='+group_id
    s=requests.Session()
    aaa=s.get(url,headers=generate_group_user_header(group_id))
    content=aaa.content.decode().translate(non_bmp_map)
    bbb=json.loads(content)
    users=bbb['data']['group_info']['users']
    return(users)

group_list=[]

with open('group.txt',mode='r' ) as f:
    for i in f:
        group_list.append(i.replace('\n',''))
    print(group_list)
#get_new_group(566670)




#for each group_id in group_list:
    #for every_user in get_user_of_group(each group_id):
        #get_new_group(every_user)
    
    #print('-------------------------------------------------------------------------------')
#os.system('''adb shell am broadcast -a clipper.set -e text "g.6V6Xo6ZHrfg365"''')
#out = os.popen('adb shell am broadcast -a clipper.set -e text "g.GVt0a2tctgk475"').read() #os.popen支持读取操作
#out = os.popen('adb shell am broadcast -a clipper.get').read()
#print(out)
