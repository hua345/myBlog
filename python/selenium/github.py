from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from lxml import etree
import time
import xlsxwriter


class githubUtil:
    # 对象初始化
    def __init__(self):
        url = 'https://github.com/trending'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10, 0.5)  # 超时时长为10s

    def getGithubTrending(self):
        self.browser.implicitly_wait(3)
        self.browser.get(self.url)
        print(self.browser.title)

    def getTrendingTitle(self):
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="Box"]//article[@class="Box-row"]')))
        trendingList = self.browser.find_elements_by_xpath(
            '//div[@class="Box"]//article[@class="Box-row"]')
        for trendingItem in trendingList:
            item = {}
            item["title"] = trendingItem.find_element_by_xpath(
                './h1').text.replace(' ', '')
            try:
                item["desc"] = trendingItem.find_element_by_xpath('./p').text
            except Exception as err:
                print('没有描述信息')
            print(item)

    def getLangTrending(self, lang):
        self.wait.until(EC.presence_of_element_located(
            (By.ID, 'select-menu-language')))
        self.browser.find_element_by_id("select-menu-language").click()
        selectLang = self.browser.find_element_by_id(
            "select-menu-language").find_element_by_xpath('.//filter-input[@class="select-menu-text-filter"]/input')
        selectLang.click()
        selectLang.send_keys("Go")
        time.sleep(1)
        ActionChains(self.browser).key_down(Keys.ENTER).perform()
        time.sleep(1)
        self.getTrendingTitle()

    def getSearch(self):
        self.browser.maximize_window()
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class="js-site-search-form"]/label/input')))
        searchElem = self.browser.find_element_by_xpath(
            '//form[@class="js-site-search-form"]/label/input[1]')
        # self.wait.until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, 'form.js-site-search-form label input')))
        # searchElem = self.browser.find_elements_by_css_selector(
        #     'form.js-site-search-form label input')[0]
        searchElem.click()
        searchElem.send_keys("stars:>=10000 sort:stars")
        time.sleep(1)
        ActionChains(self.browser).key_down(Keys.ENTER).perform()


if __name__ == "__main__":

    github = githubUtil()
    github.getGithubTrending()
    # github.getTrendingTitle()
    # github.getLangTrending("Go")
    github.getSearch()
