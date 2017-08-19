# encoding=utf-8
import json
import base64
import requests
import pickle

MANUAL = True
READFROMFILE = False

"""
输入你的微博账号和密码，可去淘宝买，一元七个。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    {'no': '13557261116', 'psw': 'awmsx6017'},
]


manual_cookies = [
 {'SCF': 'AmRud45bRgYaA6Ekt8DxOSgwlhgrXDKgIjeod-5VUcts-_lejW-L8XvU1JIfWu5oiYBzGxYzSIm8aZK55DtcHSI.',
  'SSOLoginState': '1500621629',
  'SUB': '_2A250ddttDeRhGeBP7lsV8yjLyD6IHXVXmeUlrDV6PUJbkdBeLWilkW0G7Qek3FF45h5MG_uEyxdcwEi9Bw..',
  'SUHB': '0D-1QQjAOB1L_N',
  '_T_WM': 'bbaf70a5ad397c9009afb869fb30a183'},
 {'SCF': 'ApekUUC4eGitAw8IfwLVJSCbr8picW9kH6DH18Z6vBCbZXJpDCtz-8t7B765LzVFVri3Os2ITHoKWuV9mJsLdhI.',
  'SSOLoginState': '1500621849',
  'SUB': '_2A250ddxIDeRhGeBP7VIU8ivOzzmIHXVXmeQArDV6PUJbkdBeLVf6kW0lRzzujGEU3Dif3IX6Q9kWrL4GDw..',
  'SUHB': '0C1yjYzV4gaZYc',
  '_T_WM': '2de45e90beedcc7198d38114e791950f'},
 {'SCF': 'AhggL9u4_C-y0ZdDB3sg5ZMij2v-Dica4GAztw_6pW6tQ20ao8-OYEGX_r2Se3QAvOYMIQR1BCIJv26Qumuhrhs.',
  'SSOLoginState': '1500621976',
  'SUB': '_2A250ddzIDeRhGeBP7lsV8SbJzDmIHXVXmeSArDV6PUJbkdBeLULSkW1js9IbTRtgwL9sr8oJHORbcob1ZQ..',
  'SUHB': '05iKElw_Q5ezhW',
  '_T_WM': 'd982d7e143d40d06bc066ad7765049d3'},
 {'SCF': 'AseknkHEidXuAiSUdGIX7jxDOxLUTsrAdiqZsLkJOkoShaXxDi4LBtST4XgJgKqP5nB8Ewfd5ntZD4410-KoiQA.',
  'SSOLoginState': '1500622489',
  'SUB': '_2A250dd7IDeRhGeBP7VIU8SvMwzuIHXVXmeKArDV6PUJbkdBeLUjYkW1aF6kNOoSPStwmFLiN5CexFzx-Fw..',
  'SUHB': '0HTR7VKgia9Ofs',
  '_T_WM': 'da0d59fda1d5a21bb686513ce698bdf0'},
 {'SCF': 'AjVR-bSS3zcXuhqKdaZyLdPYhKu2IAU8v5G_SxbuIJRMGMe0zDzof5Fqz7BjpNCgPa3WmIR3gre6PWmt7IOWkJQ.',
  'SSOLoginState': '1500622613',
  'SUB': '_2A250dd9FDeRhGeBP7lES8CzPwj2IHXVXmeENrDV6PUJbkdBeLXLYkW13QRQH_xNaooogA2zPTxFFh7n_WA..',
  'SUHB': '0WGsRY2amRC2hx',
  '_T_WM': '92c64708af2177273776658774868fb9'},
 {'SCF': 'AgfabZOuXSrK6Ace5s7Wz12DGudOp-_ztNGi43PTe9wwQmcCdeKVfuzo4TiCBiORvtzfF3NJraoZpcHYse17Meo.',
  'SSOLoginState': '1500639359',
  'SUB': '_2A250dYAvDeRhGeBP7lES8CfFwz6IHXVXmSBnrDV6PUJbkdBeLXehkW2HlfBdCWY4ZeEXJCR828JJZijPyA..',
  'SUHB': '0jBIVPEW2FRPQ1',
  '_T_WM': '0ec3a3277b29e6f81816bc39ef39e4cc'},
 {'SCF': 'As8Xv2TG8DrGG9Hv6abR4oBufDHWl5heiwVAHRFy--nUQ7ENc2dqXuIRGPubpHdWhdmp3zW6uF1VrzsgYTvzGdk.',
  'SSOLoginState': '1500639547',
  'SUB': '_2A250dYFrDeRhGeBP7lYW8i_PzTuIHXVXmS8jrDV6PUJbkdBeLXPbkW0jdVR2t5QpnIc6T7ldbR8NC3sNbA..',
  'SUHB': '0k1Cj7PCtbxRZg',
  '_T_WM': '5ffb24f36ff57bfc70a081d8015a2aaa'},
 {'SCF': 'Akg2fDllBfNcakqH5dZ9nA3WseZMh6G6wAy1R58rpxZDyxiok1lzkFD3K29BGv2_1SQhw64Z-Qb_jlGOwutAk5Q.',
  'SSOLoginState': '1500639626',
  'SUB': '_2A250dYHaDeRhGeBP7VIU8SjMyDuIHXVXmS-SrDV6PUJbkdBeLRTTkW1lj6Nsai55zzi4BhQaO1F1HHLq8g..',
  'SUHB': '0C1CjY1FQh_Tby',
  '_T_WM': '56e439193a7e34937f9555148d92b107'},
 {'SCF': 'AmtI_hInmG8if4BKb69fl35UPj1zpZ8tctGYFxvXyyDhj1DZhBeji0I7GpQjo223Wn6E2TPUY-A3wPndsmEl1fk.',
  'SSOLoginState': '1500639717',
  'SUB': '_2A250dYG1DeRhGeBP7VIU8SnMyDmIHXVXmS_9rDV6PUJbkdBeLXTTkW1DxyoVh5ABH_NiO0oxOS4Xcu8nzg..',
  'SUHB': '0WGcRY1TuRC2hz',
  '_T_WM': 'f8e291f082bc3d4669d31176470b89cf'},
 {'SCF': 'AjtdA6aSJyXdQXFKKL2dLCClb7hjLe1HakaA2Ul995ivVcNw3gh0fHSDhiKLBglWoLHXKP9SgC0U_T8WcC9deL4.',
  'SSOLoginState': '1500639780',
  'SUB': '_2A250dYJ0DeRhGeBP7VIU8SjPyDWIHXVXmS48rDV6PUJbkdBeLU_FkW1Lwgbe0fa3gd3JlJ0lO_W_VYcICA..',
  'SUHB': '0sqBp0Y1eONkDj',
  '_T_WM': 'e054adc4a3a801aa332500d12bd8d706'},
 {'SCF': 'AlNRpB-jXy4IXvv2lkN_tLTpaFnylG9bq3RRwfeM9hoSYsZ2VpeFNI7CuBOWBy1W2sk2k8qvGUo-1MKyN9d2N4Q.',
  'SSOLoginState': '1500639846',
  'SUB': '_2A250dYILDeRhGeBP7lYW8i7Jyj6IHXVXmS5DrDV6PUJbkdAKLRP4kW1shspgLNyiLZS9TC7p_uV6LEqidg..',
  'SUHB': '079jzh15I_7F18',
  '_T_WM': '12ec9191fd9a83e093ce61adee201a50'}]


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    if len(cookies) == 0 and READFROMFILE:
        pkl_file = open('data12.pkl','rb')
        data1 = pickle.load(pkl_file)
        pkl_file.close()
        cookies = data1
        print "Get Cookies From Local File!( Num:%d)" % len(cookies)
    return cookies


if MANUAL:
    cookies = manual_cookies
    print "Get Manual Cookies Finish!( Num:%d)" % len(cookies)
else:
    cookies = getCookies(myWeiBo)
    print "Get Cookies Finish!( Num:%d)" % len(cookies)
