# #coding=gbk
import json
import pymysql
from config import db

"""
����ͼר�����ڴ���ajax����
"""
from flask import Blueprint
from dbmodel.floor_location import FloorLocation
from dbmodel.house_size import HouseSize

data = Blueprint('data', __name__)


@data.route("/getFloor", methods=['GET'])
def get_floor():
    conn = pymysql.connect(host="localhost", user="root", password="root", database="cqhouseanalyze",
                                   charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select floor_top, floor_mid, floor_low from floor_location')
    data = cursor.fetchall()
    view_data = {'view_data': data}
    return json.dumps(view_data, ensure_ascii=False)


@data.route("/getHouseSize", methods=['GET'])
def get_house_size():
    conn = pymysql.connect(host="localhost", user="root", password="root", database="cqhouseanalyze",
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
    return json.dumps(data, ensure_ascii=False)


# @data.route('/getAvg', methods=['GET'])
# def get_avg():
#     conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
#                                    charset='utf8')
#     cursor = conn.cursor()
#     cursor.execute('select houses_avgUnitPrice from avgprice')
#     price = cursor.fetchall()
#     for i in range(len(price)):
#         price[i] = price[i][0]
#     cursor.execute('select houses_area from avgprice')
#     area = cursor.fetchall()
#     for i in range(len(area)):
#         area[i] = area[i][0]
#     avg = {
#         'price': price,
#         'area': area
#     }
#     avg = json.dumps(avg)
#     return avg
#
#
# @data.route('/getType', methods=['GET'])
# def get_type():
#     conn = pymysql.connect(host="10.20.220.203", user="root", password="sx2626", database="python",
#                                    charset='utf8')
#     cursor = conn.cursor()
#     cursor.execute('select number from housestype')
#     num = cursor.fetchall()
#     # price=price(lambda x:x[0])
#     for i in range(len(num)):
#         num[i] = num[i][0]
#     cursor.execute('select houses_HouseType from housestype')
#     type = cursor.fetchall()
#     for i in range(len(type)):
#         type[i] = type[i][0]
#     data = {
#         'num': num,
#         'type': type
#     }
#     data = json.dumps(data)
#     return data
