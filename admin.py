
import os, binascii
from flask import session, request

import dao.admin

def check_login_user(server, username, password):

    check = dao.admin.check_login(server, username, password)

    # print repr(check)

    if not check:
        return False

    else:
        uid, privileged = check
        session['SERVER'] = server
        session['USER'] = username
        session['LOGOUT_KEY'] = binascii.hexlify(os.urandom(8))
        session['PRIVILEGED'] = privileged

        return True

def logout_user():
    k = request.args.get('k')
    # print session['LOGOUT_KEY'], k
    if k == session['LOGOUT_KEY'] :
        for x in ('SERVER', 'USER', 'LOGOUT_KEY', 'PRIVILEGED'):
            if x in session:
                session.pop(x)


