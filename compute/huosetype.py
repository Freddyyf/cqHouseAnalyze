#coding=gbk
import pymysql

# ��ȡ����
conn=pymysql.connect(host="10.20.220.203",user="root",password="sx2626",database="python",charset='utf8')
cursor=conn.cursor()
cursor.execute('select house_HouseType from data')
type=cursor.fetchall()
huxing=["1��","2��","3��","4��","5�Ҽ�����"]
types= {}
num=[0,0,0,0,0]
for nums in range(len(type)):
    types[nums]=type[nums][0][:2]
for nums in range(len(type)):
    for i in range(len(huxing)):
        if types[nums]==huxing[i]:
            num[i]+=1
    if types[nums]!="1��" and types[nums]!="2��"and types[nums]!="3��"and types[nums]!="4��":
            num[4]+=1
print(len(types))
print(num)
print(len(type))
#������д�����ݿ�
query = "insert into housestype (houses_HouseType,number) values (%s,%s)"
for r in range(len(num)):
    houses_HouseType=huxing[r]
    number=num[r]
    values=(houses_HouseType,number)
    cursor.execute(query,values)
conn.commit()