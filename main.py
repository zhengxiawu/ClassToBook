from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import srt
import requests

waiting_interval = 4
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}


def waiting_with_xpath_click(browser, xpath):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
    browser.find_element_by_xpath(xpath).click()


def check_with_xpath_click(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath).click()
        return True
    except selenium_exceptions.NoSuchElementException:
        return False


def get_all_classes(browser):
    check_with_xpath_click(browser, '//div[@class="list-more"]')
    return browser.find_elements_by_xpath('//span[@class="list-title"]')


def get_classes_url_and_name(course_url):
    browser = webdriver.Chrome(executable_path='/Users/sherwood/.local/chromedriver')
    browser.get(course_url)
    elements = get_all_classes(browser)
    #网易云课堂存在两种模式的课程页面，分类处理
    time.sleep(waiting_interval)
    classes_link = []
    classes_name = []
    if len(elements) > 0:
        length = len(elements)
        for i in range(length):
            elements = get_all_classes(browser)
            span = elements[i]
            classes_name.append(span.text)
            span.click()
            time.sleep(waiting_interval)
            classes_link.append(browser.current_url)
            print(browser.current_url)
            browser.back()
            time.sleep(waiting_interval)
    else:
        container = browser.find_element_by_xpath('//table[@id="list2"]')
        browser.execute_script("arguments[0].style.display = 'block';", container)
        elements = browser.find_elements_by_xpath('//table[@id="list2"]//td[@class="u-ctitle"]/a')
        for i in elements:
            classes_name.append(i.text)
            classes_link.append(i.get_attribute('href'))
    browser.close()
    return classes_link, classes_name


def get_srt_url(url):
    browser = webdriver.Chrome(executable_path='/Users/sherwood/.local/chromedriver')
    # 利用硕鼠网站进行解析
    browser.get('http://www.flvcd.com/url.php')
    input_box = browser.find_element_by_xpath('//*[@id="kw"]')
    input_box.send_keys(url)
    browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/th/div/form/table/tbody/tr[4]/td/div/input').click()
    time.sleep(waiting_interval)
    zh_link_ = browser.find_element_by_xpath('/html/body/table/tbody/tr[4]/th/table[2]/tbody/tr[2]/td/a[1]')
    en_link_ = browser.find_element_by_xpath('/html/body/table/tbody/tr[4]/th/table[2]/tbody/tr[2]/td/a[2]')
    zh_en_link_ = browser.find_element_by_xpath('/html/body/table/tbody/tr[4]/th/table[2]/tbody/tr[2]/td/a[3]')
    zh_link = zh_link_.get_attribute('href')
    en_link = en_link_.get_attribute('href')
    zh_en_link = zh_en_link_.get_attribute('href')
    browser.close()
    return zh_link, en_link, zh_en_link


def download_srt(url):
    r = requests.get(url, headers=headers)
    string = r.text
    # req = urllib.request.Request(url=url, headers=headers)
    # output = urllib.request.urlopen(req).read()
    # charset = 'utf-8'
    # try:
    #     string = output.decode(charset)
    # except UnicodeDecodeError:
    #     charset = 'gbk'
    #     string = output.decode(charset)
    # print(charset)
    return list(srt.parse(string))


def get_str_from_srt_list(srt_):
    string_ = ''
    for i in srt_:
        string_ += i.content + ' '
    return string_


if __name__ == '__main__':
    # course_url = 'http://open.163.com/newview/movie/' \
    #              'courseintro?newurl=%2Fspecial%2Fopencourse%2Fpositivepsychology.html'
    course_url = 'http://open.163.com/special/sp/philosophy-death.html'
    name = 'Philosophy-Death'
    print('Get classes link')
    classes_link, classes_name = get_classes_url_and_name(course_url)
    print('Finish classes link')
    zh_en_fo = open("./book/{}_zh_en.txt".format(name), "a+")
    zh_fo = open("./book/{}_zh.txt".format(name), "a+")
    en_fo = open("./book/{}_en.txt".format(name), "a+")
    print('Get srt')
    for index, url in enumerate(classes_link):
        print(index)
        zh_link, en_link, zh_en_link = get_srt_url(url)
        zh_srt = download_srt(zh_link)
        zh_string = get_str_from_srt_list(zh_srt)
        zh_fo.write("\n\n\n Chapter {}: {}".format(str(index), classes_name[index]) + '\n\n\n')
        zh_fo.write(zh_string + '\n')
        en_srt = download_srt(en_link)
        en_string = get_str_from_srt_list(en_srt)
        en_fo.write("\n\n\n Chapter {}: {}".format(str(index), classes_name[index]) + '\n\n\n')
        en_fo.write(en_string + '\n')
        print(zh_en_link)
        zh_en_srt = download_srt(zh_en_link)
        zh_en_string = get_str_from_srt_list(zh_en_srt)
        zh_en_fo.write("\n\n\n Chapter {}: {}".format(str(index), classes_name[index]) + '\n\n\n')
        zh_en_fo.write(zh_en_string + '\n')
    zh_fo.close()
    en_fo.close()
    zh_en_fo.close()

    # url = 'http://open.163.com/newview/movie/free?pid=M6HV755O6&mid=M6HV8DF19'
    # zh_link, en_link, zh_en_link = get_srt_url(url)
    # zh_link = 'http://nos.netease.com/oc-caption-srt/oc-srt-1410862459469.srt'
    # a = download_srt(zh_link)
    #
    # fo = open("./book/test.txt", "a+")
    # fo.write(string_)
    # fo.close()
