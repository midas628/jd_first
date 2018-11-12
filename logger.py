__author__ = 'yangyz'


import logging
logger = logging.getLogger( 'weibo' )
logger.setLevel( logging.DEBUG )

sched_Timer_prepare = "2018-11-12 15:59:56"
sched_Timer         = "2018-11-12 15:59:58"
sched_Timer_stop    = "2018-11-12 16:01:01"
# log format

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# console log
ch = logging.StreamHandler()
ch.setLevel( logging.DEBUG )
ch.setFormatter( formatter )
logger.addHandler(ch)
