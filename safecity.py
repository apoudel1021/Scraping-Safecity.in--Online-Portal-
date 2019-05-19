# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 23:38:57 2018

@author: deadp
"""

import time 
from bs4 import BeautifulSoup 
import urllib
html = urllib.urlopen('http://www.maps.safecity.in/reports').read()
#print html.text
soup = BeautifulSoup(html, 'html.parser')
start_time = time.time()

Text =[]
Types =[] 


tweet=soup.find('div',class_='rapidxwpr floatholder')
process = soup.find('div', id ='middle')
process1 =  soup.find('div', class_='background layoutleft')
process2 =  soup.find('div', id ='content').find('div',class_='content-bg').find('div',class_='big-block').find('div',id='reports-box')
#print process2

getpages= process2.find('div',class_='rb_nav-controls r-5').find('ul',class_='pager')
process3=getpages.findAll('li')
print len(process3)
count= int(getpages.findAll('li')[8].span.a.text)
print count

for i in range(count):
    print "We ARE AT PAGE NUMBER" + str(i+1)
    url = 'http://www.maps.safecity.in/reports/fetch_reports?page='+str(i+1)
#    print url
    html = urllib.urlopen(url).read()
#    print html
    soup = BeautifulSoup(html, 'html.parser')
    tweetsonpage = soup.find('div',class_='rb_list-and-map-box').find('div', id = 'rb_list-view')
    alltrs = tweetsonpage.findAll('div',class_='rb_report unverified')
#    print tweetsonpage
#.find('div',class_='rb_list-view')
#    
#    print alltrs[0].text
    for a in alltrs:
#        print a
        try:
            link = a.find('div',class_='r_media').p.a.get('href')
            inpage = urllib.urlopen(link).read()
            soup1 = BeautifulSoup(inpage, 'html.parser')
            desc=soup1.find('div',class_='rapidxwpr floatholder')
            adesc = soup1.find('div', id ='middle')
            bdesc =  soup1.find('div', class_='background layoutleft').find('div',class_='report_detail').find('div',class_='left-col')
            category = bdesc.find('div',class_='report-category-list').p.a.text
        #    #.findAll('div',class_='reb_report unverified')
            description= bdesc.find('div',class_='report-description-text')
            text=description.h5.find_next_siblings(text=True)[0].strip()
            Text.append(text)
            category = category.lstrip().replace('\n','').strip()
            print category
            Types.append(category)
        except:
            pass

import pandas as pd 
test_df =pd.DataFrame({'Text':Text, 'Types':Types}) 
print test_df

test_df.to_csv('safecity.csv',sep=",", encoding='utf-8', index=False)    
print("--- %s seconds ---" % (time.time() - start_time))

print 'end'