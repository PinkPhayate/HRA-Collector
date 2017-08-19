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
```


## Environment
+ python 3.6.0


# How to use

## スクレイピング

### 過去の情報を取得
	HRA-Collecter/src/page_scraping3.py
	- main関数のwordsを変更

### 当日の情報を取得
	HRA-Collecter/src/today_scraping3.py
	- main関数のridを対象レースに変更

## 予測
### モデルがそのレースで通用するか評価
	HRAnalyzer/Source3/history_race_analyzer.py
	- main関数のwordsを変更

### 当日レースを予測
	HRAnalyzer/Source3/today_scraping.py
	ターミナル引数にレースid
	main関数のwordsを変更

