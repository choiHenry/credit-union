class Capi:
    def __init__(self):
        districtList = ["서울", "경기", "인천", "부산", "대구", "광주", "대전",
                        "세종", "울산", "강원", "경북", "경남", "충북", "충남",
                        "전북", "전남", "제주"]
        self._districtList = districtList

    @property
    def districtList(self):

        return self._districtList

    @districtList.setter
    def districtList(self, districtList):

        self._districtList = districtList

    def saveBranchTables(self):
        from selenium import webdriver
        import re
        import pandas as pd
        import os

        if not os.path.exists('./data'):
            os.makedirs('./data')

        driver = webdriver.Chrome('./chromedriver')
        url = "http://cu.co.kr/cu/ad/cuSearch.do"
        driver.get(url)

        for district in self.districtList:
            driver.find_element_by_link_text(district).click()
            page = driver.find_element_by_xpath('//*[@id="contents"]/div/section/div[3]/p[2]').text
            pageNum = re.findall('\d', page)[1]

            driver.implicitly_wait(3)
            target = driver.find_elements_by_tag_name('table')
            html = target[0].get_attribute('outerHTML')
            table = pd.read_html(html, encoding='utf-8')[0]
            tables = [table]

            if (int(pageNum) <= 10):
                i = 2
                while (i <= int(pageNum)):
                    driver.find_element_by_link_text(str(i)).click()
                    driver.implicitly_wait(3)
                    target = driver.find_elements_by_tag_name('table')
                    html = target[0].get_attribute('outerHTML')
                    table = pd.read_html(html, encoding='utf-8')[0]
                    tables.append(table)
                    i += 1
            else:
                i = 2
                while (i <= 10):
                    driver.find_element_by_link_text(str(i)).click()
                    driver.implicitly_wait(3)
                    target = driver.find_elements_by_tag_name('table')
                    html = target[0].get_attribute('outerHTML')
                    table = pd.read_html(html, encoding='utf-8')[0]
                    tables.append(table)
                    i += 1
                driver.find_element_by_link_text('다음').click()
                driver.find_element_by_link_text(str(i)).click()
                driver.implicitly_wait(3)
                target = driver.find_elements_by_tag_name('table')
                html = target[0].get_attribute('outerHTML')
                table = pd.read_html(html, encoding='utf-8')[0]
                tables.append(table)
                i += 1
                while (i <= pageNum):
                    driver.find_element_by_link_text(str(i)).click()
                    driver.implicitly_wait(3)
                    target = driver.find_elements_by_tag_name('table')
                    html = target[0].get_attribute('outerHTML')
                    table = pd.read_html(html, encoding='utf-8')[0]
                    tables.append(table)
                    i += 1

            df = pd.concat(tables)
            df.reset_index(inplace=True)
            df.to_csv(f'/data/{district}.csv')