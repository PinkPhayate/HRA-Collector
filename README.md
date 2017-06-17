# HRA-collctor

## Discription
This repository works to collect horse data amd race record by crawling web.

## Requirement
+ mysql(pythonモジュールをインストールするのに必要)
+ docker-compose
　　
```
docker-compose up
pip install --r ./src/requirement.txt
mysql -u root -p -h 127.0.0.1 -P 3333 < hra_2017-05-28.sql
python test.py

``


## Environment
+ python 3.6.0

## ForUse
