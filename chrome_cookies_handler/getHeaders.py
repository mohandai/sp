def getHeaders(fileName):
    headers = []
    headList = ['User-Agent','Cookie']
    with open(fileName,'r') as fp:
        for line in fp.readlines():
            name,value = line.split(':',1)
            if name in headList:
                headers.append((name.strip(),value.strip()))
    return headers

def extract_cookies(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies

if __name__ == "__main__":
    cookie = getHeaders('headers.txt')
    #cookie = "continue=http://www.bj.10086.cn/service/fee/zdcx/; continuelogout=http://www.bj.10086.cn/service/fee/zdcx/; CmLocation=100|100; CmProvid=bj; WT_FPC=id=2e4f7c373760da4bead2e31489565793714:lv=1489635199762:ss=1489635053131; Webtrends=58.132.171.245.1489565794320746; JSESSIONID=0000UGBr1eur3P3Yp6EalieXCp8GP2T:16vf1jlcr; input_loginName=15210357242; c_loginName=15210357242; SSOTime=2017-03-15 16:17:16; mobileNo1=6251a6b7d69b5b5047495ale16ad8b5a5c149d6f2c0@@b50883ee4753ba0784210ce85435ee29c7oesl24a856f3@@1489565836722"
    c = cookie[0]
    cookies = extract_cookies(c[1])
    print(type(cookies))
    cookie_keys = cookies.keys()
    print(cookies)
    for c in cookie_keys:
        print(c,' with: ', cookies[c])