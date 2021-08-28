# #coding=gbk
import json

import numpy as np
import pymysql
from config import db

"""
本视图专门用于处理ajax数据
"""
from flask import Blueprint


data = Blueprint('data', __name__)
conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
                       charset='utf8')
cursor1 = conn.cursor()
cursor1.execute('select houses_avgUnitPrice,houses_area from avgprice')
cursor2 = conn.cursor()
cursor2.execute('select houses_HouseType,number from housestype')

cursot_ky1 = conn.cursor()
cursot_ky1.execute("select * from gz;")
cursot_ky2 = conn.cursor()
cursot_ky2.execute("select area,avg from zx;")

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
    num = cursor2.fetchall()
    numb = {}
    type = {}
    for i in range(len(num)):
        type[i] = num[i][0]
        numb[i] = num[i][1]
    data = {
        'numb': numb,
        'type': type
    }
    data = json.dumps(data)
    return data


@data.route('/getGZ', methods=['GET'])
def get_gz():

    row1 = cursot_ky1.fetchall()
    row2 = np.array(row1)
    row3 = row2.tolist()    #转换为列表
    C_area=[]
    SumPeople=[]

    for i in row3:
        C_area.append(i[0])
        SumPeople.append(i[1])

    gz = C_area+SumPeople

    data1 = SumPeople

    data2 = ['关注人数']

    data3 = data2+data1

    data4 = ['product']

    data5 = C_area

    data6 = data4+data5
    print(data6,'\n',data3)
    gz=json.dumps(gz)

    return gz

@data.route('/get_relation_data', methods=['GET'])

def get_relation():
#重庆各区二手房装修情况与单价间关系
    conn = pymysql.connect(host='10.20.220.203', user='root', passwd='sx2626', port=3306, db='python', charset='utf8')

    data_2 = cursot_ky2.fetchall()
    # print(data_2)

    data_3 = np.array(data_2)
    data_4= data_3.tolist()    #转换为列表
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