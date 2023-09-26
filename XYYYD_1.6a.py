import time
import requests
import random
import re
import config
import threading
import JhWxPusher
import getWxInfo
from urllib.parse import urlparse, parse_qs
#公众号字典
checkDict={
'MzkxNTE3MzQ4MQ==':['香姐爱旅行','gh_54a65dc60039'],
'Mzg5MjM0MDEwNw==':['我本非凡','gh_46b076903473'],
'MzUzODY4NzE2OQ==':['多肉葡萄2020','gh_b3d79cd1e1b5'],
'MzkyMjE3MzYxMg==':['Youhful','gh_b3d79cd1e1b5'],
'MzkxNjMwNDIzOA==':['少年没有乌托邦3','gh_b3d79cd1e1b5'],
'Mzg3NzUxMjc5Mg==':['星星诺言','gh_b3d79cd1e1b5'],
'Mzg4NTcwODE1NA==':['斑马还没睡123','gh_b3d79cd1e1b5'],
'Mzk0ODIxODE4OQ==':['持家妙招宝典','gh_b3d79cd1e1b5'],
'Mzg2NjUyMjI1NA==':['Lilinng','gh_b3d79cd1e1b5'],
'MzIzMDczODg4Mw==':['有故事的同学Y','gh_b3d79cd1e1b5'],
'Mzg5ODUyMzYzMQ==':['789也不行','gh_b3d79cd1e1b5'],
'MzU0NzI5Mjc4OQ==':['皮蛋瘦肉猪','gh_58d7ee593b86'],
'Mzg5MDgxODAzMg==':['北北小助手','gh_58d7ee593b86'],
'MzkxNDU1NDEzNw==': ['小阅阅服务', 'gh_e50cfefef9e5'],
}
def getmsg():
    lvsion = 'v1.6a'
    r=''
    try:
        u='http://175.24.153.42:8881/getmsg'
        p={'type':'xyyyd'}
        r=requests.get(u,params=p)
        rj=r.json()
        version=rj.get('version')
        gdict = rj.get('gdict')
        gmmsg = rj.get('gmmsg')
        print('系统公告:',gmmsg)
        print(f'最新版本{version}当前版本{lvsion}')
        print(f'系统的公众号字典{len(gdict)}个:{gdict}')
        print(f'本脚本公众号字典{len(checkDict.values())}个:{list(checkDict.keys())}')
        s=len(gdict)
        l=len(checkDict.values())
        if s>l:
            print(f'新增了{s-l}个过检测字典，快手动去脚本的checkDict里添加吧')
        print('='*50)
    except Exception as e:
        print(r.text)
        print(e)
        print('公告服务器异常')

def ts():
    return str(int(time.time()))+'000'

class HHYD():
    def __init__(self,txbz,cg):
        self.cg=cg
        self.name=cg['name']
        self.key=cg["key"]
        self.ysmuid=cg["ck"]
        self.devid=cg['devid']
        self.txbz=txbz
        self.headers={
            'Host': '1694829964.njzyl.top',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://1694829964.njzyl.top/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'ysmuid={self.ysmuid};',
        }
        self.sec=requests.session()
        self.sec.headers=self.headers
        self.lastbiz=''

    def setstatus(self):
        try:
            u = 'http://175.24.153.42:8882/setstatus'
            p = {'key': self.key, 'type': 'xyyyd', 'val': '1'}
            r = requests.get(u, params=p,timeout=10)
            print(self.name, r.text)
        except Exception as e:
            print('设置状态异常')
            print(e)

    def getstatus(self):
        try:
            u = 'http://175.24.153.42:8882/getstatus'
            p = {'key': self.key, 'type': 'xyyyd'}
            r = requests.get(u, params=p,timeout=3)
            return r.text
        except Exception as e:
            print('查询状态异常',e)
            return False

    def printjson(self,text):
        if printf == 0:
            return
        print(self.name,text)
    def init(self):
        try:
            r=self.sec.get('http://1694829964.njzyl.top/')
            htmltext = r.text
            res1 = re.sub('\s', '', htmltext)
            exchangeUrl = re.findall('"target="_blank"href="(.*?)">提现<', res1)
            ysm_uid = re.findall('\{unionid="(.*?)"', res1)
            #print(ysm_uid)
            #print(exchangeUrl)
            if ysm_uid == []:
                print(self.name, '初始化失败,账号异常,获取ysm_uid失败')
                return False
            else:
                self.ysm_uid = ysm_uid[0]
                if exchangeUrl == []:
                    print(self.name, '初始化失败,账号异常，获取exchangeUrl失败')
                    return False
                else:
                    self.eurl = exchangeUrl[0]
                return True
        except:
            print(self.name,'初始化失败,请检查你的ck')
            return False
    def user_info(self):
        u=f'http://1694829964.njzyl.top/yunonline/v1/sign_info?time={ts()}000&unionid={self.ysm_uid}'
        r=''
        try:
            r=self.sec.get(u)
            rj=r.json()
            if rj.get('errcode')==0:
                self.printjson(r.json())
                return True
            else:
                print(self.name,f'获取用户信息失败，账号异常，请查看你的账号是否正常')
                return False
        except:
            print(self.name,r.text)
            print(self.name,f'获取用户信息失败,gfsessionid无效，请检测gfsessionid是否正确')
            return False
    def hasWechat(self):
        r=''
        try:
            u=f'http://1694829964.njzyl.top/yunonline/v1/hasWechat?unionid={self.ysm_uid}'
            r=self.sec.get(u)
            self.printjson(r.json())
        except:
            print(self.name,r.text)
            return False
    def gold(self):
        r=''
        try:
            u=f'http://1694829964.njzyl.top/yunonline/v1/gold?unionid={self.ysm_uid}&time={ts()}000'
            r=self.sec.get(u)
            self.printjson(r.json())
            rj = r.json()
            self.remain=rj.get("data").get("last_gold")
            print(self.name,f'今日已经阅读了{rj.get("data").get("day_read")}篇文章,剩余{rj.get("data").get("remain_read")}未阅读，今日获取金币{rj.get("data").get("day_gold")}，剩余{self.remain}')
        except:
            print(self.name,r.text)
            return False
    def devtouid(self):
        u = f'http://1694829964.njzyl.top/yunonline/v1/devtouid'
        p=f'unionid={self.ysm_uid}&devid={self.devid}'
        r = self.sec.post(u,data=p)
        print(self.name,'模拟上传设备指纹:',r.text)
    def getKey(self):
        u='http://1694829964.njzyl.top/yunonline/v1/wtmpdomain'
        p=f'unionid={self.ysm_uid}'
        r=requests.post(u,headers=self.headers,data=p)
        self.printjson(r.text)
        rj=r.json()
        domain=rj.get('data').get('domain')
        pp = parse_qs(urlparse(domain).query)
        hn = urlparse(domain).netloc
        uk = pp.get('uk')[0]
        self.printjson(f'get ydkey is {uk}')
        h = {
            'Host': 'nsr.zsf2023e458.cloud',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Origin': f'https://{hn}',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh',
        }
        return uk, h
    def read(self):
        self.falg=0
        info = self.getKey()
        time.sleep(3)
        self.params = {'uk': info[0]}
        while True:
            u = f'https://nsr.zsf2023e458.cloud/yunonline/v1/do_read'
            r = requests.get(u, headers=info[1], params=self.params)
            print(self.name,'-' * 50)
            self.printjson(r.json())
            rj = r.json()
            if rj.get('errcode') == 0:
                link=rj.get('data').get('link')
                wxlink=self.jump(link)
                a = getWxInfo.getinfo(wxlink)
                if self.testCheck(a, wxlink) == False:
                    return False
                self.printjson(f'this:{a[4]}|last:{self.lastbiz}')
                if a[4]==self.lastbiz:
                    self.falg+=1
                else:
                    self.falg=0
                if self.falg>=2:
                    print(f'{self.name}小阅阅阅读异常脚本')
                    JhWxPusher.push(self.cg['name']+'阅读异常', wxlink, a[3]+'\n'+'阅读异常脚本已停止，请手动打开活动查看情况', 'xyyyd', self.cg['uids'], self.key)
                    return False
                self.lastbiz = a[4]
                tsm = random.randint(7, 10)
                print(self.name,f'本次模拟读{tsm}秒')
                time.sleep(tsm)
                u1 = f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={info[0]}&time={tsm}&timestamp={ts()}'
                r1 = requests.get(u1, headers=info[1])
                self.printjson(r1.text)
            elif rj.get('errcode') == 405:
                print(self.name,'阅读重复')
                time.sleep(1.5)
            elif rj.get('errcode') == 407:
                print(self.name,'阅读结束')
                print(self.name,rj)
                return True
            else:
                print(self.name,'未知情况')
                time.sleep(1.5)
    def testCheck(self,a,url):
        if a == False:
            print(self.name, '解析文章链接失败')
            return True
        if a[4] == []:
            print(self.name,'这个链接没有获取到微信号id', url)
            return True
        if checkDict.get(a[4]) != None:
            self.setstatus()
            for i in range(60):
                if i % 30 == 0:
                    JhWxPusher.push(self.cg['name'], url, a[3], 'xyyyd',self.cg['uids'],self.key)
                getstatusinfo = self.getstatus()
                if getstatusinfo == '0':
                    print(self.name,'过检测文章已经阅读')
                    return True
                elif getstatusinfo == '1':
                    print(self.name,f'正在等待过检测文章阅读结果{i}秒。。。')
                    time.sleep(1)
                else:
                    print(self.name, f'回调服务器请求超时，等待中{i}秒。。。')
                    time.sleep(1)
            print(self.name,'过检测超时中止脚本防止黑号')
            return False
        else:return True
    def jump(self,link):
        print(self.name,'开始本次阅读')
        hn = urlparse(link).netloc
        h={
            'Host': hn,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Cookie': f'ysmuid={self.ysmuid}',
        }
        r = requests.get(link, headers=h,allow_redirects=False)
        self.printjson(r.status_code)
        Location=r.headers.get('Location')
        self.printjson(Location)
        return Location
    def withdraw(self):
        if int(self.remain)<self.txbz:
            print(self.name,'没有达到提现标准')
            return False
        b = urlparse(self.eurl)
        host = b.netloc
        querydict = parse_qs(b.query)
        h = {
            'Host': host,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': f'http://{host}',
            'Referer': self.eurl,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh',
            'Cookie': f'ysmuid={self.ysmuid}; ejectCode=1',
        }
        gold = int(int(self.remain) / 1000) * 1000
        print(self.name, '本次提现金币', gold)
        if gold:
            unionid = querydict.get('unionid')[0]
            request_id = querydict.get('request_id')[0]
            u1 = f'http://{host}/yunonline/v1/user_gold'
            p1 = f'unionid={unionid}&request_id={request_id}&gold={gold}'
            r = requests.post(u1, headers=h, data=p1)
            gold1 = getmsg.__name__
            self.printjson(r.json())
            u = f'http://1695460025.snak.top/yunonline/v1/withdraw'
            p = f'unionid={unionid}&signid={request_id}&ua=0&ptype=0&paccount=&pname='
            r = requests.post(u, headers=h, data=p)
            print(self.name, '提现结果', r.json())
    def run(self):
        if self.init():
            self.user_info()
            self.hasWechat()
            self.gold()
            self.devtouid()
            time.sleep(3)
            self.read()
            time.sleep(3)
            self.gold()
            time.sleep(3)
            self.withdraw()
if __name__ == '__main__':
    printf = config.printf
    getmsg()
    tl=[]
    if config.threadingf == 1:
        for i in config.xyyconfig:
            print('*' * 50)
            print(f'开始执行{i["name"]}')
            api = HHYD(config.xyytxbz,i)
            t = threading.Thread(target=api.run, args=())
            tl.append(t)
            t.start()
            time.sleep(0.5)
        for t in tl:
            t.join()
    elif config.threadingf == 0:
        for i in config.xyyconfig:
            print('*' * 50)
            print(f'开始执行{i["name"]}')
            api = HHYD(config.xyytxbz,i)
            api.run()
            print(f'{i["name"]}执行完毕')
            time.sleep(3)
    else:
        print('请确定config配置文件中threadingf参数是否正确')
    print('全部账号执行完成')