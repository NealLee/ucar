# -*- coding: utf-8 -*-

import requests
import datetime
import time
import logging

LQJX_HOST = "http://106.37.230.254:81"
lq_session = requests.Session()


class LQJX:

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
    }

    def __init__(self):
        pass

    def login(self, uname, passwd):
        post_data = {
            '__VIEWSTATE': '/wEPDwUKMTg0NDI4MDE5OGRkj8OrkkOlfYqdhxkeEVV4GsZ6FLw0IioIcl+nbwqoGbo=',
            '__EVENTVALIDATION': '/wEWBgKF6pivDAKl1bKzCQK1qbSRCwLoyMm8DwLi44eGDAKAv7D9Co04a1vpmJ/QuWDi2GFypJ8LBXRdxHsgxKaj/eIzgMJ6',
            'txtUserName': uname,
            'txtPassword': passwd,
            'BtnLogin': '登  录',
            'rcode': ''
        }
        result = lq_session.post(LQJX_HOST + '/login.aspx', data=post_data, headers=self.header)
        if 'zhxx.aspx' in result.text:
            logging.info("登录成功!")
            flag = True
        else:
            logging.error("登录失败，请检查账号状态或请求参数!")
            flag = False
        return flag
        
    def logout(self):
        lq_session.get(LQJX_HOST + '/Login.aspx?LoginOut=true', headers=self.header)    

    def order_car(self, xnsd, jlcbh):
        query_param = {
            'jlcbh': jlcbh,  #教练场编号
            'yyrqbegin': str(datetime.date.today() + datetime.timedelta(13)).replace('-', ''),  #预约14天后
            'xnsd': xnsd,  #时段 -1  812  15  58
            'trainType': '3',  #原地1 道路3 实际4
            'type': 'km2Car2',  #约车类型 科目二km2Car2
            '_': int(time.time())  #时间戳
        }
        return lq_session.get(LQJX_HOST + "/Tools/km2.aspx?", params=query_param, headers=self.header).text

    def get_bookable_car(self, xnsd):
        base_url = LQJX_HOST + "/Tools/km2.aspx?date=" + str(datetime.datetime.now())
        query_param = {
            'filters[yyrq]': str(datetime.date.today() + datetime.timedelta(13)).replace('-', ''),
            'filters[xnsd]': xnsd,
            'filters[xllxid]': '3',
            'filters[type]': 'km2Car',
            'filters[cnbh]': '', #场内编号，不填写则为全部
            'pageno': '1',
            'pagesize': '30',
            '_': int(time.time())
        }
        return lq_session.get(base_url, params=query_param).text

if __name__ == "__main__":
    pass

