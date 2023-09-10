# Nhóm thực hiện
# Trần Văn Lực – 20521587​
# Ngô Ngọc Sương - 20521852​
# Nguyễn Văn Hợp - 20521358​

# khai báo các thư viện cần thiết
from selenium import webdriver
from time  import sleep
import pandas as pd
from selenium.webdriver.common.by import By


# Khởi tạo một webdriver (cụ thể là chrome) trên máy
browser=webdriver.Chrome()

# Mở trang web của tác giá cần lấy dữ liệu trên schoolar
browser.get("https://scholar.google.com/citations?hl=vi&user=p3vHDZYAAAAJ")
sleep(5) # đợi 5s để trang web được load

# Tìm nút hiện hiện thêm bài báo và click vào nó - trả về đổi tượng là thẻ button
showmore_paper = browser.find_element(By.ID,'gsc_bpf_more')
showmore_paper.click()
sleep(5) # đợi 5s để trang web được load thêm

title_paper = []
author_paper = []
year_paper = []
# lấy danh sách tất các các thẻ chứa thông tin bài báo trong trang web đã được load
paper_list = browser.find_elements(By.CLASS_NAME,'gsc_a_tr')

# với mối thẻ ứng với mỗi bài báo thì lấy thông tin tiêu đề, tác giả, năm xuất bản 
# tương ứng các class name của các thẻ chứa thôn tin cần tìm
for paper in paper_list:
        title = paper.find_element(By.CLASS_NAME,'gsc_a_at') 
        authors = paper.find_element(By.CLASS_NAME,'gs_gray')
        year=paper.find_element(By.CLASS_NAME,'gsc_a_h')
        # thêm các thông tin đã lấy vào danh sách tương ứng
        title_paper.append(title.text)
        author_paper.append(authors.text)
        year_paper.append(year.text)
# tạo dataframe từ các danh sách đã lấy
data={'Title': title_paper,'Authors':author_paper,'Year':year_paper}
# lưu dữ liệu vào file csv
pd.DataFrame(data).to_csv('./paper.csv')
# đóng trình duyệt
browser.close()

