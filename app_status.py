#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, exceptions, datetime, urllib, urlparse

import settings, openvpn_api

from functools import wraps

from flask import Flask, render_template, session, redirect, url_for, escape, request, g, jsonify, send_from_directory, flash
app = Flask(__name__)
app.config.from_object(settings)

from jinja2 import Markup

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    ret = '[not a timestamp]'
    ts = 0
    try:
        ts = int(value)
    except exceptions.ValueError:
        return ret

    return datetime.datetime.fromtimestamp(ts).strftime(format)

app.add_template_filter(datetimeformat)


def on_endpoint(endpoint, **kwargs):
   
    if endpoint == request.endpoint:
        if len(kwargs) > 0:
            for k,v in kwargs.iteritems():
                if request.values.get(k) != v:
                    return ' '
        return ' on '
    else:
        return ' '

app.jinja_env.globals['on_endpoint'] = on_endpoint
 

@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'USER' not in session:
            return redirect(url_for('login', next=request.url, why='no_user'))

        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():

    status = None
    with openvpn_api.OVPN() as tn:
        status = openvpn_api.get_status(tn)

    # print status

    return render_template('index.html', status=status)


@app.route('/login', methods=['POST', 'GET'])
def login():

    error = None
    if request.method == 'POST':
        
        if admin.check_login_user(app,
                    request.form['username'],
                    request.form['password']):
            
            next_url = request.args.get('next')
            if not next_url:
                next_url = url_for('index')

            return redirect(bgn.url_append(next_url,server=server))
        else:
            flash('Invalid username/password', 'error')

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    admin.logout_user()
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host=settings.LISTEN_HOST, port=settings.LISTEN_PORT)

