import mt ,json ,time ,threading
from random import randint

def filter_active_users():
    run = mt.app()
    with open('userlist0.txt',mode='r') as f0:
        content = f0.read()
        content_json = json.loads(content)
    print(len(content_json))
    u_list = {}
    n=0
    start_time=time.time()
    print(time.time(), '计数', n)
    for each in list(content_json.keys()):
        #print(each)
        n+=1
        if n%100==0:
            print(int(time.time()-start_time),'计数',n)
        a = run.get_user_info(userid=each, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
        #b = run.get_group_of_user(userid=each, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
        #quantity_group = (len(b['data']['data']))

        active_user_id = a['data']['userinfo']['user_id']
        active_user_online = a['data']['userinfo']['online']
        active_device_id = a['data']['userinfo']['device_id']
        active_device_type = a['data']['userinfo']['device_type']
        active_device_ver = a['data']['userinfo']['ver']
        active_update_time = a['data']['userinfo']['update_time']
        active_alive_hour = int((time.time()-active_update_time)/3600)
        #print(active_user_id,active_user_online,active_device_id,active_device_type,active_update_time)
        u_list[active_user_id]=[active_device_id,active_user_online,active_device_type,active_device_ver,active_update_time,int(time.time()),active_alive_hour,'remark']
        #time.sleep(4)
    with open('information.txt', mode='w', encoding='utf-8') as f0:
        f0.write((json.dumps(u_list, ensure_ascii=False, indent=4)))
        #time.sleep(1)
        #print(len(g_list))
    #
def check_active():
    start=time.time()
    run = mt.app()
    u_list={}
    def getuserlistinfo(blist):
        for eachid in blist:
            a=run.get_user_info(userid=eachid, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
            active_user_id = str(a['data']['userinfo']['user_id'])
            active_user_online = a['data']['userinfo']['online']
            active_device_id = a['data']['userinfo']['device_id']
            active_device_type = a['data']['userinfo']['device_type']
            active_device_ver = a['data']['userinfo']['ver']
            active_update_time = a['data']['userinfo']['update_time']
            active_alive_hour = int((time.time()-active_update_time)/3600)
            #print(active_user_id,active_user_online,active_device_id,active_device_type,active_update_time)
            u_list[active_user_id]=[randint(1,3),active_device_id,active_user_online,active_device_type,active_device_ver,active_update_time,int(time.time()),active_alive_hour,'remark']
            if len(u_list)%100==0:
                print(int(time.time()-start),len(u_list))


    def starttread(alist):
        Thread_list = []

        # 创建并启动线程
        for eachlist in alist:

            #p = main0(eachlist)
            p = threading.Thread(target=getuserlistinfo, args=(eachlist,))
            p.start()
            Thread_list.append(p)

        # 让主线程等待子线程执行完成
        for i in Thread_list:
            i.join()


    def readuserlist():

        with open('userlist1.txt', mode='r', encoding='utf-8') as f0:
            a=f0.read()
            b=json.loads(a)
            a1,a2,a3,a4,a5=[],[],[],[],[]
            for each in list(b.keys()):
                if b[each][0]==1:
                    a1.append(each)
                elif b[each][0]==2:
                    a2.append(each)
                elif b[each][0]==3:
                    a3.append(each)
                elif b[each][0]==4:
                    a4.append(each)
                elif b[each][0]==5:
                    a5.append(each)
            #print(a1,a2,a3,a4,a5)
            return[a1,a2,a3,a4,a5]
            #time.sleep(1)
            #print(len(g_list))

    alist=readuserlist()
    starttread(alist)
    #print(u_list)
    with open('userlist2.txt', mode='w', encoding='utf-8') as f1:
        f1.write((json.dumps(u_list, ensure_ascii=False, indent=4)))

#check_active()


def check_active_users():
    start=time.time()
    run = mt.app()
    u_list={}
    def getuserlistinfo(blist):
        for eachid in blist:
            a=run.get_user_info(userid=eachid, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
            active_user_id = str(a['data']['userinfo']['user_id'])
            active_user_online = a['data']['userinfo']['online']
            active_device_id = a['data']['userinfo']['device_id']
            active_device_type = a['data']['userinfo']['device_type']
            active_device_ver = a['data']['userinfo']['ver']
            active_update_time = a['data']['userinfo']['update_time']
            active_alive_hour = int((time.time()-active_update_time)/60)
            #print(active_user_id,active_user_online,active_device_id,active_device_type,active_update_time)
            u_list[active_user_id]=[randint(1,3),active_device_id,active_user_online,active_device_type,active_device_ver,active_update_time,int(time.time()),active_alive_hour,'remark']
            if len(u_list)%100==0:
                print(int(time.time()-start),len(u_list))

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
    def readuserlist(thread_num=20):
        with open('userlist1.txt', mode='r', encoding='utf-8') as f0:
            a = f0.read()
            b = json.loads(a)
            list_fenzu=[]
            for i in range(thread_num):
                list_fenzu.append([])
            for each in list(b.keys()):
                b[each][0] = randint(0, thread_num-1)
                list_fenzu[b[each][0]].append(each)
            with open('userlist2.txt', mode='w', encoding='utf-8') as f1:
                f1.write((json.dumps(b, ensure_ascii=False, indent=4)))
            return(list_fenzu)
    alist=readuserlist(thread_num=10)
    starttread(alist)
    with open('userlist2.txt', mode='w', encoding='utf-8') as f1:
        f1.write((json.dumps(u_list, ensure_ascii=False, indent=4)))

def temp():
    with open('userlist2.txt', mode='r', encoding='utf-8') as f0:
        a = f0.read()
        b = json.loads(a)
        print(len(b))
        for each in list(b.keys()):
            b[each][0]=randint(1,5)
        with open('userlist3.txt', mode='w', encoding='utf-8') as f1:
            f1.write((json.dumps(b, ensure_ascii=False, indent=4)))


check_active_users()
