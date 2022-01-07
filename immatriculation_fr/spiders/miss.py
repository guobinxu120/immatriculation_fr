# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from collections import OrderedDict
from scrapy.http import TextResponse
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time, json, os, csv

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class immatriculation_frSpider(Spider):
    name = "miss"
    start_url = 'https://immatriculation.ants.gouv.fr/Services-associes/Ou-immatriculer-mon-vehicule?displayMap=list&deptNumber={}&types%5B0%5D=garage&order=town'
    domain1 = 'https://reseau.citroen.fr'

    driver = None
    conn = None
    use_selenium = True
    total_message_count = 0
    field_names = ['URL', 'Nom', 'Adresse', 'Tel',
                   'Email', 'Map', 'Latitude', 'Longitude', 'Horraires',  'Web site']

    total_count = 0
    all_data = []

    def start_requests(self):
        fname = 'result_imma_final_1.csv'

        def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
           csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
           for row in csv_reader:
               yield [cell for cell in row]

        # filename = 'da.csv'
        reader = unicode_csv_reader(open(fname, encoding='utf-8'))

        for i, row in enumerate(reader):
            if i == 0:
                continue

            if i > 15000:
                url = row[0]
                item = OrderedDict()
                for j, field_name in enumerate(self.field_names):
                    if j == 9:
                        item[field_name] = ''
                    else:
                        item[field_name] = row[j]
                yield Request(url, self.parseProduct, meta={'item': item})
                # break


        # f2 = open('result_imma_final_1.csv')
        #
        # csv_items = csv.DictReader(f2)
        # cat_data = {}
        #
        # for i, row in enumerate(csv_items):
        #     self.all_data.append(row)
        # f2.close()
        #
        # print('\n################################')
        # print('total count: ' + str(len(self.all_data)))
        # print('################################\n')
        #
        # for i, d in enumerate(self.all_data):
        #     url = d['URL']
        #     yield Request(url, self.parseProduct, meta={'item': d})
        #     break

    def parseProduct(self, response):
        item = response.meta.get('item')

        datas = response.xpath('//div[@class="article-intro"]//text()').extract()
        site = ''
        for i, d in enumerate(datas):
            d = d.strip()
            if 'Site web' in d:
                site = datas[i + 1]
                break
        item['Web site'] = site

        self.total_count += 1
        print('Total count: ' + str(self.total_count))

        yield item
