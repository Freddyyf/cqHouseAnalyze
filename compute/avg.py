#coding=gbk
import pymysql

# ��ȡ����
conn=pymysql.connect(host="10.20.220.203",user="root",password="sx2626",database="python",charset='utf8')
cursor=conn.cursor()
cursor.execute('select house_area,house_UnitPrice from data')
avg=cursor.fetchall()
area=["����","��ɿ�","�ϰ�","����","����","�山","ɳƺ��","����","������"]
price=[0,0,0,0,0,0,0,0,0]
num_price=[0,0,0,0,0,0,0,0,0]
avgs=[0,0,0,0,0,0,0,0,0]
print(len(avg))

def paimi(line):
    for lines in range(len(line)):
        for i in range(len(area)):
            if line[lines][0] == area[i]:
                price[i]+=int((line[lines][1].split('Ԫ'))[0])
                num_price[i]+=1
paimi(avg)
print(price)
print(num_price)
def avg(price,num_price):
    for num in range(len(area)):
        num_avgs=price[num]/num_price[num]
        avgs[num]=str(round(num_avgs,2))
        # avgs[num]=avgs[num]+"Ԫ/ƽ��"
avg(price,num_price)
print(avgs)

#������д�����ݿ�
query = "insert into avgprice (houses_area,houses_avgUnitPrice) values (%s,%s)"
for r in range(len(area)):
    houses_area=area[r]
    houses_avgUnitPrice=avgs[r]
    values=(houses_area,houses_avgUnitPrice)
    cursor.execute(query,values)
conn.commit()