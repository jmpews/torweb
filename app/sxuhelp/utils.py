import re

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
