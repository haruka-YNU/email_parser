# -*-coding:utf-8 -*-
from bs4 import BeautifulSoup
from dateutil.parser import parse
import email
import hashlib
import re
import os

class parser():
    def __init__(self, file_path = '', save_dir = './files'):
        self.file_path = file_path
        self.save_dir = save_dir
        self.msg, self.file_hash = self.__open_file()
        self.result = {}

    def __my_unicode(self, str, encoding):
        if encoding != None:
            return unicode(str, encoding, errors='ignore')
        else:
            return unicode(str, errors='ignore')

    def __open_file(self):
        with open(self.file_path, 'r') as fb:
            msg = email.message_from_file(fb)
            md5obj = hashlib.md5()
            md5obj.update(fb.read().encode())
            file_hash = md5obj.hexdigest()
            return msg, file_hash

    def __save_file(self, file_name, data):
        file_dir = os.path.join(self.save_dir, self.file_path.split('/')[-1])
        file_path = os.path.join(file_dir, file_name)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, 'wb') as f:
            f.write(data)

    def __format_str(self, str):
        no_enter = ''.join(str.splitlines())
        no_space = re.sub(' +', '', no_enter)
        no_tables = re.sub('\t', '', no_space)
        return no_tables

    def decode_head(self, head):
        decoded_header = ''
        if head:
            encode_header = email.Header.decode_header(head)
            for part in encode_header:
                if part[1] != None:
                    decoded_header += self.__format_str(self.__my_unicode(part[0],part[1]))
                else:
                    decoded_header += self.__my_unicode(part[0], 'utf-8')
        if decoded_header == '':
            return None
        else:
            return decoded_header

    def get_meta_date(self):
        #返回.eml文件名
        file_name = self.file_path.split('/')[-1]
        #返回.eml文件hash
        file_md5 = self.file_hash
        #抽出邮件id
        mail_id = self.msg['Message-ID']
        #抽出邮件日期
        if self.msg['date']:
            mail_date = parse(self.msg['date'][0:31]).strftime("%Y-%m-%d %H:%M:%S")
        else:
            mail_date = None
        #解码发信人并抽出
        mail_sender = self.decode_head(self.msg['from'])
        #解码标题并抽出
        mail_subject = self.decode_head(self.msg['Subject'])
        #解码收件人并抽出
        mail_receiver = self.decode_head(self.msg['to'])
        #解码CC并抽出
        mail_cc = self.decode_head(self.msg['cc'])
        #保存结果
        self.result['FileName'] = file_name
        self.result['FileHash'] = file_md5
        self.result['MailID'] = mail_id
        self.result['MailSubject'] = mail_subject
        self.result['MailSender'] = mail_sender
        self.result['MailDate'] = mail_date
        self.result['MailReceiver'] = mail_receiver
        self.result['MailCc'] = mail_cc
        return file_name, file_md5, mail_id, mail_subject, mail_sender, mail_date, mail_receiver, mail_cc

    def get_content(self):
        attachment_list = []
        attachment_type_list = []
        attachment_hash_list = []
        mail_text_article = ''
        mail_html_article = ''
        url_list = []
        for part in self.msg.walk():
            if not part.is_multipart():
                content_type = part.get_content_type()
                file_name = part.get_filename()
                charset = part.get_content_charset()
                #处理附件
                if file_name:
                    data = part.get_payload(decode=True)
                    md5obj = hashlib.md5()
                    md5obj.update(data)
                    attachment_hash_list.append(md5obj.hexdigest())
                    encoded_attachment_name = email.Header.Header(file_name)
                    attachment_name = self.decode_head(encoded_attachment_name).replace('/','-')
                    attachment_list.append(attachment_name)
                    if os.path.splitext(attachment_name)[1]:
                        attachment_type_list.append(os.path.splitext(attachment_name)[1])
                    self.__save_file(attachment_name, data)
                #处理txt文本
                elif 'plain' in content_type:
                    if charset == None or 'cp-850' or '7-bit':
                        mail_text_article = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    else:
                        mail_text_article = part.get_payload(decode=True).decode(charset, errors='ignore')
                #处理html
                elif 'html' in content_type:
                    html = part.get_payload(decode=True)
                    soup = BeautifulSoup(html, 'lxml')
                    mail_html_article = soup.get_text()
                    links = soup.find_all('a')
                    for tag in links:
                        link = tag.get('href', None)
                        url_list.append(link)
        #处理结果
        if len(attachment_list) == 0:
            attachment_list, attachment_type_list, attachment_hash_list = None, None, None
        if len(url_list) == 0:
            url_list = None
        #保存结果
        self.result['Attachment'] = attachment_list
        self.result['AttachmentType'] = attachment_type_list
        self.result['AttachmentHash'] = attachment_hash_list
        self.result['Urls'] = url_list
        if mail_text_article:
            self.result['MailArticle'] = mail_text_article
            return attachment_list, attachment_type_list, attachment_hash_list, url_list, mail_text_article
        else:
            self.result['MailArticle'] = mail_html_article
            return attachment_list, attachment_type_list, attachment_hash_list, url_list, mail_html_article

    def parse_email(self):
        self.get_meta_date()
        self.get_content()
        return self.result
