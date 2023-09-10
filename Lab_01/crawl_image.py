# Nhóm thực hiện
# Trần Văn Lực – 20521587​
# Ngô Ngọc Sương - 20521852​
# Nguyễn Văn Hợp - 20521358​

# Khai báo các thư viện cần thiết
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request 


# Khai báo hàm khởi tạo một webdriver (cụ thể là chrome) trên máy
options = Options()
# Thêm option để tránh hiện thông báo lỗi tin nhắn ghi nhật ký chorme
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

# Truy cập vào google hình ảnh 
browser.get('https://images.google.com/')

# Tìm kiếm ô nhập thông tin cần tìm kiếm qua xpath
# search_input = browser.find_element(by=By.XPATH, value='//*[@id="sbtc"]/div/div[2]/input')
search_input = browser.find_element(by=By.XPATH, value='//*[@class="RNNXgb"]/div/div[2]/input')

# Nhập thông tin cần tìm kiếm
info = 'cow'
search_input.send_keys(info)

# Nhấn enter để thực hiện tìm kiếm
search_input.send_keys(Keys.ENTER) 

# Tạo một list chứa các đường dẫn ảnh và đường dẫn chứa ảnh
src_images = []
path = '.\\image\\'

for i in range(1, 15):
    try:
        # tìm thẻ chứa ảnh và lấy đường dẫn ảnh
        img = browser.find_element(by=By.XPATH, value = '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img')
        src_images.append(img.get_attribute("src"))
        sleep(0.5)
    except:
        continue
    
number = 0
# for src in src_images:
#     # Sao chép ảnh được biểu thị bằng đường dẫn vào thư mục với đường dẫn được khai báo trước đó
#     urllib.request.urlretrieve(src, path + str(number) + ".jpg") #https://docs.python.org/3/library/urllib.request.html
#     number += 1 
sleep(5)
# Đóng trình duyệt
browser.close()