import uuid, os, re
from datetime import datetime
from .email import SendEmail

def sendEmail(receive_list, params, id):
    email_name = '又有一篇博文更新啦'
    # 邮件初始化
    email_sender = SendEmail(email_name=email_name)
    for receiver in receive_list:
        email_text = f"Hi,{receiver.split('@')[0]}:<br /><p style='white-space:pre'>{' '*4}{params['creator']}创作了一篇博文，《{params['title']}》，赶快来康康 bia~</p><a href='http://ncuteam.top/#/web/{id}'>去康康到底有啥好看(doge)</a><br /><p style='color:gray;font-size:.8em;white-space:pre'>{' '*60}--- 订阅信息，请勿直接回复</p>"
        # 发送邮件
        email_sender.send(receiver_list=[receiver, ], email_text=email_text, receiver_name=receiver.split('@')[0])
    email_sender.quit()

def emailMatch(email):
    return re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', email)

def getDirname():
    from blog import settings
    return settings.BASE_DIR

def getFiles(dir):
    return os.listdir(dir)

def getIntervalOfTwoStrTime(start, end, unit='days'):
    if isinstance(start, str):
        try:
            start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        except Exception:
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
    return getattr((end-start), unit)

def updateArticleFormat(article):
    return {
        'id': article['id'],
        'title': article['title'],
        'modify_time': f'{article["modify_time"].month}-{article["modify_time"].day}'
    }

def getNowTimeString(detail=False):
    now = datetime.now()
    if detail:
        return datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    return datetime.strftime(now, "%Y-%m-%d")

def isUnique(value, model):
    obj = model.objects.filter(user_name=value)
    if obj:
        return (True, obj)
    return (False, None)

def isUniqueInTag(value, model):
    obj = model.objects.filter(name=value).first()
    if obj:
        return (True, obj)
    return (False, None)

# 将返回的 OrderDict 类型转化为 Dict 类型，并可选择进行空值检测
def orderDictToDict(orderDict, validVal, checkList=[]):
    orderDict = dict(orderDict)
    flag = True
    if not orderDict:
        flag = False
    for key in orderDict.keys():
        if validVal and key not in checkList and not orderDict[key][0]:
            flag = False
        orderDict[key] = orderDict[key][0]

    return (orderDict, flag)


def generateUUID(filename): # 创建唯一的文件名
    id = str(uuid.uuid4())
    extend = os.path.splitext(filename)[1]
    return id + extend

def md5(user):
    import hashlib,time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()
