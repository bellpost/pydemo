#!/usr/bin/python
# coding=utf-8
'''
@ctime: 2017年4月2日
@author: Bellpost
'''

import sys,os
import configparser

class dealconfig():
    def __init__(self,config_file_path):
        self.cf = configparser.ConfigParser()
        self.config_file_path = config_file_path
        self.cf.read(self.config_file_path)
        
    def get(self, field: object, key: object) -> object:
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result

        
    def set(self,filed, key, value):
        try:
            #self.cf.set("baseconf", "password", "123456")
            self.cf.set(filed, key, value)
            with open(self.config_file_path, "w+") as f:
                self.cf.write(f)
                f.flush()
                f.close()
        except:
            return False
        return True