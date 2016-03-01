#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hkk
# @Date:   2015-11-20 11:51:48
# @Last Modified by:   anchen
# @Last Modified time: 2016-02-29 14:26:38

import sqlite3
import sys,os
import re,time
class DBConnection(object):
    """docstring for DBConnection"""
    db_cursor = None
    db_connect = None
    CreateDatabase = [
            "CREATE TABLE wx_user_info ( \
              id INT NOT NULL PRIMARY KEY, \
              username VARCHAR DEFAULT NULL, \
              password VARCHAR DEFAULT NULL, \
              tuijianren TEXT DEFAULT NULL, \
              userpay VARCHAR DEFAULT NULL, \
              hardcode VARCHAR DEFAULT NULL, \
              istype INT DEFAULT 0, \
              ctime VARCHAR  DEFAULT NULL  \
            )",
            "CREATE TABLE agent_pay ( \
              id INT NOT NULL PRIMARY KEY, \
              agentname TEXT DEFAULT NULL,\
              agentpay VARCHAR DEFAULT NULL,\
              code VARCHAR DEFAULT NULL,\
              ctime VARCHAR DEFAULT NULL\
            )",
            "CREATE TABLE agent_info (\
              id  INT NOT NULL PRIMARY KEY,\
              agentname TEXT DEFAULT NULL,\
              agentpay VARCHAR DEFAULT NULL,\
              ctime VARCHAR DEFAULT NULL\
            )",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('1', 'test', 'testhkk', null, '10000501012015102331317179688.00', 'a7bea7416b06d84034ba6979ae0c098a', 2, '1445909054')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('2', 'dongshao', 'dongshao', null, '10000500012015102732165857200.01', null, 0, '1445922170')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('3', 'shuohua8023', 'shuohua8023', null, '10000500012015102732174472280.01', '1b2a716a420aa8a77db8a5743efb19ac', 0, '1445924436')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('4', 'feicheng114', 'feicheng114', null, '2015102714165838.00', '7a2d7bdae98c213f4632305f0904fe41', 1, '1445926127')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('5', 'lengyanzhuzi', 'lengyanzhuzi.', null, '2015102714284438.00', 'a84444c870a55a839204e0a12d03fdaf', 1, '1445926855')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('6', 'Poyanglou', 'Poyanglou.', null, '100005010120151028323417483938.00', '37625d5e4562d877d0ffeb59a0a3167e', 1, '1445995733')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('7', 'hjxfgc1', 'hjxfgc1', null, '10000500012015102832356507470.01', 'c94129beb1ae6ef1941cfdea3aa988b0', 0, '1446001060')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('8', 'hyx68680', 'hyx68680', '|123', '2015102818263488.00', '535b3edfeba3a2fb6c9add530f6e7f30', 1, '1446027501')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('9', '1231', '123', '|zeminseocom|sniffer-hkk|Jac|PK18899|tuilage006', null, null, 1, '1446702142')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('10', 'zeminseocom', 'zemin0623', null, null, null, 1, '1447226635')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('11', 'sniffer-hkks', '018019', null, null, null, 1, '1447311406')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('12', 'Jaca', '018019', null, null, null, 0, '1447314113')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('13', 'PK18899', '159599.', null, null, null, 2, '1447331605')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('14', 'tuilage006', 'tuilage006', null, null, null, 0, '1447898324')",
            "INSERT INTO wx_user_info (id, username, password, tuijianren,userpay,hardcode,istype,ctime) VALUES ('14', '181441322', '88887777', null, null, null, 1, '1448541302')"           
]
    def __init__(self, path):
        
        self.db_connect = sqlite3.connect(path, timeout=10)
        self.db_connect.text_factory = str
        if self.db_connect == None:
             print 'error'
        self.db_cursor = self.db_connect.cursor()
        try:
            self.db_connect.execute('SELECT COUNT(*) FROM wx_user_info')
        except sqlite3.Error:
            # .. If not set up, we set it up.
            try:
                self.create()
            except BaseException as e:
                print("Tried to set up the WechatCloud database schema, but failed: " + e.args[0])
        
    def create(self):
        try:
            for qry in self.CreateDatabase:
                self.db_cursor.execute(qry)
            self.db_connect.commit()
            print 'ok'
        except sqlite3.Error as e:
            raise BaseException("SQL error encountered when setting up database: " +  e.args[0])
    def check_user(self,username,password):
        qry = "SELECT password,\
                        istype\
               FROM wx_user_info WHERE username = ?"
        qvars = [username]
        try:
            self.db_cursor.execute(qry, qvars)
            db_str = self.db_cursor.fetchone()
            if db_str is not None:
                if password ==db_str[0]:
                    return db_str
                else:
                    return None
            return None         
        except sqlite3.Error as e:
            #self.np.error("SQL error encountered when retreiving scan instance:" + e.args[0])
            print e
    def regist_user(self,username,password,invite):
        qry = "SELECT   id,\
                        password,\
                        istype,\
                        tuijianren\
               FROM wx_user_info WHERE username = ?"
        qvars = [invite]
        try:
            self.db_cursor.execute(qry, qvars)
            db_str = self.db_cursor.fetchone()
            #print type(db_str)
            #print db_str
            if db_str is not None:
              count_qry = "SELECT count(*) FROM wx_user_info"
              self.db_cursor.execute(count_qry)
              total = self.db_cursor.fetchone()

              check_user_qry = "SELECT count(*) FROM wx_user_info WHERE username = ?"
              check_user =[username]
              self.db_cursor.execute(check_user_qry,check_user)
              res  = self.db_cursor.fetchone()
              #print res
              if res[0] == 1:
                return 'user'
              qry = "INSERT INTO wx_user_info \
                  (id,username, password, tuijianren,userpay,hardcode,istype,ctime)\
                  VALUES (?,?, ?, ?, ?, ?, ?, ?)"

              qvalss = [int(total[0])+1,username,password,invite,'','',0,str(time.time())[:10]]
              self.db_cursor.execute(qry, qvalss)
              #self.db_connect.commit() 

              qvarys = list()
              qry = "UPDATE wx_user_info SET "
              qry += " tuijianren = ?"
              #print type(db_str[2])
              if db_str[3] != None:
                qvarys.append('|'+db_str[3])
              else:
                qvarys.append(None)    
              qry += " WHERE username = ?"
              qvarys.append(invite)
              self.db_cursor.execute(qry, qvarys)
              self.db_connect.commit()
              return True 

            return False         
        except sqlite3.Error as e:
            #self.np.error("SQL error encountered when retreiving scan instance:" + e.args[0])
            print e            
    def __del__(self):
      self.db_connect.close()

            
