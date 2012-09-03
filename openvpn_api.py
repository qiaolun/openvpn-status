#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import settings

def connect():
    tn = telnetlib.Telnet(settings.MANAGE_HOST, settings.MANAGE_PORT, 3)
 
    tn.read_until("ENTER PASSWORD:")
    tn.write(settings.MANAGE_PWD + "\n") # YAY HARDCODED PASSWORDS
  
    hurr = tn.read_some()
   
    if hurr[:7] != "SUCCESS":
        raise Exception("login failed")
    
    tn.read_until("info\r\n", 3)
    return tn

def get_status_1(tn):
    tn.write("status 2\n")
    status = tn.read_until("END", 2)
    return status

def send(tn, command):
    command = command.encode('ascii')
    tn.write("%s\n" % command)

def quit(tn):
    tn.write("quit\n")
    tn.close()

def parse_status(status):
    stati = status.split("\r\n")
    users_header = []
    users = []
    routes_header = []
    routes = []

    for i,line in enumerate(stati):
        if line.startswith("HEADER,CLIENT_LIST,"):
            users_header = line.split(",")[2:]
        elif line.startswith("HEADER,ROUTING_TABLE,"):
            routes_header = line.split(",")[2:]
        elif line.startswith("CLIENT_LIST,"):
            users.append(line.split(",")[1:])
        elif line.startswith("ROUTING_TABLE,"):
            routes.append(line.split(",")[1:])
        else:
            print 'skip: %s' % (line, )

    return {'users_header':users_header, 'users': users, 'routes_header': routes_header, 'routes': routes}

def get_status(tn):
    v = get_status_1(tn) 
    status = parse_status(v)
    return status

class OVPN(object):

    def __init__(self):
        pass

    def __enter__(self):
        self.tn = connect()
        
        return self.tn


    def __exit__(self, *exc_info):
        
        quit(self.tn)
        
        





if __name__ == '__main__':
    print 'test status'
    
    status = None
    with OVPN() as tn:
        status = get_status(tn)

    print status



