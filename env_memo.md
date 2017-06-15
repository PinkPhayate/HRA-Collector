#mongodb

+ mongodb起動

```
mongod -dbpath /usr/local/var/mongodb

```

+ クライアント側の操作

```
# 起動
mongo
# データベースの確認と使用するデータベース選択
show dbs
use hra
# テーブル一覧を表示
show collectionss
# テーブル作成
db.createCollection('res');
```


## architect

```
hra - hist	#　key: race_id, value: entried_horses

	- - res #  key* raceid, value: 各馬券のオッズ
```

```
{
	uid: xxxxx,
	rid: *****,
	hid: 123456789,
	record: {
				frame: 1,
				num: 1,
				age: 3,
				rank: 1,
				.....
				}
}

```

##mysql
+ mysqlの起動

	```
	sudo ./usr/local/mysql-5.7.18-macos10.12-x86_64/support-files/mysql.server start
	```

	**mysql.serverがあるところにパスを貼っておく**

+ mysqlの文字コード変更

	```
	alter table history character set utf8;
	```
	もしできない場合：カラムのencodingをutf8mb4に文字コードを変える
	

+ **mysqlのdumpファイルをgithubかなんかに保存しておかないとマイグレーションできない**


### mysql起動時rror
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
/usr/local/var/mysql/~.error

+ エラーログ確認

+ 解決方法
mysqlディレクトリの権限が_mysqlになっていたらユーザ名に変更

```
cd /usr/local/var/
sudo chown -R phayate mysql
```

# dockerファイルの作成
docker-composeを使って、使用するサーバを用意することができる。
docker-compose.yamlはHRAna-prvtの方にある。

## 接続コマンド
- mysql
mysql -u root -p -h 127.0.0.1 --port 3333

- nosql
接続コマンド分からないけど、接続はできる

