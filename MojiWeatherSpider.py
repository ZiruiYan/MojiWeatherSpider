import requests
from bs4 import BeautifulSoup

import argparse

parser=argparse.ArgumentParser(description='MojiWeatherSpider')
parser.add_argument('-p','--province', type=str,default='beijing',help='name of province')
parser.add_argument('-d','--district',type=str,default='dongcheng',help='name of district')
args=parser.parse_args()

def get_url(province,city):
	urlWeather='https://tianqi.moji.com/weather/china/%s/%s-district'%(province,city)
	urlDress='https://tianqi.moji.com/dress/china/%s/%s-district'%(province,city)
	urlUltraviolet='https://tianqi.moji.com/uray/china/%s/%s-district'%(province,city)

	return urlWeather,urlDress,urlUltraviolet


def get_(urlWeather,urlDress,urlUltraviolet):
	r=requests.get(urlWeather)
	soup = BeautifulSoup(r.text,'html.parser')
	data_now=soup.find_all('div',attrs={'class':"wrap clearfix wea_info"})[0]
	list_now=data_now.find_all('em')
	now_pm25=list_now[0].get_text()
	now_tmp =list_now[1].get_text()
	now_wind=list_now[2].get_text()
	now_feel=list_now[3].get_text()
	now_weat=data_now.find_all('b')[0].get_text()
	now_amp=data_now.find_all('span')[2].get_text()
	print('*'*5+'现在的天气情况'+'*'*5)
	print('现在是%s'%now_weat)
	print('气温：%s'%now_tmp)
	print('风速：%s'%now_wind)
	print('感觉：%s'%now_feel)
	print('湿度：%s'%now_amp)
	print('空气质量：%s'%now_pm25)

	data_today=soup.find_all('ul',attrs={'class':'days clearfix'})[0]
	TodayWeather=data_today.find_all('li')[1]
	TodayWeather=TodayWeather.find_all('img')[0]
	TodayWeather=TodayWeather['alt']
	TodayTmp=data_today.find_all('li')[2].get_text()
	TodayWind=data_today.find_all('li')[3]
	TodayWind=TodayWind.find_all('em')[0].get_text()+TodayWind.find_all('b')[0].get_text()
	TodayPm25=data_today.find_all('li')[4].find_all('strong')[0].get_text()
	TodayPm25=TodayPm25.replace(' ','')
	TodayPm25=TodayPm25.replace('\r','')
	TodayPm25=TodayPm25.replace('\n','')
	print('*'*5+'今天的天气情况'+'*'*5)
	print('天气%s'%TodayWeather)
	print('气温：%s'%TodayTmp)
	print('风速：%s'%TodayWind)
	print('空气质量：%s'%TodayPm25)

	dataLiveIndex=soup.find_all('div',attrs={'id':'live_index'})

	rDress=requests.get(urlDress)
	soupDress=BeautifulSoup(rDress.text,'html.parser')
	wear=soupDress.find_all('div',attrs={'class':'aqi_info'})[0]
	clothes=wear.find_all('span')[0].get_text()+' :'+wear.find_all('em')[0].get_text()
	clothesOther=wear.find_all('dt')[0].get_text()+wear.find_all('dd')[0].get_text()

	dataUltraviolet=requests.get(urlUltraviolet)
	soupUltraviolet=BeautifulSoup(dataUltraviolet.text,'html.parser')
	Ultraviolet=soupUltraviolet.find_all('div',attrs={'class':'aqi_info_detail'})[0]
	UltravioletInfo=Ultraviolet.find_all('span')[0].get_text()+' :'+Ultraviolet.find_all('em')[0].get_text()
	print(clothes)
	print(clothesOther)
	print(UltravioletInfo)

def main():
	urlWeather,urlDress,urlUltraviolet=get_url(args.province,args.district)
	get_(urlWeather,urlDress,urlUltraviolet)

if __name__ == '__main__':
	main()