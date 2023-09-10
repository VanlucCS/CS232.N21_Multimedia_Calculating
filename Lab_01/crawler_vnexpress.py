# Nhóm thực hiện
# Trần Văn Lực – 20521587​
# Ngô Ngọc Sương - 20521852​
# Nguyễn Văn Hợp - 20521358​

# thêm các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import argparse
from selenium.webdriver.chrome.options import Options

# tạo đối tượng parser chứa số lượng bài viết và số lượng bình luận cần lấy
parser = argparse.ArgumentParser()
parser.add_argument('--num_article', type=int, help='number article to get crawling', default=2)
parser.add_argument('--num_commnet', type=int, help='number comment ber post', default=2)
parser.add_argument('--save_file', type=str, default='./comments.csv')
args = vars(parser.parse_args())

# mở trình duyệt

# Khai báo hàm khởi tạo một webdriver (cụ thể là chrome) trên máy
options = Options()
# Thêm option để tránh hiện thông báo lỗi tin nhắn ghi nhật ký chorme
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# browser = webdriver.Chrome(options=options)
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
# nhập url của trang báo điện tử
url = 'https://vnexpress.net/'
driver.get(url)

# lấy source của tất cả các bài viết
page_source = BeautifulSoup(driver.page_source)
# tìm tất cả source là thẻ h3 và có class là "title-news" 
# thẻ này chứa thông tin tiêu đề bài viết và link bài viết
element_title_articles = page_source.find_all('h3', class_ = "title-news")

# tạo các danh sách chứa các thông tin cần lấy
all_title_link = []
all_title_name = []
all_comments = []

# lấy thông tin tiêu đề và link của các bài viết
for element in element_title_articles: 
    all_title_name.append(element.find('a').get('title'))
    all_title_link.append(element.find('a').get('href'))
print(all_title_name)
# với mỗi link bài viết thì lấy thông tin bình luận 
# (lấy theo số lượng tối thiểu đã cho theo argument --num_commnet)
for link in all_title_link[:min(len(all_title_link),  args['num_article'])]:
    # mở trang bài viết để lấy command
    comment_inpage = []

    driver.get(link)
    # xử dụng thư viện beautifulsoup để lấy dữ liệu từ HTML của trang web
    # time.sleep(2) # đợi 2s để trang web được load
    page_source = BeautifulSoup(driver.page_source,features="lxml")
    time.sleep(2) # đợi 2s để trang web được load

    # tạo set chứa các thẻ chứa thông tin bình luận
    element_comments = set()
    num_of_comment = len(element_comments)
    # lấy số command theo argument --num_commnet đã cho hoặc tới khi hết command
    # while num_of_comment < args['num_commnet']:
    #     print(num_of_comment)
    #     print(args['num_commnet'])
    try:
        # tìm tất cả các thẻ div và có class là "content-comment"
        comments = page_source.find_all('div', class_='content-comment')
        element_comments.update(comments) # thêm các thẻ vào set
        num_of_comment = len(element_comments)
    except:
        break

        # try:
        #     # tìm thẻ button và có id là "show_more_coment"
        #     # btn = driver.find_element(By.ID, 'show_more_coment')
        # except:
        #     raise
            # click vào button để load thêm comment
        # driver.execute_script("arguments[0].click();",btn)
        # click vào button để load thêm comment
        # driver.execute_script("arguments[0].click();",btn)  
        

    # Lấy thông tin bình luận cho mỗi phần tử trong danh sách comment
    for cmt in list(element_comments):
        try:
            cmt_text = cmt.find('p', 'full_content')
            # all_comments.append([cmt_text.text])
            comment_inpage.append(cmt_text.text)
        except:
            cmt_text = cmt.find('p', 'content_more')
            comment_inpage.append(cmt_text.text)
            # all_comments.append([cmt_text.text])

    all_comments.append(comment_inpage)
driver.close()

# Ghi dữ liệu vào file csv ver 1
# header = ['Comment']
# with open(args['save_file'], 'w',encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     # Thêm header vào file csv
#     writer.writerow(header)
#     # Thêm dữ liệu vào file csv
#     writer.writerows(all_comments)

# Viết dữ liệu vào file csv ver 2

data={'Comment': all_comments}
# print(data)
# print(len(all_title_name))
# print(len(all_comments))
pd.DataFrame(data).to_csv('./comment2.csv')
# vuesetads 

