# !/usr/bin/python
# -*- coding: utf-8 -*-

import lqjx
import sys
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

#约车时段，全部、上午8-12、下午1-5、晚上5-8
xnsd = ("-1", "812", "15", "58")
#指定想约的教练
jlcbh = ""
uname = ""
passwd = ""

if __name__ == "__main__":
    lq = lqjx.LQJX()
    try:
        if lq.login(uname, passwd):
            while 1:
                cars = lq.get_bookable_car(xnsd[1])
                if 'null_0' in cars:
                    logging.info('没到时间或者没有可预订车辆！')
                else:
                    result = lq.order_car(xnsd[1], jlcbh)
                    print result
                    if u'成功' in result:
                        logging.info('\n 预定成功！')
                        sys.exit(0)
                #增加间隔时间，防止频繁请求，账号被封
                time.sleep(3)
    except KeyboardInterrupt:
        lq.logout()
        logging.info('退出约车系统！')
