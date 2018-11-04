#coding:utf8
import chardet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json 
import collections

# pip 를 통하여 bs4 , selenium 설치. chrome web driver 설치.


def tree():
	return collections.defaultdict(tree)

chromedriver = 'C:/Users/sub/Downloads/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

driver.get("https://www.pooq.co.kr/")

text_contents = [el.text for el in driver.find_elements_by_xpath("/html/body/div/div/div/div/div/ul/li/button")]

test = driver.find_elements_by_xpath("/html/body/div/div/div/div/div/ul/li/button[1]")
test[1].send_keys(Keys.ENTER)

driver.implicitly_wait(1) # seconds

test1 = driver.find_elements_by_xpath(".//*[contains(text(), '스포츠')]")

driver.execute_script("arguments[0].click();", test1[0])


search = driver.find_elements_by_xpath('//*[@id="searchPop"]/div/div/div/div/ul/li/button')
driver.execute_script("arguments[0].click();", search[1])

entire_list = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/h3/a')
driver.execute_script("arguments[0].click();", entire_list[0])

# 프로그램 목록 페이지. 


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 현재 페이지 주소&page=숫자
#url = driver.current_url

# 프로그램 페이지 리스트 갯수 구하기. 
page_lists = soup.select('body > div > div.top-padding > div.wrap > div > div > div.paging-type01')
for i in page_lists:
	print(i.text)
tot_page = len(page_lists)
print(tot_page)


# 페이지 옮기기 & 이름, 제작사 crawling
dict_program = tree()
name_list =[]
studio_list=[]
program_list = []
with open ('./result.json', 'w', encoding='utf-8') as file:
	for page_num in range(0, tot_page+1):
		lists = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div/a')
		print(page_num)
		driver.execute_script("arguments[0].click();", lists[page_num])
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		driver.implicitly_wait(5)
		names = soup.find_all("strong", class_="con-tit")
		studios = soup.select('body > div > div.top-padding > div.wrap > div > div > div.sh-component01-wrap > div > div > a > span.con-text-wrap > span')
		
		for name in names:
			name_list.append(name.text)
		for studio in studios:
			studio_list.append(studio.text)
		for i in range(len(names)):
			dict_program['name'] = name_list[i]	
			dict_program['studio'] = studio_list[i]
			program_list.append(dict_program.copy())	
	json.dump(program_list, file, ensure_ascii=False, indent=3)


#ele = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/ul[2]/li[2]/button').click()
#driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
#ele = driver.find_element_by_xpath('//*[@id="taglist"]/div/ul/li/label').click()

# tag search selector , xpath
#body > div > div:nth-child(2) > div > div:nth-child(2) > div > ul.gnb-right > li:nth-child(2) > button
# /html/body/div/div[2]/div/div[2]/div/ul[2]/li[2]/button

# label sport xpath
# //*[@id="taglist"]/div[2]/ul[1]/li[3]/label


