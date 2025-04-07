import re
from utils import url_manager
import requests
from bs4 import BeautifulSoup

root_url  = 'http://www.crazyant.net'
urls = url_manager.UrlManager()
urls.add_new_url(root_url)

fout = open('craw_all_paper.txt','w')
while urls.has_new_url():
    cur_url = urls.get_url()
    r = requests.get(cur_url,timeout=3)
    if r.status_code != 200:
        print('error',cur_url)
        continue
    soup = BeautifulSoup(r.text,'html.parser')
    title = soup.title.string

    fout.write('%s \t %s \n'%(cur_url,title))
    fout.flush()
    print("success:%s %s"%(cur_url,title))

    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href is None:
            continue
        pattern = r'^http://www.crazyant.net/\d+.html$'
        if re.match(pattern,href):
            urls.add_new_url(href)

fout.close()