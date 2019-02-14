import mt ,json ,time ,threading
from random import randint

def check_active_users():
    start=time.time()
    thread_num=20
    run = mt.app()
    u_list={}
    def getuserlistinfo(blist):
        for eachid in blist:
            try:
                a=run.get_user_info(userid=eachid, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
                active_user_id = str(a['data']['userinfo']['user_id'])
                active_user_online = a['data']['userinfo']['online']
                active_device_id = a['data']['userinfo']['device_id']
                active_device_type = a['data']['userinfo']['device_type']
                active_device_ver = a['data']['userinfo']['ver']
                active_update_time = a['data']['userinfo']['update_time']
                active_alive_hour = int((time.time()-active_update_time)/60)
                #print(active_user_id,active_user_online,active_device_id,active_device_type,active_update_time)
                u_list[active_user_id]=[randint(0,thread_num-1),active_device_id,active_user_online,active_device_type,active_device_ver,active_update_time,int(time.time()),active_alive_hour,'remark']
                if len(u_list)%1000==0:
                    print(int(time.time()-start),len(u_list))
            except:
                pass

    def starttread(alist):
        Thread_list = []

        # 创建并启动线程
        for eachlist in alist:

            p = threading.Thread(target=getuserlistinfo, args=(eachlist,))
            p.start()
            Thread_list.append(p)

        # 让主线程等待子线程执行完成
        for i in Thread_list:
            i.join()
    def readuserlist(thread_num):
        with open('active_userlist.txt', mode='r', encoding='utf-8') as f0:
            a = f0.read()
            b = json.loads(a)
            print(len(b))
            list_fenzu=[]
            for i in range(thread_num):
                list_fenzu.append([])
            for each in list(b.keys()):
                b[each][0] = randint(0, thread_num-1)
                list_fenzu[b[each][0]].append(each)
            return(list_fenzu)
    alist=readuserlist(thread_num)
    starttread(alist)
    with open('active_userlist.txt', mode='w', encoding='utf-8') as f1:
        f1.write((json.dumps(u_list, ensure_ascii=False, indent=4)))
    print('totaltime',int(time.time() - start))



check_active_users()
