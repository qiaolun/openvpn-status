OpenVPN Status
==============

A web OpenVPN management interface GUI **DEMO**

![Screenshot](//raw.github.com/qiaolun/openvpn-status/master/docs/screenshot_1.png)

Installation
------------

Setup OpenVPN management interface

    management 127.0.0.1 22222 /etc/openvpn/pwd.txt

Install dependencies
    
start application 

    ./app_status.py

or

    ./gevent_app_status.py

Dependencies
------------
* Python 2.6
* [Flask](http://flask.pocoo.org/docs/)
* [gevent](http://www.gevent.org/)


