# #coding=gbk
import json

import numpy as np
import pymysql
from config import db
import pandas as pd
"""
����ͼר�����ڴ���ajax����
"""
from flask import Blueprint

data = Blueprint('data', __name__)


def query():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select houses_area,houses_TotalPrice from price_analysis')
    area = ["'����'", "'�山'", "'�ϰ�'", "'����'", "'ɳƺ��'", "'������'", "'����'", "'��ɿ�'", "'����'"]

    Price_info=cursor.fetchall()
    Price_area = pd.DataFrame(list(Price_info), columns=["houses_area",'houses_TotalPrice'])

    data_total={}
    for i in area:
        query = i + "in houses_area"  # ���ò�ѯʱ���ַ���
        data_query = Price_area.query(query)  # �ҳ������������
        if eval(i) == "����":
            data_jiangbei=data_query.values
            data_total['data_jiangbei']=data_jiangbei
        else:
            if eval(i)=="�山":
                data_yubei=data_query.values
                data_total['data_yubei']=data_yubei
            else:
                if eval(i) == "�ϰ�":
                    data_nanan = data_query.values
                    data_total['data_nanan'] = data_nanan
                else:
                    if eval(i)=="����":
                        data_yuzhong=data_query.values
                        data_total['data_yuzhong']=data_yuzhong
                    else:
                        if eval(i)=="ɳƺ��":
                            data_shapingba=data_query.values
                            data_total['data_shapingba']=data_shapingba
                        else:
                            if eval(i)=="������":
                                data_jiulongpo=data_query.values
                                data_total['data_jiulongpo']=data_jiulongpo
                            else:
                                if eval(i)=="����":
                                    data_banan=data_query.values
                                    data_total['data_banan']=data_banan
                                else:
                                    if eval(i)=="��ɿ�":
                                        data_dadukou=data_query.values
                                        data_total['data_dadukou']=data_dadukou
                                    else:
                                        if eval(i)=="����":
                                            data_beibei=data_query.values
                                            data_total['data_beibei']=data_beibei
    return data_total



@data.route("/getPriceAmount",methods=['GET'])
def get_Price_Amount():
    data_total=query()
    UnderThirty = 0
    ThirtyToSixty = 0
    SixtyToHundred = 0
    HundredToHfifty = 0
    HfiftyToTHundred = 0
    AboveTHundred = 0
    for i in data_total:
        for t in data_total[i]:
            if float(t[1].split('��')[0])<30:
                UnderThirty+=1
            else:
                if float(t[1].split('��')[0])<60 and float(t[1].split('��')[0])>=30:
                    ThirtyToSixty +=1
                else:
                    if float(t[1].split('��')[0])>=60 and float(t[1].split('��')[0])<100:
                        SixtyToHundred+=1
                    else:
                        if float(t[1].split('��')[0]) >= 100 and float(t[1].split('��')[0]) < 150:
                            HundredToHfifty+=1
                        else:
                            if float(t[1].split('��')[0]) >= 150 and float(t[1].split('��')[0]) < 200:
                                HfiftyToTHundred+=1
                            else:
                                if float(t[1].split('��')[0]) >= 200:
                                    AboveTHundred+=1
    price_amount_all={
        'UnderThirty':UnderThirty,
        'ThirtyToSixty':ThirtyToSixty,
        'SixtyToHundred':SixtyToHundred,
        'HundredToHfifty':HundredToHfifty,
        'HfiftyToTHundred':HfiftyToTHundred,
        'AboveTHundred':AboveTHundred
    }
    price_amount_all=json.dumps(price_amount_all)
    return price_amount_all

@data.route("/getPrice",methods=['GET'])
def get_Price():
    # cursor = getdb()
    data_total=query()
    for i in data_total:
        UnderThirty = 0
        ThirtyToSixty = 0
        SixtyToHundred = 0
        HundredToHfifty = 0
        HfiftyToTHundred = 0
        AboveTHundred = 0
        for t in data_total[i]:
            if float(t[1].split('��')[0])<30:
                UnderThirty+=1
            else:
                if float(t[1].split('��')[0])<60 and float(t[1].split('��')[0])>=30:
                    ThirtyToSixty +=1
                else:
                    if float(t[1].split('��')[0])>=60 and float(t[1].split('��')[0])<100:
                        SixtyToHundred+=1
                    else:
                        if float(t[1].split('��')[0]) >= 100 and float(t[1].split('��')[0]) < 150:
                            HundredToHfifty+=1
                        else:
                            if float(t[1].split('��')[0]) >= 150 and float(t[1].split('��')[0]) < 200:
                                HfiftyToTHundred+=1
                            else:
                                if float(t[1].split('��')[0]) >= 200:
                                    AboveTHundred+=1
            if t[0]=='����':
                # price_amount_beibei=[UnderThirty,ThirtyToSixty,SixtyToHundred,EightyToHundred,HundredToHfifty,HfiftyToTHundred,AboveTHundred]
                price_amount_beibei={
                    'area': t[0],
                    'UnderThirty': UnderThirty,
                    'ThirtyToSixty': ThirtyToSixty,
                    'SixtyToHundred': SixtyToHundred,
                    'HundredToHfifty': HundredToHfifty,
                    'HfiftyToTHundred': HfiftyToTHundred,
                    'AboveTHundred': AboveTHundred
                }
            else:
                if t[0]=='����':
                    price_amount_jiangbei = {
                        'area': t[0],
                        'UnderThirty': UnderThirty,
                        'ThirtyToSixty': ThirtyToSixty,
                        'SixtyToHundred': SixtyToHundred,
                        'HundredToHfifty': HundredToHfifty,
                        'HfiftyToTHundred': HfiftyToTHundred,
                        'AboveTHundred': AboveTHundred
                    }
                else:
                    if t[0] == '�山':
                        price_amount_yubei ={
                            'area': t[0],
                            'UnderThirty': UnderThirty,
                            'ThirtyToSixty': ThirtyToSixty,
                            'SixtyToHundred': SixtyToHundred,
                            'HundredToHfifty': HundredToHfifty,
                            'HfiftyToTHundred': HfiftyToTHundred,
                            'AboveTHundred': AboveTHundred
                        }
                    else:
                        if t[0]=='�ϰ�':
                            price_amount_nanan={
                                'area': t[0],
                                'UnderThirty': UnderThirty,
                                'ThirtyToSixty': ThirtyToSixty,
                                'SixtyToHundred': SixtyToHundred,
                                'HundredToHfifty': HundredToHfifty,
                                'HfiftyToTHundred': HfiftyToTHundred,
                                'AboveTHundred': AboveTHundred
                            }
                        else:
                            if t[0]=='����':
                                price_amount_yuzhong={
                                    'area': t[0],
                                    'UnderThirty': UnderThirty,
                                    'ThirtyToSixty': ThirtyToSixty,
                                    'SixtyToHundred': SixtyToHundred,
                                    'HundredToHfifty': HundredToHfifty,
                                    'HfiftyToTHundred': HfiftyToTHundred,
                                    'AboveTHundred': AboveTHundred
                                }
                            else:
                                if t[0]=='ɳƺ��':
                                    price_amount_shapingba={
                                        'area': t[0],
                                        'UnderThirty': UnderThirty,
                                        'ThirtyToSixty': ThirtyToSixty,
                                        'SixtyToHundred': SixtyToHundred,
                                        'HundredToHfifty': HundredToHfifty,
                                        'HfiftyToTHundred': HfiftyToTHundred,
                                        'AboveTHundred': AboveTHundred
                                    }
                                else:
                                    if t[0]=='������':
                                        price_amount_jiulongpo={
                                            'area': t[0],
                                            'UnderThirty': UnderThirty,
                                            'ThirtyToSixty': ThirtyToSixty,
                                            'SixtyToHundred': SixtyToHundred,
                                            'HundredToHfifty': HundredToHfifty,
                                            'HfiftyToTHundred': HfiftyToTHundred,
                                            'AboveTHundred': AboveTHundred
                                        }
                                    else:
                                        if t[0]=='����':
                                            price_amount_banan={
                                                'area': t[0],
                                                'UnderThirty': UnderThirty,
                                                'ThirtyToSixty': ThirtyToSixty,
                                                'SixtyToHundred': SixtyToHundred,
                                                'HundredToHfifty': HundredToHfifty,
                                                'HfiftyToTHundred': HfiftyToTHundred,
                                                'AboveTHundred': AboveTHundred
                                            }
                                        else:
                                            if t[0]=='��ɿ�':
                                                price_amount_dadukou={
                                                    'area': t[0],
                                                    'UnderThirty': UnderThirty,
                                                    'ThirtyToSixty': ThirtyToSixty,
                                                    'SixtyToHundred': SixtyToHundred,
                                                    'HundredToHfifty': HundredToHfifty,
                                                    'HfiftyToTHundred': HfiftyToTHundred,
                                                    'AboveTHundred': AboveTHundred
                                                }

    price_amount={
        'price_amount_jiangbei':price_amount_jiangbei,
        'price_amount_yubei':price_amount_yubei,
        'price_amount_nanan':price_amount_nanan,
        'price_amount_yuzhong':price_amount_yuzhong,
        'price_amount_shapingba':price_amount_shapingba,
        'price_amount_jiulongpo':price_amount_jiulongpo,
        'price_amount_banan':price_amount_banan,
        "price_amount_dadukou":price_amount_dadukou,
        'price_amount_beibei':price_amount_beibei
    }
    # print(price_amount['price_amount_jiangbei']['area'])
    price_amount = json.dumps(price_amount)
    # cursor.close()
    return price_amount

@data.route("/getAmount",methods=['GET'])
def get_Amount():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor = conn.cursor()
    # cursor = getdb()
    cursor.execute('select houses_area,houses_quantity from houses_amount')
    amount_info=cursor.fetchall()
    # print(len(amount_info))
    area={}
    amount={}
    count = 0
    for i in amount_info:
        area[count]=amount_info[count][0]
        amount[count]=amount_info[count][1]
        count=count+1

    data = {
        'area': area,
        'amount': amount
    }
    data=json.dumps(data)
    cursor.close()
    return data

@data.route("/getFloor", methods=['GET'])
def get_floor():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select floor_top, floor_mid, floor_low from floor_location')
    data = cursor.fetchall()
    view_data = {'view_data': data}
    return json.dumps(view_data, ensure_ascii=False)


@data.route("/getHouseSize", methods=['GET'])
def get_house_size():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select interval0, interval1, interval2, interval3 from house_size')
    data = cursor.fetchall()
    view_data = {'view_data': []}
    interval1 = []
    interval2 = []
    interval3 = []
    interval4 = []
    for i in data:
        interval1.append(i[0])
        interval2.append(i[1])
        interval3.append(i[2])
        interval4.append(i[3])
    view_data['view_data'].append(interval1)
    view_data['view_data'].append(interval2)
    view_data['view_data'].append(interval3)
    view_data['view_data'].append(interval4)
    return json.dumps(view_data, ensure_ascii=False)


@data.route('/getAvg', methods=['GET'])
def get_avg():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor1 = conn.cursor()
    cursor1.execute('select houses_avgUnitPrice,houses_area from avgprice')
    price = cursor1.fetchall()
    avg = {}
    area = {}
    for i in range(len(price)):
        avg[i] = price[i][0]
        area[i] = price[i][1]
    avgs = {
        'avg': avg,
        'area': area
    }
    avgs = json.dumps(avgs)
    return avgs


@data.route('/getType', methods=['GET'])
def get_type():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursor2 = conn.cursor()
    cursor2.execute('select houses_area,houses_HouseType,number from housestype')
    num = cursor2.fetchall()
    huxing = ["1��", "2��", "3��", "4��", "5�Ҽ�����"]
    price = [0, 0, 0, 0, 0]
    for i in range(len(num)):
        for x in range(len(huxing)):
            if num[i][1] == huxing[x]:
                price[x] += num[i][2]
    data = {
        'num': num,
        'price': price,
        'huxing': huxing
    }
    data = json.dumps(data)
    return data


@data.route('/getGZ', methods=['GET'])
def get_gz():
    conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                           charset='utf8')
    cursot_ky1 = conn.cursor()
    cursot_ky1.execute("select * from attention;")

    row1 = cursot_ky1.fetchall()
    row2 = np.array(row1)
    row3 = row2.tolist()    #ת��Ϊ�б�
    C_area=[]
    Sum_people=[]
    people=[]

    for i in row3:
        C_area.append(i[0])
        Sum_people.append(i[1])
        people.append(i[2])
        b = [round(float(i)) for i in people]
        Avg_people = [i * 10000 for i in b]

    gz = C_area+Sum_people+Avg_people
    gz=json.dumps(gz)
    return gz

@data.route('/get_relation_data', methods=['GET'])
def get_relation():
#����������ַ�װ������뵥�ۼ��ϵ
    conn = pymysql.connect(host='10.20.220.203', user='root', passwd='sx2626', port=3306, db='python', charset='utf8')
    cursot_ky2 = conn.cursor()
    cursot_ky2.execute("select area,avg from zx;")
    data_2 = cursot_ky2.fetchall()
    # print(data_2)

    data_3 = np.array(data_2)
    data_4= data_3.tolist()    #ת��Ϊ�б�
    # print(data_4)
    data=[]
    area=[]

    for i in data_4:
        data.append(i[1])
        area.append(i[0])

    # print(area)
    area_data=area[0::4]
    mp_data=data[1::4]
    jianz_data=data[2::4]
    jinz_data=data[3::4]
    relation_data=area_data+mp_data+jianz_data+jinz_data
    # print(relation_data)
    relation=json.dumps(relation_data)
    return relation