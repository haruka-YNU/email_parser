# -*-coding:utf-8 -*-
from email_parser import parser
from pymongo import MongoClient
import traceback
import sys
import os

client = MongoClient('mongodb://127.0.0.1:27017/email')
db = client.email
tests = db.newtests

def batch_parse(email_path, save_path, error_path = '../../error_log/'):
    count = 1
    for root, dirs, files in os.walk(email_path, topdown=False):
        for name in files:
            print count, name
            try:
                mail_par = parser(os.path.join(root, name), save_path)
                result = mail_par.parse_email()
                tests.insert_one(result)
            except:
                if not os.path.exists(error_path):
                    os.makedirs(error_path)
                log = open(error_path + name + '.txt', 'w')
                log.write(name)
                traceback.print_exc(file=log)
                log.flush()
                log.close()
            count +=1

if __name__ == '__main__':
    batch_parse(sys.argv[1], sys.argv[2])
