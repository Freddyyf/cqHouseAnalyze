#coding=gbk
import pymysql
from MySQLdb.constants.FIELD_TYPE import VARCHAR

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, Row, DoubleType
# ��ȡ����
conn=pymysql.connect(host="10.20.220.203",user="root",password="sx2626",database="python",charset='utf8')
cursor=conn.cursor()
cursor.execute('select house_area,house_HouseType from data')
type=cursor.fetchall()
huxing=["1��","2��","3��","4��","5�Ҽ�����"]
types= {}
area=["����","��ɿ�","�ϰ�","����","����","�山","ɳƺ��","����","������"]
areatype={}
for nums in range(len(type)):
    types[nums]=type[nums][1][:2]
def typearea(area):
    num = [0, 0, 0, 0, 0]
    for nums in range(len(type)):
        if type[nums][0]==area:
            for i in range(len(huxing)):
                if types[nums] == huxing[i]:
                    num[i] += 1
            if types[nums] != "1��" and types[nums] != "2��" and types[nums] != "3��" and types[nums] != "4��":
                num[4] += 1
    # print(area,num)
    return num
for i in range(len(area)):
    num=typearea(area[i])
    for y in range(len(num)):
        areatype[len(areatype)]=(area[i],huxing[y],num[y])
print(areatype[0])
#������д�����ݿ�
query = "insert into housestype (houses_area,houses_HouseType,number) values (%s,%s,%s)"
for r in range(len(areatype)):
    houses_area=areatype[r][0]
    houses_HouseType=areatype[r][1]
    number=areatype[r][2]
    values=(houses_area,houses_HouseType,number)
    cursor.execute(query,values)
conn.commit()