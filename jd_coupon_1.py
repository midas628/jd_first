__author__ = 'yangyz'


from logger import logger
import requests ,json
import datetime ,time


user_agent = (
      'User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
)
session = requests.session()
session.headers['User-Agent'] = user_agent

##将浏览器中能看到的cookie转化为python中的字典
def get_cookie():
    with open("cookie.txt") as f:
        cookies={}
        for line in f.read().split(';'):
            name,value=line.strip().split('=',1)
            cookies[name]=value
        #print(cookies)
        return cookies

##抢优惠券
def getCoupon():
    sched_Timer="2018-10-26 16:19:59" ##配置抢券的时间
    ##配置要抢购的券的url  在浏览器的Network中找
    couPonUrl="https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%22mob5gedpAL8X3AkSLwK6JcvoMrN%22%2C%22from%22%3A%22H5node%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D1a09621df6fd49cd8989381fc13f9d70%2CroleId%3D15155152%22%2C%22platform%22%3A%223%22%2C%22orgType%22%3A%222%22%2C%22openId%22%3A%22-1%22%2C%22pageClickKey%22%3A%22Babel_Coupon%22%2C%22eid%22%3A%22XUMINDP74DCW3Z4T7L5ZNBONQXNUGLCRZIE2AWUP5QMMBL5SDFD5CZCLKDV46ONS4K5MLF5KNSXBPNA3MW3T43ACUY%22%2C%22fp%22%3A%22e79036f62acaee7f417c07b2a12db9a4%22%2C%22shshshfp%22%3A%223330fb5cacbd509cb23ac45868d3dd98%22%2C%22shshshfpa%22%3A%22efbf1ad3-6a43-69be-aa38-5b672e1e6845-1538983902%22%2C%22shshshfpb%22%3A%2225eef18bfc1984857b8b953de42c1f3d95b4ff5144a0f8407562b73e45%22%2C%22childActivityUrl%22%3A%22https%253A%252F%252Fpro.m.jd.com%252Fmall%252Factive%252Fmob5gedpAL8X3AkSLwK6JcvoMrN%252Findex.html%253Futm_campaign%253D%2526utm_source%253D%2526utm_term%253D%2526utm_medium%253D%22%2C%22mitemAddrId%22%3A%2213_1042_51029_51030%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%2C%22addressId%22%3A%22138120295%22%2C%22posLng%22%3A%22121.184%22%2C%22posLat%22%3A%2237.573%22%2C%22focus%22%3A%22%22%2C%22innerAnchor%22%3A%22%22%7D&client=wh5&clientVersion=1.0.0&sid=2c90538b5336c48ec32d36123213a3d0&uuid=15389838999881107232128&area=13_1042_51029_51030"
    ##配置要抢购的券的referer  在浏览器的Network中找
    referer="https://pro.m.jd.com/mall/active/mob5gedpAL8X3AkSLwK6JcvoMrN/index.html?utm_campaign=&utm_source=&utm_term=&utm_medium="
    cj = requests.utils.cookiejar_from_dict(get_cookie())
    session.cookies = cj
    while(1):
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        print(now)
        if now==sched_Timer:
            while(1):
        #if 1==1:

                resp=session.get(
                              url=couPonUrl,
                              headers={
                             'Referer':referer ,
                           }
                            )
                logger.info(resp.text)
                #time.sleep(0.1)
            #break

def getCouponlist():
                url='https://s.m.jd.com/activemcenter/mcouponcenter/selectcouponlist?pagenum=1&pagesize=10&_=1540440345510&sceneval=2&g_login_type=1&callback=jsonpCBKC&g_tk=358046892&g_ty=ls'
                referer='https://coupon.m.jd.com/center/getCouponCenter.action'
                cj = requests.utils.cookiejar_from_dict(get_cookie())
                session.cookies = cj
                resp=session.get(
                              url=url,
                              headers={
                             'Referer':referer ,
                           }
                            )
                #print(resp.text.replace('try{ jsonpCBKC(','').replace(');}catch(e){}',''))
                a=json.loads(resp.text.replace('try{ jsonpCBKC(','').replace(');}catch(e){}',''))
                print(len(a))
                for i in  a['couponItem']:
                    print(i.keys())
                    print('------------------------')
                #logger.info(resp.text)
if __name__ == '__main__':
    getCoupon()
    #getCouponlist()


