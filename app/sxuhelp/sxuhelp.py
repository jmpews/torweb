# coding:utf-8
import tornado.web
from db.mysql_model.user import User
from custor.handlers.basehandler import BaseRequestHandler

from custor.utils import json_result, get_cleaned_query_data, get_cleaned_post_data

from custor.decorators import login_required

import re
import requests
import base64

class Student(object):
    def __init__(self, type, stu_id, password):
        self.type = type
        self.stu_id = stu_id
        self.password = password

    def set_cookie(self, cookie):
        self.cookie = cookie

class IndexHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        openid = get_cleaned_query_data(self, ['openid'])['openid']
        self.render('index.html', openid = openid)

class BindHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        response = requests.get('http://bkjw.sxu.edu.cn/_data/login.aspx',
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        viewstate = find_viewstate(response.text)
        self.set_cookie('ViewState', viewstate)

        sessionid = response.cookies.get('ASP.NET_SessionId')
        response = requests.get("http://bkjw.sxu.edu.cn/sys/ValidateCode.aspx",
                                    cookies = {'ASP.NET_SessionId': sessionid},
                                    headers = {'Referer': 'http://bkjw.sxu.edu.cn/_data/login.aspx', 'Host': 'bkjw.sxu.edu.cn'},
                                    #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        uri = ("data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8","ignore")))
        self.set_cookie('ASP.NET_SessionId', sessionid)
        self.render('bind.html', captcha = uri)
    def post(self, *args, **kwargs):
        stutype = get_cleaned_post_data(self,['stutype'])['stutype']
        if int(stutype) == 1:
            self.post_new(*args, **kwargs)
        else:
            self.post_old(*args, **kwargs)

    def post_old(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['stuid', 'passwd', 'stutype'])
        #stuid = '2012241004'
        stuid = post_data['stuid']
        #passwd = 'qwaszx'
        passwd = post_data['passwd']
        stutype = post_data['stutype']
        openid = get_cleaned_query_data(self, ['openid'])['openid']

        data = {
            'Login.Token1': stuid,
            'Login.Token2': passwd,
        }
        response = requests.post('http://myportal.sxu.edu.cn/userPasswordValidate.portal',
                                data = data,
                                headers = {'Host': 'myportal.sxu.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded'},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        if 'handleLoginSuccessed' not in response.text:
            self.write(json_result(1,'用户名密码验证失败'))
            return
        iPlanetDirectoryPro = response.cookies.get('iPlanetDirectoryPro')
        response = requests.get('http://stuach.sxu.edu.cn/student/caslogin.asp', allow_redirects = False,
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = {'iPlanetDirectoryPro': iPlanetDirectoryPro},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )

        ASPSESSIONIDACRRADAD = response.cookies.get('ASPSESSIONIDACRRADAD')
        response = requests.get('http://stuach.sxu.edu.cn/student/studentinfo.asp',
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = {'ASPSESSIONIDACRRADAD': ASPSESSIONIDACRRADAD},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        stuname, stumajor = find_stu_info_old(response.content.decode('gb2312','ignore'))
        temp_user = User.get_by_openid(openid)
        if temp_user:
            temp_user.openid = temp_user.openid + '_d'
            temp_user.save()
        User.new(stuid, stuname, stumajor, passwd, stutype, openid, 'test')
        self.write(json_result(0,{'stuid': stuid, 'stuname': stuname, 'stumajor': stumajor}))
        return

    def post_new(self, *args, **kwargs):
        #stuid = self.get_body_argument('stuid')
        #passwd = self.get_body_argument('passwd')
        post_data = get_cleaned_post_data(self, ['stuid', 'passwd', 'captcha', 'stutype'])
        captcha = post_data['captcha']
        #stuid = '201502401037'
        stuid = post_data['stuid']
        #passwd = '622307'
        passwd = post_data['passwd']
        stutype = post_data['stutype']
        openid = get_cleaned_query_data(self, ['openid'])['openid']
        passwd_encrpyt, captcha_encrpt = get_encrypt_code(stuid, passwd, captcha)
        cookies = {'ASP.NET_SessionId': self.get_cookie('ASP.NET_SessionId')}
        data = {
            '__VIEWSTATE': self.get_cookie('ViewState'),
            'pcInfo': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0Intel Mac OS X 10.115.0 (Macintosh) SN:NULL',
            'txt_asmcdefsddsd': stuid,
            # 密码密文
            'dsdsdsdsdxcxdfgfg': passwd_encrpyt,
            # 验证码
            'fgfggfdgtyuuyyuuckjg': captcha_encrpt,
            'Sel_Type': 'STU',
            'typeName': '学生'
        }

        response = requests.post('http://bkjw.sxu.edu.cn/_data/login.aspx',
                                 data = data,
                                 cookies = cookies,
                                 headers = {'Host': 'bkjw.sxu.edu.cn', 'Referer': 'http://bkjw.sxu.edu.cn/_data/login.aspx'},
                                 #proxies = {'http': 'http://127.0.0.1:8080'}
                             )
        if '帐号或密码不正确' in response.text:
            self.write(json_result(1,'账号或密码不正确'))
            return
        elif '验证码错误' in response.text:
            self.write(json_result(1,'验证码错误'))
            return
        elif '权限' not in response.text:
            self.write(json_result(1,'未知错误'))
            return

        response = requests.get('http://bkjw.sxu.edu.cn/xsxj/Stu_MyInfo_RPT.aspx',
                                cookies = cookies,
                                headers = {'Host': 'bkjw.sxu.edu.cn','Referer': 'http://bkjw.sxu.edu.cn/xsxj/Stu_MyInfo.aspx'},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                            )

        stuid, stuname, stumajor = get_stu_info(response.text)
        temp_user = User.get_by_openid(openid)
        if temp_user:
            temp_user.openid = temp_user.openid + '_d'
            temp_user.save()
        User.new(stuid, stuname, stumajor, passwd, stutype, openid, 'test')
        self.write(json_result(0,{'stuid': stuid, 'stuname': stuname, 'stumajor': stumajor}))
        return

class MySecondScoreHandler_Old(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        cookies = {'ASPSESSIONIDACRRADAD': self.get_login_cookie(self.current_user)}
        response = requests.get('http://stuach.sxu.edu.cn/student/achieve/sxwachievebrow.asp', allow_redirects = False,
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = cookies,
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        if 'errornotic' in response.text:
            self.render('error.html',error="您没有双学位")
            return
        scores = find_stu_score_old(response.content.decode('gb2312','ignore'))
        score = {
            'stuname': self.current_user.nickname,
            'stuid': self.current_user.username,
            'stumajor': self.current_user.major,
            'score': scores
        }
        self.render('myscore_old.html', score = score)

    def get_login_cookie(self, user):
        data = {
            'Login.Token1': user.username,
            'Login.Token2': user.passwd,
        }
        response = requests.post('http://myportal.sxu.edu.cn/userPasswordValidate.portal',
                                data = data,
                                headers = {'Host': 'myportal.sxu.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded'},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        if 'handleLoginSuccessed' not in response.text:
            self.write(json_result(1,'用户名密码验证失败'))
            return
        iPlanetDirectoryPro = response.cookies.get('iPlanetDirectoryPro')
        response = requests.get('http://stuach.sxu.edu.cn/student/caslogin.asp', allow_redirects = False,
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = {'iPlanetDirectoryPro': iPlanetDirectoryPro},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        return response.cookies.get('ASPSESSIONIDACRRADAD')

class MyScoreHandler_Old(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        cookies = {'ASPSESSIONIDACRRADAD': self.get_login_cookie(self.current_user)}
        response = requests.get('http://stuach.sxu.edu.cn/student/achieve/achievebrow.asp',
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = cookies,
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        scores = find_stu_score_old(response.content.decode('gb2312','ignore'))
        score = {
            'stuname': self.current_user.nickname,
            'stuid': self.current_user.username,
            'stumajor': self.current_user.major,
            'score': scores
        }
        self.render('myscore_old.html', score = score)

    def get_login_cookie(self, user):
        data = {
            'Login.Token1': user.username,
            'Login.Token2': user.passwd,
        }
        response = requests.post('http://myportal.sxu.edu.cn/userPasswordValidate.portal',
                                data = data,
                                headers = {'Host': 'myportal.sxu.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded'},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        if 'handleLoginSuccessed' not in response.text:
            self.write(json_result(1,'用户名密码验证失败'))
            return
        iPlanetDirectoryPro = response.cookies.get('iPlanetDirectoryPro')
        response = requests.get('http://stuach.sxu.edu.cn/student/caslogin.asp', allow_redirects = False,
                                headers = {'Host': 'stuach.sxu.edu.cn','User-Agent': ''},
                                cookies = {'iPlanetDirectoryPro': iPlanetDirectoryPro},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                                )
        return response.cookies.get('ASPSESSIONIDACRRADAD')


class MyScoreHandler_New(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        self.render('myscore_new.html')

    @login_required
    def post(self, *args, **kwargs):
        captcha = get_cleaned_post_data(self, ['captcha'])['captcha']
        if self.get_login_cookie(self.current_user, captcha):
            return
        if self.get_myscore(self.current_user):
            return
        return

    def get_login_cookie(self, user, captcha):
        # 验证码的cookie
        cookies = {'ASP.NET_SessionId': self.get_cookie('ASP.NET_SessionId')}
        passwd_encrpyt, captcha_encrpt = get_encrypt_code(user.username, user.passwd, captcha)
        data = {
            '__VIEWSTATE': self.get_cookie('ViewState'),
            'pcInfo': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0Intel Mac OS X 10.115.0 (Macintosh) SN:NULL',
            'txt_asmcdefsddsd': user.username,
            # 密码密文
            'dsdsdsdsdxcxdfgfg': passwd_encrpyt,
            # 验证码
            'fgfggfdgtyuuyyuuckjg': captcha_encrpt,
            'Sel_Type': 'STU',
            'typeName': '学生'
        }
        response = requests.post('http://bkjw.sxu.edu.cn/_data/login.aspx',
                                 data = data,
                                 cookies = cookies,
                                 headers = {'Host': 'bkjw.sxu.edu.cn', 'Referer': 'http://bkjw.sxu.edu.cn/_data/login.aspx'},
                                 proxies = {'http': 'http://127.0.0.1:8080'}
                             )
        if '权限' not in response.text:
            self.write(json_result(1,'验证码失败'))
            return 1
        return 0

    def get_myscore(self, user):
        # 登陆成功的cookie
        cookies = {'ASP.NET_SessionId': self.get_cookie('ASP.NET_SessionId')}
        response = requests.post('http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx',
                                data = {'SJ': 1, 'SelXNXQ': 0, 'zfx_flag': 0, 'zxf': 0, 'btn_search': '检索'},
                                cookies = cookies,
                                headers = {'Host': 'bkjw.sxu.edu.cn','Referer': 'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore.aspx'},
                                proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        stupoint = find_point(response.text)

        response = requests.get('http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_Drawimg.aspx?x=1&h=2&w=739&xnxq=20150&xn=2015&xq=0&rpt=0&rad=2&zfx=0',
                                cookies = cookies,
                                headers = {'Host': 'bkjw.sxu.edu.cn','Referer': 'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx',
                                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                                           'Accept': 'image/webp,image/*,*/*;q=0.8'},
                                proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        score_base64_img_semester_1 = ("data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8","ignore")))

        response = requests.get('http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_Drawimg.aspx?x=1&h=2&w=708&xnxq=20151&xn=2015&xq=1&rpt=0&rad=2&zfx=0',
                                cookies = cookies,
                                headers = {'Host': 'bkjw.sxu.edu.cn','Referer': 'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx',
                                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                                           'Accept': 'image/webp,image/*,*/*;q=0.8'},
                                #proxies = {'http': 'http://127.0.0.1:8080'}
                            )
        score_base64_img_semester_2 = ("data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8","ignore")))
        self.write(json_result(0, {
            'stuname': user.nickname,
            'stuid': user.username,
            'stupoint': stupoint,
            'stumajor': user.major,
            'score_base64_img_semester_1': score_base64_img_semester_1,
            'score_base64_img_semester_2': score_base64_img_semester_2
        }))
        return 0

class LoginHandler(BaseRequestHandler):

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,['username','password'])
        #try:
        #    post_data=get_cleaned_post_data(self,['username','password'])
        #except RequestArgumentError as e:
        #    self.write(json_result(e.code,e.msg))
        #    return
        user=User.auth(post_data['username'],post_data['password'])
        if user:
            self.set_secure_cookie('uuid',user.username)
            result=json_result(0,'login success!')
            self.redirect('/')
        else:
            result=json_result(-1,'login failed!')
            self.redirect('/login')
        # write as json
        #self.write(result)

def get_stu_info(content):
    pattern = re.compile(r"号</td><td width='133'>(.+?)<br></td>.+名</td><td colspan='2'>(.+?)<br></td>.+专业</td><td>(.+?)<br></td>")
    v = pattern.search(content)
    return v.group(1), v.group(2), v.group(3)

def find_stu_info_old(content):
    pattern = re.compile(r'姓\u3000\u3000名:[\s\S]+?<p align="left">(.+?)<br></p>[\s\S]+?专\u3000\u3000业:[\s\S]+?<p align="left">(.+?)<br></p>')
    v = pattern.search(content)
    return v.group(1), v.group(2)

def find_stu_score_old(content):
    tempa = []
    tempb = {}

    pattern = re.compile(r'<tr>[\s\S]+?<p align="center">(\d{4}-\d{4}-\d)</p>[\s\S]+?<p align="left">(.+?)<br>[\s\S]+?<p align="center"> \r\n          (?:\r\n          <font color="#996600"><b><font size="2">)?(\d+)[\s\S]+?<p align="center">([\s\S]*?)<br>')
    v = pattern.findall(content)
    for semester, course, score, credit in v:
        tempa.append([semester.strip(), course.strip(), score.strip(), '0' if credit.strip()=='' else credit.strip()])
    for score in tempa:
        if score[0] not in tempb.keys():
            tempb[score[0]]=[]
        tempb[score[0]].append(score)
    return tempb

def find_point(content):
    pattern = re.compile(r'<td align=left>平均学分绩点：(.+?)</td></tr><tr><td')
    v = pattern.search(content)
    return v.group(1)

def find_viewstate(content):
    pattern = re.compile(r'name="__VIEWSTATE" value="(.*?)"')
    v = pattern.search(content)
    return v.group(1)

def get_encrypt_code(stuid, passwd, captcha):

    # 密码和验证码的加密处理,参考js
    #var s=md5(document.all.txt_asmcdefsddsd.value+md5(obj.value).substring(0,30).toUpperCase()+'10108').substring(0,30).toUpperCase();
    #var s=md5(md5(obj.value.toUpperCase()).substring(0,30).toUpperCase()+'10108').substring(0,30).toUpperCase(); 
    import hashlib
    # 验证码处理
    m = hashlib.md5()
    m.update(captcha.encode().upper())
    m5 = m.hexdigest()
    m = hashlib.md5()
    m.update((m5[:30].upper() + '10108').encode())
    captcha_md5 = m.hexdigest()[:30].upper()
    #密码处理
    m = hashlib.md5()
    m.update(passwd.encode())
    m5 = m.hexdigest()
    m = hashlib.md5()
    m.update((stuid + m5[:30].upper() + '10108').encode())
    passwd_md5 = m.hexdigest()[:30].upper()
    return passwd_md5, captcha_md5

