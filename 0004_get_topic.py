import mt ,json ,time ,threading
from random import randint

def check_active_group():
    start=time.time()
    thread_num=20
    run = mt.app()
    g_list={}
    u_list=[]

    def getusergroup(blist):
        print('我的任务数量',len(blist))
        for eachid in blist:
            u_list.append(eachid)
            try:
                a=run.get_group_of_user(userid=eachid, devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
                #print(a)
                if len(a['data']['data'])>0:
                    for each in a['data']['data']:


                        topic_id=each['res_info']['id']
                        topic_group_id = each['res_info']['group_id']
                        topic_name = each['res_info']['name']
                        topic_content = each['res_info']['content']
                        topic_usercount = each['res_info']['user_count']
                        topic_ip = each['res_info']['ip']
                        topic_owner = each['res_info']['owner']
                        topic_users= each['res_info']['users']
                        topic_redpacket_time = each['res_info']['expire_time']
                        #print(topic_id,topic_group_id,topic_name,topic_content,topic_usercount,topic_ip,topic_owner,topic_users,topic_redpacket_time)
                        g_list[str(topic_id)] = [topic_group_id,topic_name,topic_content,topic_usercount,topic_ip,topic_owner,topic_users,topic_redpacket_time,int(time.time())]
                if(len(u_list))%1000==0:
                    print(run.get_now,int(time.time()-start),len(u_list),len(g_list))

            except:
                pass

                #print(g_list)



    def starttread(alist):
        Thread_list = []

        # 创建并启动线程
        for eachlist in alist:

            p = threading.Thread(target=getusergroup, args=(eachlist,))
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
            glist_fenzu = []
            for i in range(thread_num):
                glist_fenzu.append([])
            for each in list(b.keys()):
                b[each][0] = randint(0, thread_num - 1)
                try:
                    if b[each][7] < 4320:
                        glist_fenzu[b[each][0]].append(each)
                except:
                    glist_fenzu[b[each][0]].append(each)
            return (glist_fenzu)

    alist=readuserlist(thread_num)
    starttread(alist)

    with open('active_group.txt', mode='w', encoding='utf-8') as f1:
        f1.write((json.dumps(g_list, ensure_ascii=False, indent=4)))
    with open('record_group.txt', mode='a', encoding='utf-8') as f2:
        f2.write(str(int(time.time()))+','+(json.dumps(g_list, ensure_ascii=False)))

    print('totaltime',int(time.time() - start))
    for eachid in list(g_list.keys()):


        aa = run.get_group_info(groupid=g_list[eachid][0], devid='742344B46C61', devtype='Redmi Note 3',token='T1g0N+PYcYQ2taOJaMKTdRWpl487kkCdlzZw==.6cc')
        print(aa)
        users=aa['data']['group_info']['users']
        with open('active_userlist.txt', mode='r', encoding='utf-8') as f3:
            aaa = f3.read()
            bbb = json.loads(aaa)
        for each_group_users in users:
            if str(each_group_users) not in u_list:
                print(str(each_group_users))
                bbb[str(each_group_users)]=[1]
        with open('active_userlist.txt', mode='w', encoding='utf-8') as f4:
            f4.write((json.dumps(bbb, ensure_ascii=False, indent=4)))

        #print(len((aa['data']['group_info']['users'])),len((aa['data']['group_info']['users']).append(aa['data']['group_info']['owner'])),aa['data']['group_info']['users'])


#check_active_users()


while(1):
    check_active_group()
    time.sleep(1200)
