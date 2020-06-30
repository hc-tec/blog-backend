import smtplib
from email.mime.text import MIMEText
from email.header import Header
# email_sender = "2598772546@qq.com"
# email_pawd = "xcrfbkkswljzebca"
# email_name = "NCU-TEAM博客平台"   #input("邮件名称：")
# #email_text = input("邮件信息：")
# sender_name = input("发件人名称：")
# receiver_name = input("收件人名称：")
# receiver_list = []
# receivers = input("收信人邮件：(可输入多个)")
# while receivers != 'q':
#   receiver_list.append(receivers)
#   receivers = input()
# substitute_sender = email_sender

def getMessage(cls, email_text, receiver_name, encode="utf-8", format_="html"):
  # 封装 message
  message = MIMEText(email_text, format_, encode)
  # 发送者
  message['from'] = Header(cls.sender_name, encode)
  # 接受者
  message['to'] = Header(receiver_name, encode)
  # 此邮件名称
  message['Subject'] = Header(cls.email_name, encode)
  # 返回封装后的 message
  return message


class SendEmail():
  def __init__( self, email_name,
                email_sender="sunjitao@ncuteam.com.cn",
                email_pawd="Sun19961203",
                substitute_sender="sunjitao@ncuteam.com.cn",
                sender_name="NCU-TEAM博客平台"):
    self.substitute_sender = substitute_sender
    self.sender_name = sender_name
    self.email_name = email_name
    # 腾讯企业邮箱 提供第三方 SMTP 服务
    self.email_host = 'smtp.exmail.qq.com'
    #发送者的腾讯企业邮箱用户名
    self.email_sender = email_sender
    #发送者的 腾讯企业邮箱授权码
    self.email_pawd = email_pawd
    # 链接 腾讯企业邮箱 SMTP 服务
    #print("正在与第三方服务链接")
    self.smtpObj = smtplib.SMTP_SSL(self.email_host, 465)
    # 登录
    #print("链接成功，正在登录")
    self.smtpObj.login(self.email_sender, self.email_pawd)
    # 发送邮件
    #print("登录成功")
  def send(self, email_text, receiver_name, receiver_list):
    # 代发者
    substitute_sender = self.substitute_sender
    # 收信人列表
    self.receiver_list = receiver_list
    # 封装邮件信息
    message = getMessage(self, email_text, receiver_name)
    try:
      #print("执行邮件发送")
      self.smtpObj.sendmail(substitute_sender, receiver_list, message.as_string())
      #print("邮件发送成功。")
    except smtplib.SMTPException as e:
      print(e)
      #print("发送邮件失败")
  def quit(self):
    self.smtpObj.quit()
    #print("正常停止")

