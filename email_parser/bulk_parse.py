# -*-coding:utf-8 -*-
from email_parser.email_parser import parser
from pymongo import MongoClient
import traceback
import os

client = MongoClient('mongodb://127.0.0.1:27017/email')
db = client.email
tests = db.bulktests

def batch_parse():
    count = 1
    for i in os.listdir('../../samples/samples'):
        print count, i
        try:
            mail_par = parser('../../samples/samples/' + i, '../../files/')
            result = mail_par.parse_email()
            tests.insert_one(result)
        except:
            if not os.path.exists('../error_log/'):
                os.makedirs('../error_log/')
            log = open('../error_log/' + i + '.txt', 'w')
            log.write(i)
            traceback.print_exc(file=log)
            log.flush()
            log.close()
        count +=1

if __name__ == '__main__':
    batch_parse()
