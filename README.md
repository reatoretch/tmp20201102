# code test

## Usage
実行
```bash
python 01.py log.txt --N 2 --m 3 --t 20 -s
```
引数の説明
```
filepath: 対象となる監視ログファイルへのPATH
--N: 故障とみなすタイムアウト回数
--m: 直近m回の平均応答時間
--t: 直近m回の平均応答時間t
-s (--subnet): サブネット毎の出力可否（デフォルトでTrue）
```
実行結果
```

-----------------------設問1-----------------------
サーバアドレス：10.20.30.1/16
故障期間1： 2020年10月19日13:33:24～2020年10月19日13:33:53まで (0:00:29)
故障期間2： 2020年10月19日13:34:11～2020年10月19日13:34:22まで (0:00:11)
サーバアドレス：10.20.30.2/16
故障期間1： 2020年10月19日13:31:25～2020年10月19日13:32:25まで (0:01:00)
故障期間2： 2020年10月19日13:33:25～2020年10月19日13:33:58まで (0:00:33)

-----------------------設問2-----------------------
サーバアドレス：10.20.30.1/16
故障期間1： 2020年10月19日13:33:24～2020年10月19日13:33:53まで (0:00:29)
サーバアドレス：10.20.30.2/16
故障期間1： 2020年10月19日13:33:25～2020年10月19日13:33:58まで (0:00:33)

-----------------------設問3-----------------------
サーバアドレス：10.20.30.1/16
故障期間1： 2020年10月19日13:33:24～2020年10月19日13:33:53まで (0:00:29)
サーバアドレス：10.20.30.2/16
故障期間1： 2020年10月19日13:33:25～2020年10月19日13:33:58まで (0:00:33)

-----過負荷期間の出力-----

サーバアドレス：10.20.30.1/16
過負荷期間1： 2020年10月19日13:33:24～現在まで
サーバアドレス：10.20.30.2/16
過負荷期間1： 2020年10月19日13:33:25～現在まで

-----------------------設問4-----------------------
サーバアドレス：10.20.30.1/16
故障期間1： 2020年10月19日13:33:24～2020年10月19日13:33:53まで (0:00:29)
サーバアドレス：10.20.30.2/16
故障期間1： 2020年10月19日13:33:25～2020年10月19日13:33:58まで (0:00:33)

-----サブネット毎の出力-----

ネットワークアドレス：10.20.0.0/16
故障期間1： 2020年10月19日13:33:25～2020年10月19日13:33:53まで (0:00:28)
```

## Description
### 設問01
pingがタイムアウトした最初の時刻とタイムアウトから復帰した時刻を格納した配列で値を保持  
try-exceptは配列が[タイムアウト開始,タイムアウト終了,タイムアウト開始]という場合に  
最後の要素について「タイムアウト開始～現在まで」と出力することを意図している  
### 設問02
設問01の「if timeoutCnt[ipAddress] >= 1:」を「if timeoutCnt[ipAddress] >= args.N:」とすることで  
任意回数のタイムアウトで障害を検知  
### 設問03
設問02のtimeoutCntの構造を利用した過負荷期間用overloadCntを用意した  
実行時引数で指定されるm個分のresTime(応答時間)が貯まった時点を過負荷期間の開始時としている  
また、タイムアウトは1000msとして過負荷期間の算出に利用している
### 設問04
ネットワークアドレスにはサブネット部が含まれるので各IPアドレスのサブネットを算出後  
サブネット内のネットワークの故障期間が重複している部分をサブネットの故障期間として算出  
元々出力される故障期間は[開始,終了,開始,終了]というデータなので一つのデータにまとめた後に  
時刻でソートをすると[開始,開始,終了,終了]というデータになる  
開始を+1、終了を-1とすると線形に探索して初めてサブネット内のネットワーク数と一致した瞬間から  
次に初めて終了を発見した瞬間が故障期間が重複しているサブネットの故障期間となる  
 
## Author
[reatoretch](https://github.com/reatoretch)
