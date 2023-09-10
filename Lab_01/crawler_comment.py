# Nhóm thực hiện
# Trần Văn Lực – 20521587​
# Ngô Ngọc Sương - 20521852​
# Nguyễn Văn Hợp - 20521358​

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import os
from time import sleep

# đọc ghi file chứa id cần lấy comment của tất cả bài viết trong group cần lấy
def readData(fileName):
    f = open(fileName, 'r', encoding='UTF8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("error")
    return data
def writeFile(fileName, content):
    with open(fileName, 'a', encoding='UTF8') as f1:
        f1.write(content + os.linesep)

# Khởi tạo webdriver 
def initDriver():
    # Thêm option để tránh hiện thông báo lỗi tin nhắn ghi nhật ký chorme
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options) 
    return browser

# Thiết lập tự động thực hiện login vào facebook
def loginFacebook(browser, username, password):
    browser.get("https://mbasic.facebook.com/") 
    # TÌm phần tử để nhập tên người dùng
    # Nhập chuổi tên người dùng bằng phương thức send_keys
    textUserName = browser.find_element(By.ID, "m_login_email")
    textUserName.send_keys(username)
    textPassword = browser.find_element(By.NAME, "pass")
    textPassword.send_keys(password)
    textPassword.send_keys(Keys.ENTER) # Nhấn enter để đăng nhập
    sleep(50)

# Lấy comment của mỗi bài post
def getContentComment(driver):
    try:
        list_comments_of_a_post = []
        
        links = driver.find_elements(By.XPATH,'//a[contains(@href, "comment/replies")]') # lấy link của comment
        ids = []
        if (len(links)):
            for link in links:
                # lấy id của comment
                # chia thành chuỗi con 'ctoken=' để trích xuất ID nhận xét
                # chuỗi ID nhận xét được chia nhỏ hơn nữa trên ký tự & để xóa mọi tham số truy vấn bổ sung khỏi URL.
                takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0] 
                # Định vị phần tử trên trang web có chứa văn bản của nhận xét
                # Lấy comment dựa trên id của comment vừa lấy được ở trên
                textCommentElement = driver.find_element(By.XPATH,('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                if (takeLink not in ids):
                    # writeFile('comments.csv', textCommentElement.text)
                    list_comments_of_a_post.append(textCommentElement.text)
                    ids.append(takeLink)
        return ids, list_comments_of_a_post
    except:
        print("error get link")
        raise

# Thực hiện crawl comments từ mỗi bài post
def getAmountOfComments(driver, postId, numberCommentTake, list_comments):
    comments = []
    try:
        driver.get("https://mbasic.facebook.com/" + str(postId))
        # driver.get("https://mbasic.facebook.com/" + str(postId))
        # lấy comment của bài post
        sumLinks, list_comments_of_a_post = getContentComment(driver)
        comments.append(list_comments_of_a_post)
        # nếu só comment lấy được nhỏ hơn số comment cần lấy thì tiếp tục lấy
        while(len(sumLinks) < numberCommentTake):
            try:
                # tìm nút next để lấy thêm comment tiếp theo
                nextBtn = driver.find_elements(By.XPATH,'//*[contains(@id,"see_next")]/a')
                if (len(nextBtn)):
                    nextBtn[0].click()
                    sumLinks_more, list_comments_of_a_post_more = getContentComment(driver)
                    comments.append(list_comments_of_a_post_more)
                    sumLinks.extend(sumLinks_more)
                else:
                    break
            except:
                print('Error when cralw content comment')
        return comments
    except:
        print("Error get cmt")

def getPostIds(driver, filePath = 'posts.csv'):
    allPosts = readData(filePath) # Lấy danh sách các id bài viết đã lấy
    sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # cuộn xuống dưới
    shareBtn = driver.find_elements(By.XPATH,'//a[contains(@href, "/sharer.php")]') # Lấy các nút chia sẻ
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('sid=')[1].split('&')[0] # Lấy id của bài viết
            if postId not in allPosts:
                writeFile(filePath, postId) # Lưu id bài viết không trùng vào file

# Thực hiện việc lấy id từng bài viết của trang và lưu vào file post.csv
def getnumOfPostFanpage(driver, pageId, amount, filePath = 'posts.csv'):
    driver.get("https://touch.facebook.com/" + pageId)
    while len(readData(filePath)) < amount * 2:
        getPostIds(driver, filePath)


list_comments = []
browser = initDriver()

# user = input("Nhập tên đăng nhập:")
# passw = input("Nhập mật khẩu:")
# loginFacebook(browser, user, passw)
getnumOfPostFanpage(browser, 'neuconfessions', 10, './comments_crawl/posts.csv')

# Duyệt qua từng id của bài post
for postId in readData('./comments_crawl/posts.csv'):
    list_comments.append(getAmountOfComments(browser, postId, 10, list_comments))

print(len(list_comments))
browser.close()

data = { 'List Comments': list_comments }
pd.DataFrame(data).to_csv('./comments_crawl/comments.csv')
