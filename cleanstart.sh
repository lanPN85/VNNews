#!/usr/bin/env bash
rm files/*.txt
mysql -u lanpn -p <purge.sql
scrapy crawl dantri
scrapy crawl kenh14
scrapy crawl vnexpress
scrapy crawl vietnamnet
scrapy crawl vtv
scrapy crawl vietbao
scrapy crawl danviet
scrapy crawl vov
scrapy crawl vnplus
scrapy crawl thanhnien
scrapy crawl btt
scrapy crawl ttvh
