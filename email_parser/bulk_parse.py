# -*-coding:utf-8 -*-
from email_parser import parser
from pymongo import MongoClient
import traceback
import sys
import os

client = MongoClient('mongodb://xiao-mongodb:27017/email')
db = client.email
collection_name = sys.argv[1].split('/')[3]+'.'+sys.argv[1].split('/')[4]
collection = db[collection_name]

def batch_parse(base_path, start, end, error_path = '../../error_log/'):
    continuous = range(int(start), int(end) + 1)
    count = 1
    for day in continuous:
        day = str(day)
        if len(day) < 2:
            day = '0' + str(day)
        email_path = os.path.join(base_path, day)
        for root, dirs, files in os.walk(email_path, topdown=False):
            for name in files:
                print count, name
                try:
                    mail_par = parser(os.path.join(root, name), save_dir = '/mnt/AttachFiles/')
                    result = mail_par.parse_email()
                    collection.insert_one(result)
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
    batch_parse(sys.argv[1], sys.argv[2], sys.argv[3])
	#sudo python /mnt/AttachFiles/2017/06 07 12
