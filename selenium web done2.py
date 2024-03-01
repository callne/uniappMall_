
from selenium import webdriver
from lxml import etree
import bs4
import urllib.request as ur
import sqlalchemy as sql
import sqlalchemy.orm as sqlorm
from sqlalchemy.ext.declarative import declarative_base
import sys
import imp
imp.reload(sys)

wb = webdriver.Chrome(r'C:\Users\86134\Desktop\chromedriver_win32\chromedriver.exe')# 游览器驱动driver
b=[]
c=[]
price=[]
shop=[]
content=[]
img=[]
for i in range(1,201,2):
    b.append(i)
for i in range(1,5001,50):
    c.append(i)

urls = ('https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page={}&s={}&click=0'.format(b[i],c[i]) for i in range(99))

for url in urls:
    wb.get(url)
    data = wb.page_source
    soup = bs4.BeautifulSoup(data,'lxml')
    shop_datas = soup.select("a[class='curr-shop hd-shopname']")
    shop_datas2 = soup.select('a[class="curr-shop hd-shopname"]')
    shop_datas3 = shop_datas+shop_datas2
    price_datas = soup.select("strong[data-done='1'] i")
    price_datas2 = soup.select('strong[data-done="1"] i')
    price_datas3 = price_datas+price_datas2
    content_datas = soup.select("div[class='p-name p-name-type-2'] em")
    content_datas2 = soup.select('div[class="p-name p-name-type-2"] em')
    content_datas3 = content_datas+content_datas2
    for i in price_datas3:
        price.append(i.get_text())
    for i in shop_datas3:
        shop.append(i.get_text())
    for i in content_datas3:
        content.append(i.get_text())

    img_datas = soup.find_all('img',width="220",height="220")
    img_datas2 = soup.find_all('img',width='220',height='220')
    img_datas3 = img_datas+img_datas2
    for i in range(60):
        img.append(img_datas3[i])
    # for i in price_datas3:
    #     jishu+=1
    #     print(i.get_text())
    # print(jishu)



# for r,n,t in zip(shop_datas,price_datas,content_datas):
#         r = r.get_text().replace('\n','').replace('\t','').replace('\r','')
#         n = n.get_text()
#         t = t.get_text().replace('\n','').replace('\t','').replace('\r','')
#         data = {
#             '商店名字': r,
#             '价格': n,
#             '手机介绍': t
#         }
#         print(data)






#图片保存
jishu=0
for i in img:
    jishu+=1
    src = i.get('src')
    html = ur.urlopen('https:'+str(src))
    html_ = html.read()
    with open('picture{}.jpg'.format(jishu),'wb') as f:
        f.write(html_)



#数据库操作
engine = sql.create_engine('mysql+mysqlconnector://root:')
metadata = sql.MetaData(engine)
metadata.create_all(engine)
DBSession = sqlorm.sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()
phone1 = sql.Table('phone_data',metadata,
                    sql.Column('id',sql.Integer,primary_key=True),
                    sql.Column('price',sql.String(200)),
                    sql.Column('content',sql.String(500)),
)
phone2 = sql.Table('phone_shop',metadata,
                    sql.Column('id',sql.Integer,primary_key=True),
                    sql.Column('shop_name',sql.String(100)),
)
metadata.create_all()
class PHONE_data(Base):
    __tablename__ = 'Phone_data'
    id = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column(sql.String(200))
    content = sql.Column(sql.String(500))
class PHONE_shop(Base):
    __tablename__ = 'phone_shop'
    id = sql.Column(sql.Integer, primary_key=True)
    shop_name = sql.Column(sql.String(200))
num=0
for i in range(6):
    for i in range(990):
        phone1 = PHONE_data(price=price[num],content=content[num])
        num+=1
        session.add(phone1)
        session.commit()
        session.close()


numq=0
for i in range(6):
    for i in range(980):
        phone2 = PHONE_shop(shop_name=shop[numq])
        numq+=1
        session.add(phone2)
        session.commit()
        session.close()




