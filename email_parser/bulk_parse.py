# -*-coding:utf-8 -*-
from email_parser import parser
from pymongo import MongoClient
import traceback
import sys
import os

client = MongoClient('mongodb://192.168.10.107:27017/email')
db = client.email
tests = db.bulktests

def batch_parse(email_path, save_path, error_path = '../error_log/'):
    count = 1
    for i in os.listdir(email_path):
        print count, i
        try:
            mail_par = parser(email_path + i, save_path)
            result = mail_par.parse_email()
            tests.insert_one(result)
        except:
            if not os.path.exists(error_path):
                os.makedirs(error_path)
            log = open(error_path + i + '.txt', 'w')
            log.write(i)
            traceback.print_exc(file=log)
            log.flush()
            log.close()
        count +=1

if __name__ == '__main__':
    batch_parse(sys.argv[1], sys.argv[2])
