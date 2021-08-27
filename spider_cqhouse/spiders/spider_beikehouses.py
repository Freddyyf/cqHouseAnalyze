#coding=gbk
import scrapy
import re

from spider_cqhouse.items import houses
zpage ={}
ls=[]
areas = ['yuzhong', 'jiangbei', 'nanan', 'jiulongpo', 'shapingba', 'dadukou', 'beibei', 'yubei', 'banan']
for line in areas:
    url = 'https://cq.ke.com/ershoufang/' + line + '/'
    ls.append(url)

class CquptbeikehouseSpider(scrapy.Spider):
    name = 'beikehouses'
    allowed_domains = ['cq.lianjia.com']
    current_page=1
    start_urls =ls

    def parse(self, response):
        info_clear=response.xpath("//div[@class='info clear']")
        for sell in info_clear:
            url = response.request.url
            area = url.split("/")
            #����
            house=houses()
            houses_area=response.xpath("//*[@id='beike']/div[1]/div[3]/div[1]/dl[2]/dd/div[1]/div[1]/a[@class='selected CLICKDATA']/text()").extract()[0]
            # house['houses_area']=area[4]
            house['houses_area']=houses_area
            #�ص�
            houses_LocationName="0"
            house['houses_LocationName']=houses_LocationName
            # С����
            houses_CommunityName=sell.xpath("./div[@class='address']/div[@class='flood']/div/a/text()").extract()[0]
            house['houses_CommunityName']=houses_CommunityName
            # ����
            houses_HouseType=sell.xpath("./div[@class='address']/div[@class='houseInfo']/text()").extract()[1].replace(" ","")
            houses_HouseTypes=houses_HouseType.split("/n")
            # print(houses_HouseTypes)
            houses_HouseType=houses_HouseTypes[-4].split("|")
            houses_HouseSize=houses_HouseTypes[-4].split("|")
            houses_HouseType=houses_HouseType[0]
            house['houses_HouseType']=houses_HouseType
            #װ�����
            houses_Decoration="0"
            house['houses_Decoration']=houses_Decoration
            #���ݴ�С
            houses_HouseSize=houses_HouseSize[1]
            house['houses_HouseSize']=houses_HouseSize
            #����
            houses_orientation=houses_HouseTypes[-3].split("|")#�Ӻ��濪ʼ��ȡ
            houses_orientation=houses_orientation[1]
            house['houses_orientation']=houses_orientation
            #¥��
            houses_floor=houses_HouseTypes[1] + houses_HouseTypes[2]
            house['houses_floor'] = houses_floor
            #����ʱ��
            # print(houses_HouseTypes)
            houses_BuildingTime=houses_HouseTypes[3].split("|")
            #������ʽ
            check="��"
            res=re.search(check.encode('gbk'),houses_BuildingTime[1].encode('gbk'))
            # print(res)
            if res is not None:
                houses_BuildingTime=houses_BuildingTime[1]
            else:
                houses_BuildingTime="0"
            house['houses_BuildingTime']=houses_BuildingTime
            #�ṹ����
            houses_structureType="0"
            house['houses_structureType']=houses_structureType
            #��ע����
            houses_NumPeople=sell.xpath("./div[@class='address']/div[@class='followInfo']/text()").extract()[1].replace(" ","")
            houses_NumPeoples=houses_NumPeople.split("/n")
            houses_NumPeople=houses_NumPeoples[1]
            house['houses_NumPeople']=houses_NumPeople
            #����ʱ��
            houses_ReleaseTime=houses_NumPeoples[2].split("/")
            # print(houses_ReleaseTime[1])
            houses_ReleaseTime=houses_ReleaseTime[1]
            house['houses_ReleaseTime']=houses_ReleaseTime
            #�ܼ�
            houses_TotalPrice=sell.xpath("./div[@class='address']/div[@class='priceInfo']/div[@class='totalPrice']/span/text()").extract()[0].replace(" ","")
            houses_TotalPrice=houses_TotalPrice.split("/n")
            houses_TotalPrice=houses_TotalPrice[1]+"��"
            house['houses_TotalPrice']=houses_TotalPrice
            #����
            houses_UnitPrice=sell.xpath("./div[@class='address']/div[@class='priceInfo']/div[@class='unitPrice']/@data-price").extract()[0]
            houses_UnitPrice=houses_UnitPrice+"Ԫ/ƽ��"
            house['houses_UnitPrice']=houses_UnitPrice
            # ����
            houses_title=sell.xpath("./div[@class='title']/a/text()").extract()[0].replace(" ","��")
            house['houses_title'] = houses_title
            with open("D:/workspace/20210824/cqHouseAnalyze/spider_cqhouse/spiders/house.csv", "a", encoding='utf_8_sig')as wt:
                wt.write(houses_area+"  "+houses_LocationName+"  "+houses_CommunityName+"  "+houses_HouseType+"  "+houses_HouseSize+"  "+houses_Decoration+"  "+houses_orientation+"  "+houses_floor+"  "+houses_BuildingTime+"  "
                         +houses_structureType+"  "+houses_NumPeople+"  "+houses_ReleaseTime+"  "+houses_TotalPrice
                         +"  "+houses_UnitPrice+"  "+houses_title+"  "+"/n")
            yield house
        url = response.request.url
        yield scrapy.Request(url, callback=self.url_parse, dont_filter=True)
    def url_parse(self,response):
        urls = response.request.url
        print(urls)
        job_page = response.xpath("//div[@class='page-box fr']")
        page = job_page.xpath("div[@class='page-box house-lst-page-box']/@page-data").extract()[0]
        num = page.split(",")
        zpage[0] = num[0].split(":")
        new_zpage = int(zpage[0][1])  # ��ҳ��
        zpage[1] = num[1].split(":")
        fpage = zpage[1][1]  # ��ҳ��
        fpage=fpage.split("}")
        new_fpage = int(fpage[0])
        next_fpage=new_fpage+1
        if urls.find("pg") != -1:#����pg
            if new_fpage <= new_zpage:
                next_url = urls.replace("pg%d"%(next_fpage-1),"pg%d"%next_fpage)
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
        else:#������pg
            next_url = urls + 'pg' + str(next_fpage) + '/'
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
