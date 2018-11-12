from logger import logger
from logger import sched_Timer,sched_Timer_prepare,sched_Timer_stop
import requests ,json
import datetime ,time

user_agent = ('User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5')
session = requests.session()
session.headers['User-Agent'] = user_agent

def get_cookie():
    with open("cookie.txt") as f:
        cookies={}
        for line in f.read().split(';'):
            name,value=line.strip().split('=',1)
            cookies[name]=value
        return cookies


couPonUrl='https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%222QzmFRVocC28jaS935KqeqjRGAwv%22%2C%22from%22%3A%22H5node%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3Dfc43cc24f06b4839af5920974bd4775c%2CroleId%3D15284874%22%2C%22platform%22%3A%223%22%2C%22orgType%22%3A%222%22%2C%22openId%22%3A%22-1%22%2C%22pageClickKey%22%3A%22Babel_Coupon%22%2C%22eid%22%3A%22YJUC2TEKPNCL2CXT6GWK6YSHI3CJRZQVV2FJTZ3O2UJCUWQWJMPO6QUYKEUSX2RN6FC3HUOZQR5XAR62O5KJWAZTKQ%22%2C%22fp%22%3A%229f97b0d1ff28852911d6de16529aac88%22%2C%22shshshfp%22%3A%227910f54b57efdd3160610f0371dd5a26%22%2C%22shshshfpa%22%3A%220acade66-e576-73e2-ef50-8d0b86a5920e-1540901013%22%2C%22shshshfpb%22%3A%221c1e588965f764cc581638b900f7389124642c20077bec4f15bd848969%22%2C%22childActivityUrl%22%3A%22https%253A%252F%252Fpro.m.jd.com%252Fmall%252Factive%252F2QzmFRVocC28jaS935KqeqjRGAwv%252Findex.html%253Futm_campaign%253D%2526utm_source%253D%2526utm_term%253D%2526utm_medium%253D%22%2C%22mitemAddrId%22%3A%2213_1042_51029_51030%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%2C%22addressId%22%3A%22138120295%22%2C%22posLng%22%3A%22121.184%22%2C%22posLat%22%3A%2237.573%22%2C%22focus%22%3A%22%22%2C%22innerAnchor%22%3A%22%22%7D&client=wh5&clientVersion=1.0.0&sid=435de3151d21380080a73bc6909947ea&uuid=1540901009569571937959&area=13_1042_51029_51030'
referer='https://pro.m.jd.com/mall/active/2QzmFRVocC28jaS935KqeqjRGAwv/index.html?utm_campaign=&utm_source=&utm_term=&utm_medium='
name='厨房99-88'
cj = requests.utils.cookiejar_from_dict(get_cookie())
session.cookies = cj
def getCoupon():

    while(1):
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now==sched_Timer:
            while(1):
                resp=session.get(
                              url=couPonUrl,
                              headers={
                             'Referer':referer ,
                           }
                            )                
                logger.info('抢券时间'+resp.text)
                now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if now==sched_Timer_stop:
                    return(1)
        else:
                resp=session.get(
                              url=couPonUrl,
                              headers={
                             'Referer':referer ,
                           }
                            )
                logger.info('准备时间'+resp.text)            
                time.sleep(0.5)

if __name__ == '__main__':

    print(quan)

    resp=session.get(
                              url=couPonUrl,
                              headers={
                             'Referer':referer ,
                           }
                            )
    logger.info('测试时间'+resp.text)    
    while(1):
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        if now==sched_Timer_prepare:            
            getCoupon()
        else:
            logger.info('待机时间')
            time.sleep(0.8)
