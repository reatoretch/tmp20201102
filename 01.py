# ===========================================
# フィックスポイント プログラミング試験問題 2020
# ===========================================
# A社の監視システムでは、監視対象となる複数台のサーバに対して一定間隔でping応答確認を行っており、
# 確認結果は以下に示すカンマ区切りの形式で1行ずつ監視ログファイルに追記される。
# -------------------------------------------------
# ＜確認日時＞,＜サーバアドレス＞,＜応答結果＞
# -------------------------------------------------
# 確認日時は、YYYYMMDDhhmmssの形式。ただし、年＝YYYY（4桁の数字）、月＝MM（2桁の数字。以下同様）、日＝DD、時＝hh、分＝mm、秒＝ssである。
# サーバアドレスは、ネットワークプレフィックス長付きのIPv4アドレスである。
# 応答結果には、pingの応答時間がミリ秒単位で記載される。ただし、タイムアウトした場合は"-"(ハイフン記号)となる。

# 以下に監視ログの例（抜粋）を示す。
# -------------------------------------------------
# 20201019133124,10.20.30.1/16,2  
# 20201019133125,10.20.30.2/16,1
# 20201019133134,192.168.1.1/24,10
# 20201019133135,192.168.1.2/24,5
# 20201019133224,10.20.30.1/16,522
# 20201019133225,10.20.30.2/16,1
# 20201019133234,192.168.1.1/24,8
# 20201019133235,192.168.1.2/24,15
# 20201019133324,10.20.30.1/16,-
# 20201019133325,10.20.30.2/16,2
# -------------------------------------------------

# >> subnet_ips
# {  '10.20.0.0/16': [ '10.20.30.1/16',  '10.20.30.2/16'],
#  '192.168.1.0/24': ['192.168.1.1/24', '192.168.1.2/24']}

from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="hogehuga")
parser.add_argument('filepath', default="log01.txt" ,help="対象となる監視ログファイルへのPATH")

history = {}

def showDateTime(dt):
    return f"{dt.year}年{dt.month}月{dt.day}日{dt.hour}:{dt.minute}:{dt.second}"

# ex) "20201019133325" → datetime.datetime(2020,10,19,13,33,25)
def str2date(dateTime):
    return datetime(year=int(dateTime[:4]), month=int(dateTime[4:6]), day=int(dateTime[6:8]), hour=int(dateTime[8:10]), minute=int(dateTime[10:12]), second=int(dateTime[12:]))


# 設問1
# 監視ログファイルを読み込み、故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成せよ。
# 出力フォーマットは任意でよい。
# なお、pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、次にpingの応答が返るまでを故障期間とする。

def main01():
    history.clear()
    args = parser.parse_args()
    timeoutCnt = {}
    with open(args.filepath,"r") as f:
        for line in f:
            dateTime,ipAddress,resTime = line.split(",")
            history.setdefault(ipAddress,[])
            timeoutCnt.setdefault(ipAddress,0)
            if "-" in resTime:
                timeoutCnt[ipAddress] += 1
                if 1 == timeoutCnt[ipAddress]:
                    history[ipAddress].append(str2date(dateTime))
            else:
                if timeoutCnt[ipAddress] >= 1:
                    history[ipAddress].append(str2date(dateTime))
                elif 0 < timeoutCnt[ipAddress]:
                    try:
                        del history[ipAddress][-1]
                    except:
                        pass
                timeoutCnt[ipAddress] = 0

        for ip in history:
            if not history[ip]:
                continue
            print(f"サーバアドレス：{ip}")
            date = history[ip]
            for i,k in enumerate(range(0,len(history[ip]),2)):
                try:
                    timedelta = date[k+1] - date[k]
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                except:
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～現在まで")

    return "success!!"

# 設問2
# ネットワークの状態によっては、一時的にpingがタイムアウトしても、一定期間するとpingの応答が復活することがあり、
# そのような場合はサーバの故障とみなさないようにしたい。
# N回以上連続してタイムアウトした場合にのみ故障とみなすように、設問1のプログラムを拡張せよ。
# Nはプログラムのパラメータとして与えられるようにすること。


parser.add_argument('--N', type=int, default=1 ,help="何回以上の連続タイムアウトで故障とみなすかの閾値")

def main02():
    history.clear()
    args = parser.parse_args()
    timeoutCnt = {}
    with open(args.filepath,"r") as f:
        for line in f:
            dateTime,ipAddress,resTime = line.split(",")
            history.setdefault(ipAddress,[])
            timeoutCnt.setdefault(ipAddress,0)
            if "-" in resTime:
                timeoutCnt[ipAddress] += 1
                if 1 == timeoutCnt[ipAddress]:
                    history[ipAddress].append(str2date(dateTime))
            else:
                if timeoutCnt[ipAddress] >= args.N:
                    history[ipAddress].append(str2date(dateTime))
                elif 0 < timeoutCnt[ipAddress]:
                    try:
                        del history[ipAddress][-1]
                    except:
                        pass
                timeoutCnt[ipAddress] = 0

        for ip in history:
            if not history[ip]:
                continue
            print(f"サーバアドレス：{ip}")
            date = history[ip]
            for i,k in enumerate(range(0,len(history[ip]),2)):
                try:
                    timedelta = date[k+1] - date[k]
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                except:
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～現在まで")

    return "success!!"

# 設問3
# サーバが返すpingの応答時間が長くなる場合、サーバが過負荷状態になっていると考えられる。
# そこで、直近m回の平均応答時間がtミリ秒を超えた場合は、サーバが過負荷状態になっているとみなそう。
# 設問2のプログラムを拡張して、各サーバの過負荷状態となっている期間を出力できるようにせよ。mとtはプログラムのパラメータとして与えられるようにすること。

parser.add_argument('--m', type=int, default=1 ,help="直近m回の平均応答時間")
parser.add_argument('--t', type=int, default=1 ,help="直近m回の平均応答時間がt")

def main03():
    history.clear()
    args = parser.parse_args()
    timeoutCnt = {}
    overloadCnt = {}
    overload_hist = {}
    overload_result = {}
    with open(args.filepath,"r") as f:
        for line in f:
            dateTime,ipAddress,resTime = line.split(",")

            history.setdefault(ipAddress,[])
            timeoutCnt.setdefault(ipAddress,0)
            overloadCnt.setdefault(ipAddress,0)
            overload_hist.setdefault(ipAddress,[])
            overload_result.setdefault(ipAddress,[])

            if  len(overload_hist[ipAddress]) < args.m-1:
                try:
                    response = int(resTime.replace("\n",""))
                except:
                    response = 1000
                overload_hist[ipAddress].append(response)

            else:
                try:
                    response = int(resTime.replace("\n",""))
                except:
                    response = 1000
                overload_hist[ipAddress].append(response)

                if sum(overload_hist[ipAddress])/3 > args.t:
                    overloadCnt[ipAddress] += 1
                    if 1 == overloadCnt[ipAddress]:
                        overload_result[ipAddress].append(str2date(dateTime))
                else:
                    if overloadCnt[ipAddress] >= 1:
                        overload_result[ipAddress].append(str2date(dateTime))

                    overloadCnt[ipAddress] = 0
                # 尺取法
                del overload_hist[ipAddress][0]
                overload_hist[ipAddress].append(response)

            if "-" in resTime:
                timeoutCnt[ipAddress] += 1
                if 1 == timeoutCnt[ipAddress]:
                    history[ipAddress].append(str2date(dateTime))
            else:
                if timeoutCnt[ipAddress] >= args.N:
                    history[ipAddress].append(str2date(dateTime))
                elif 0 < timeoutCnt[ipAddress]:
                    try:
                        del history[ipAddress][-1]
                    except:
                        pass
                timeoutCnt[ipAddress] = 0

        for ip in history:
            if not history[ip]:
                continue
            print(f"サーバアドレス：{ip}")
            date = history[ip]
            for i,k in enumerate(range(0,len(history[ip]),2)):
                try:
                    timedelta = date[k+1] - date[k]
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                except:
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～現在まで")

        print("\n-----過負荷期間の出力-----\n")
        for ip in overload_result:
            if not overload_result[ip]:
                continue
            print(f"サーバアドレス：{ip}")
            date = overload_result[ip]
            for i,k in enumerate(range(0,len(history[ip]),2)):
                try:
                    timedelta = date[k+1] - date[k]
                    print(f"過負荷期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                except:
                    print(f"過負荷期間{i+1}： {showDateTime(date[k])}～現在まで") 
    
    return "success!!"

# 設問4
# ネットワーク経路にあるスイッチに障害が発生した場合、そのスイッチの配下にあるサーバの応答がすべてタイムアウトすると想定される。
# そこで、あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、
# そのサブネット（のスイッチ）の故障とみなそう。
# 設問2または3のプログラムを拡張して、各サブネット毎にネットワークの故障期間を出力できるようにせよ。

import ipaddress as ipa

parser.add_argument('-s', '--subnetflag', action='store_true' ,help="サブネット出力可否")

def network(address):
    return str(ipa.IPv4Interface(address).network)

def main04():
    history.clear()
    args = parser.parse_args()
    timeoutCnt = {}
    with open(args.filepath,"r") as f:
        for line in f:
            dateTime,ipAddress,resTime = line.split(",")
            history.setdefault(ipAddress,[])
            timeoutCnt.setdefault(ipAddress,0)
            if "-" in resTime:
                timeoutCnt[ipAddress] += 1
                if 1 == timeoutCnt[ipAddress]:
                    history[ipAddress].append(str2date(dateTime))
            else:
                if timeoutCnt[ipAddress] >= args.N:
                    history[ipAddress].append(str2date(dateTime))
                elif 0 < timeoutCnt[ipAddress]:
                    try:
                        del history[ipAddress][-1]
                    except:
                        pass
                timeoutCnt[ipAddress] = 0
        
        subnet_ips = {}
        for ip in history:
            subnet_ips.setdefault(network(ip),[])
            subnet_ips[network(ip)].append(ip)
        
        subnet_hist = {}
        for ips in subnet_ips:
            cmpVal = len(subnet_ips)
            subnet_hist.setdefault(ips,[])
            merged_hist = []
            for ip in subnet_ips[ips]:
                if not history[ip]:
                    break
                date = history[ip]
                for i in range(0,len(history[ip]),2):
                    try:
                        merged_hist.append([date[i],"start"])
                        merged_hist.append([date[i+1],"end"])
                    except:
                        pass
            
            sorted_merged_hist = sorted(merged_hist)

            cnt = 0;flag = 0
            for hiduke,seflag in sorted_merged_hist:
                if "s" in seflag:
                    cnt += 1
                elif flag and "e" in seflag:
                    subnet_hist[ips].append(hiduke)
                    cnt = 0;flag = 0
                else:
                    cnt -= 1
                if cnt == cmpVal:
                    subnet_hist[ips].append(hiduke)
                    flag = 1

        for ip in history:
            if not history[ip]:
                continue
            print(f"サーバアドレス：{ip}")
            date = history[ip]
            for i,k in enumerate(range(0,len(history[ip]),2)):
                try:
                    timedelta = date[k+1] - date[k]
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                except:
                    print(f"故障期間{i+1}： {showDateTime(date[k])}～現在まで")
        
        if args.subnetflag:
            print("\n-----サブネット毎の出力-----\n")
            for ip in subnet_hist:
                if subnet_hist[ip]:
                    print(f"ネットワークアドレス：{ip}")
                date = subnet_hist[ip]
                for i,k in enumerate(range(0,len(subnet_hist[ip]),2)):
                    try:
                        timedelta = date[k+1] - date[k]
                        print(f"故障期間{i+1}： {showDateTime(date[k])}～{showDateTime(date[k+1])}まで ({timedelta})")
                    except:
                        print(f"故障期間{i+1}： {showDateTime(date[k])}～現在まで") 
        
    return "success!!"

if __name__ == "__main__":
    print("\n-----------------------設問1-----------------------")
    main01()
    print("\n-----------------------設問2-----------------------")
    main02()
    print("\n-----------------------設問3-----------------------")
    main03()
    print("\n-----------------------設問4-----------------------")
    main04()

# ※解答をする上での注意
# 設問では明示しきれていない細かな仕様については、各自、妥当な範囲で補ってよい。
# プログラムの実行方法や内容を説明するドキュメントも作成すること。
# 作成したプログラムはテストを行い、使用したテストデータと結果についても合わせて提出すること。