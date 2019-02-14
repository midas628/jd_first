
# !-*-coding:utf-8 -*-
# @TIME    : 2019/2/11/00 20 11:20
# @Author  : GDM

import time ,json ,sys
import config ,hashlib ,requests
import logging
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


class app():
    def __init__(self):
        self.x_mt_appid = config.x_mt_appid
        self.x_mt_channel = config.x_mt_channel
        self.x_mt_devid = config.x_mt_devid
        self.x_mt_devtype = config.x_mt_devtype
        self.x_mt_rid_none= config.x_mt_rid_none
        self.x_mt_token_str_none = config.x_mt_token_str_none
        self.x_mt_platform = config.x_mt_platform
        self.x_mt_version = config.x_mt_version
        self.sequence = config.sequence
        self.code1 = config.code1
        self.code2 = config.code2
        self.version = config.version

        self._log = None
        self._init_log()

    def _init_log(self):
        self._log = logging.getLogger(__name__)
        self._log.setLevel(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        handler = logging.FileHandler("app.log",encoding='utf-8')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self._log.addHandler(handler)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self._log.addHandler(console)

    # SHA1加密
    def get_now(self):
        return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    def gethash1(self,content):
        shaa1 = hashlib.sha1()
        shaa1.update(content.encode('utf-8'))
        res = shaa1.hexdigest()
        return res

    # 发送验证码
    def send_sms(self,tel,devid='742344B46C61',devtype='Redmi Note 3'):
        path='/v2/account/sms/send'
        url = 'https://api.mtoilet.com/v2/account/sms/send'
        nowtime_13 = str(int(round(time.time() * 1000)))
        # nowtime_13='1549896307923'
        data = {"tel": tel,"type": 0}
        xd = str(data).replace('\'', '\"').replace(' ', '')
        data_str = bytes(xd, encoding='utf-8')  # 此处如果没有bytes,post的数据SHA1会出现错误
        self.code0 = self.gethash1(xd)
        # self._log.info('send_sms data==>对应SHA1为%s==>%s' % (data, self.code0))

        self.x_mt_token_str=self.x_mt_token_str_none
        self.x_mt_rid = self.x_mt_rid_none+nowtime_13
        sha1_str_send_sms = '\n'.join([path +'\n',
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code0,
                                       self.code2])
        sha1_str_send_sms_result=self.gethash1(sha1_str_send_sms)
        # self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_str_send_sms, sha1_str_send_sms_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': 'NONE',
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': 'NONE'+nowtime_13,
            'x-mt-sign': sha1_str_send_sms_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.post(url,headers=header,data=data_str)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('手机号%s请求发送验证码失败，失败信息为%s' %(tel,str(result_json)))
        else:
            self._log.info('手机号%s请求发送验证码成功,返回信息为%s' % (tel,str(result_json)))
        return(result_json)
    #验证码登录获取token
    def sms_login(self,tel,smscode,devid='742344B46C61',devtype='Redmi Note 3'):
        path='/v2/account/login/sms'
        url = 'https://api.mtoilet.com/v2/account/login/sms'
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'
        data = {"code": smscode,"tel": tel}
        xd = str(data).replace('\'', '\"').replace(' ', '')
        data_str = bytes(xd, encoding='utf-8')  #此处如果没有bytes,post的数据SHA1会出现错误
        self.code0 = self.gethash1(xd)
        #self._log.info('send_sms data==>对应SHA1为%s==>%s' % (data, self.code0))

        self.x_mt_token_str=self.x_mt_token_str_none
        self.x_mt_rid = self.x_mt_rid_none+nowtime_13
        sha1_str_sms_login = '\n'.join([path +'\n',
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code0,
                                       self.code2])
        sha1_str_sms_login_result=self.gethash1(sha1_str_sms_login)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_str_sms_login, sha1_str_sms_login_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': 'NONE',
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': 'NONE'+nowtime_13,
            'x-mt-sign': sha1_str_sms_login_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.post(url,headers=header,data=data_str)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('手机号%s使用验证码%s登录失败，失败信息为%s' %(tel,smscode,str(result_json)))
        else:
            self._log.info('手机号%s使用验证码%s登录成功，登录信息为%s' % (tel, smscode, str(result_json)))
            self._log.info('手机号%s使用验证码%s登录成功，token为%s' % (tel, smscode, result_json['data']['token']))
        return(result_json)
    #报告服务器保持在线
    def keepalive(self,devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/msg/keepalive'
        url = 'https://api.mtoilet.com/v2/msg/keepalive'
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'
        data = {"lat": 31.20503716362847,"lng": 121.58802029079861}
        xd = str(data).replace('\'', '\"').replace(' ', '')
        data_str = bytes(xd, encoding='utf-8')  #此处如果没有bytes,post的数据SHA1会出现错误
        self.code0 = self.gethash1(xd)
        #self._log.info('send_sms data==>对应SHA1为%s==>%s' % (data, self.code0))

        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_str_keepalive = '\n'.join([path +'\n',
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code0,
                                       self.code2])
        sha1_str_keepalive_result=self.gethash1(sha1_str_keepalive)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_str_keepalive, sha1_str_keepalive_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_str_keepalive_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.post(url,headers=header,data=data_str)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('账号%s keepalive失败，失败信息为%s' %(token,str(result_json)))
        else:
            self._log.info('账号%s keepalive成功，返回信息为%s' % (token,str(result_json)))
        return(result_json)
    #查询userid余额
    def get_user_money(self,userid='571551',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/usermoney?user_id='+userid
        url = 'https://api.mtoilet.com/v2/usermoney?user_id='+userid
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_user_money = '\n'.join(['/v2/usermoney',
                                       'user_id='+userid,
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_user_money_result=self.gethash1(sha1_get_user_money)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_user_money, sha1_get_user_money_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_user_money_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('账号%s 余额查询失败，失败信息为%s' %(userid,str(result_json)))
        else:

            self._log.info('账号%s 余额查询成功，返回信息为%s' % (userid,str(result_json)))
            self._log.info('账号%s 余额查询成功，当前余额为%s元' % (userid, str(result_json['data']['money']/100)))
        return(result_json)
    #查询userid信息
    def get_user_info(self,userid='571551',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/account/userinfo/get?user_id='+userid
        url = 'https://api.mtoilet.com/v2/account/userinfo/get?user_id='+userid
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_user_info = '\n'.join(['/v2/account/userinfo/get',
                                       'user_id='+userid,
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_user_info_result=self.gethash1(sha1_get_user_info)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_user_info, sha1_get_user_info_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_user_info_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('账号%s 信息查询失败，失败信息为%s' %(userid,str(result_json)))
        else:
            pass

            #self._log.info('账号%s 信息查询成功，返回信息为%s' % (userid,str(result_json)))
        return (result_json)

    #查询userid参与的话题
    def get_group_of_user(self,userid='571551',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/account/userinfo/listall?user_id='+userid+'&page=1&page_size=30'
        url = 'https://api.mtoilet.com/v2/account/userinfo/listall?user_id='+userid+'&page=1&page_size=30'

        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_user_info = '\n'.join(['/v2/account/userinfo/listall',
                                       'page=1&page_size=30&user_id='+userid,
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_user_info_result=self.gethash1(sha1_get_user_info)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_user_info, sha1_get_user_info_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_user_info_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('账号%s 参与的话题信息查询失败，失败信息为%s' %(userid,str(result_json)))
        else:
            pass
            #self._log.info('账号%s 参与的话题信息查询成功，返回信息为%s' % (userid,str(result_json)))
        return (result_json)



   #查询group id 信息
    def get_group_info(self,groupid='g.C6nLrvTXYRo433',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/msg/group/info?group_id='+groupid
        url = 'https://api.mtoilet.com/v2/msg/group/info?group_id='+groupid

        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_user_info = '\n'.join(['/v2/msg/group/info',
                                       'group_id='+groupid,
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_user_info_result=self.gethash1(sha1_get_user_info)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_user_info, sha1_get_user_info_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_user_info_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result.content.decode().translate(non_bmp_map)
        #result_json=json.loads(result.content)
        result_json = json.loads(result.content.decode().translate(non_bmp_map))
        if result_json['ok']!=True:
            self._log.info('话题%s ,token %s信息查询失败，失败信息为%s' %(groupid,token,str(result_json)))
        else:
            pass

            #self._log.info('话题%s ,token %s信息查询成功，返回信息为%s' % (groupid,token,str(result_json['ok'])))
        return(result_json)

   #查询votecheck
    def get_vote_check(self,groupid='g.C6nLrvTXYRo433',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/msg/group/vote_check?group_id='+groupid
        url = 'https://api.mtoilet.com/v2/msg/group/vote_check?group_id='+groupid


        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_user_info = '\n'.join(['/v2/msg/group/vote_check',
                                       'group_id='+groupid,
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_user_info_result=self.gethash1(sha1_get_user_info)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_user_info, sha1_get_user_info_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_user_info_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result.content.decode().translate(non_bmp_map)
        #result_json=json.loads(result.content)
        result_json = json.loads(result.content.decode().translate(non_bmp_map))
        if result_json['ok']!=True:
            self._log.info('话题%s Votecheck信息查询失败，失败信息为%s' %(groupid,str(result_json)))
        else:

            self._log.info('话题%s Votecheck信息查询成功，返回信息为%s' % (groupid,str(result_json)))
            #self._log.info('账号%s 余额查询成功，当前余额为%s元' % (userid, str(result_json['data']['money']/100)))
        return(result_json)
    #加入话题
    def join_group(self,groupid='g.C6nLrvTXYRo433',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2',vote_option=''):
        path='/v2/msg/group/join'
        url = 'https://api.mtoilet.com/v2/msg/group/join'
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'

        data = {"group_id": groupid,"vote_option": vote_option}
        xd = str(data).replace('\'', '\"').replace(' ', '')
        data_str = bytes(xd, encoding='utf-8')  #此处如果没有bytes,post的数据SHA1会出现错误
        self.code0 = self.gethash1(xd)
        #self._log.info('send_sms data==>对应SHA1为%s==>%s' % (data, self.code0))

        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_str_join_group = '\n'.join([path +'\n',
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code0,
                                       self.code2])
        sha1_str_join_group_result=self.gethash1(sha1_str_join_group)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_str_join_group, sha1_str_join_group_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_str_join_group_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.post(url,headers=header,data=data_str)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('话题%s ,token %s加入失败，失败信息为%s' %(groupid,token,str(result_json['ok'])))
        else:
            self._log.info('话题%s ,token %s加入成功，返回信息为%s' % (groupid,token,str(result_json['ok'])))
        return(result_json)
    #update_talk
    def update_talk(self,userid='571551',groupid='g.C6nLrvTXYRo433',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/msg/group/update'
        url = 'https://api.mtoilet.com/v2/msg/group/update'
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'

        data = {"group_id": groupid,"is_talk": 1,"user_id":int(userid)}
        xd = str(data).replace('\'', '\"').replace(' ', '')
        data_str = bytes(xd, encoding='utf-8')  #此处如果没有bytes,post的数据SHA1会出现错误
        self.code0 = self.gethash1(xd)
        #self._log.info('send_sms data==>对应SHA1为%s==>%s' % (data, self.code0))

        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_str_update_talk = '\n'.join([path +'\n',
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code0,
                                       self.code2])
        sha1_str_update_talk_result=self.gethash1(sha1_str_update_talk)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_str_update_talk, sha1_str_update_talk_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_str_update_talk_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.post(url,headers=header,data=data_str)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('话题%s ,token %s ,%s UserID UPDATE_TALK失败，失败信息为%s' %(groupid,token,userid,str(result_json['ok'])))
        else:
            self._log.info('话题%s ,token %s ,%s UserID UPDATE_TALK成功，返回信息为%s' % (groupid,token,userid,str(result_json['ok'])))
        return(result_json)
    #余额提现
    def get_money(self,money=2000,devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        path='/v2/usermoney/cashcode?cash_num='+str(money)
        url = 'https://api.mtoilet.com/v2/usermoney/cashcode?cash_num='+str(money)
        nowtime_13 = str(int(round(time.time() * 1000)))
        #nowtime_13='1549896307923'


        self.x_mt_token_str='x-mt-token:'+token
        self.x_mt_rid = 'x-mt-rid:'+token+nowtime_13
        sha1_get_money = '\n'.join(['/v2/usermoney/cashcode',
                                       'cash_num='+str(money),
                                       self.x_mt_appid,
                                       self.x_mt_channel,
                                       self.x_mt_devid+devid,
                                       self.x_mt_devtype+devtype,
                                       self.x_mt_platform,
                                       self.x_mt_rid,
                                       self.x_mt_token_str,
                                       self.x_mt_version,
                                       self.sequence,
                                       self.code1,
                                       self.code2])
        sha1_get_money_result=self.gethash1(sha1_get_money)
        #self._log.info('send_sms sha1_str==>对应SHA1为\n%s\n==>\n%s' % (sha1_get_money, sha1_get_money_result))

        header={
            ':authority': 'api.mtoilet.com',
            'x-mt-token': token,
            'x-mt-appid': 'mtoilet',
            'x-mt-devtype': devtype,
            'x-mt-channel': 'ringle',
            'x-mt-version': self.version,
            'x-mt-platform': 'android',
            'x-mt-devid': devid,
            'x-mt-rid': token+nowtime_13,
            'x-mt-sign': sha1_get_money_result,
            'referer': 'http://android.mtoilets.com',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.10.0'
        }
        s=requests.Session()
        result=s.get(url,headers=header)
        result_json=json.loads(result.content)
        if result_json['ok']!=True:
            self._log.info('账号%s 余额提现失败，失败信息为%s' %(token,str(result_json)))
        else:

            self._log.info('账号%s 余额提现成功，返回信息为%s' % (token,str(result_json)))
        return(result_json)

if __name__ == '__main__':
    run = app()
    ss = requests.session()

    def qianghongbao(userid='571551',groupid='g.5xkKgMOZnww357', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2'):
        group_info=run.get_group_info(groupid, devid, devtype,token)
        if group_info['data']['group_info']['vote']==1:
            vote_option='A'
        else:
            vote_option=''
        if int(userid) not in group_info['data']['group_info']['users']:
            run.join_group(groupid,devid,devtype,token,vote_option)
        run.update_talk(userid,groupid, devid, devtype,token)
        run.get_group_info(groupid, devid, devtype,token)

    while(1):
        a = ss.get('http://140.143.243.178/info2.txt')
        b = json.loads(a.content)
        with open('token.txt',mode='r') as f:
            tokenlist=json.loads(f.read())
        #run._log.info('group 集合%s ,token 集合%s' % (str(b), str(tokenlist)))
        for each in list(b.keys()):
            wait_time = b[each][1] - int(time.time())
            run._log.info("ID是%s,话题ID是%s,标题:%s,当前人数%s人,红包金额%s元,剩余时间 %s 秒" % (str(b[each][5]),each, b[each][0],str(b[each][2]),str(b[each][3] / 100.00),str(wait_time)))
            if wait_time>30 and wait_time<50:
                run._log.info('group 集合%s ,token 集合%s' % (str(b), str(tokenlist)))
                for eachuser in list(tokenlist.keys()):
                    userid=eachuser
                    groupid=each
                    devid=tokenlist[eachuser][1]
                    devtype = tokenlist[eachuser][2]
                    token= tokenlist[eachuser][3]
                    #qianghongbao(userid='571551', groupid='g.5xkKgMOZnww357', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
                    print(userid, groupid, devid, devtype, token)
                    try:
                        qianghongbao(userid, groupid, devid,devtype, token)
                    except:
                        pass
                    #run.get_user_money(eachuser, devid, devtype,token)
        run._log.info('----------等待7秒后继续查询-------------')

        time.sleep(7)

    #run.send_sms(tel="15336458684",devid='742344B46C61',devtype='Redmi Note 3')
    #run.sms_login("15336458684", smscode='831561', devid='742344B46C61', devtype='Redmi Note 3')
    #run.keepalive(devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_user_money(userid='571551', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_user_money(userid='511739', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_user_info(userid='511738', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_group_of_user(userid='571551', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_group_info(groupid='g.C6nLrvTXYRo433', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_vote_check(groupid='g.C6nLrvTXYRo433', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.join_group(groupid='g.C6nLrvTXYRo433', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2', vote_option='')

    #run.update_talk(userid='571551',groupid='g.C6nLrvTXYRo433',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')

    #run.get_money(money=2200,devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
    #run.get_user_info(userid='607271', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')


    #run.join_group(groupid='g.l0rKddO9vkM6c3', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2', vote_option='')
    #run.update_talk(userid='571551',groupid='g.l0rKddO9vkM6c3',devid='742344B46C61',devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
    #run.get_group_info(groupid='g.l0rKddO9vkM6c3', devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N/a4sTEmtaOM3demMHCkiSGW5Qb627mQ==.ea2')
