# -*- coding: utf-8 -*-
"""
Common functions that are used by other modules.

:Authors: Balwinder Sodhi
"""

import logging
import random
import string
from datetime import datetime as DT
from functools import wraps

from flask import (redirect, session, url_for, flash)
from models import db
from playhouse.shortcuts import *

TS_FORMAT = "%Y%m%d_%H%M%S"


def inject_user():
    if "user" in session:
        logging.info("Found user in session: {}".format(session["user"]))
        return dict(user=session["user"])
    else:
        logging.info("User not found in session!")
        return dict()


def auth_check(_func=None, *, roles=None):
    def decor_auth(func):
        @wraps(func)
        def wrapper_auth(*args, **kwargs):
            if "user" not in session:
                msg = "Illegal access to operation. Login required."
                logging.warning(msg)
                flash(msg)
                return redirect(url_for('login view'))

            user_role = session["user"]["role"]
            print("User role: {}".format(user_role))
            if roles and (user_role not in roles):
                msg = "You do not have required permissions to access."
                logging.warning(msg)
                flash(msg)
                return redirect(url_for('login view'))
            return func(*args, **kwargs)

        return wrapper_auth

    if _func is None:
        return decor_auth
    else:
        return decor_auth(_func)


def filter_date_using_format(date_time, given_format=None):
    if not given_format:
        given_format = TS_FORMAT
    if isinstance(date_time, str):
        date_time = DT.strptime(date_time, given_format)
    nat_dt = date_time.replace(tzinfo=None)
    to_fmt = '%d-%m-%Y@%I:%M:%S %p'
    return nat_dt.strftime(to_fmt)
    


def get_ts_str():
    return DT.now().strftime(TS_FORMAT)


def random_str(size=10):
    char_choices = string.ascii_uppercase + string.digits
    random_char_list = random.choices(char_choices, k=size)
    return ''.join(random_char_list)


def merge_form_to_model(mod, frm):
    """[summary]

    Arguments:
        mod {Model} -- peewee Model class instance
        frm {dict} -- dict from JSON object instance
    """
    # print("BEFORE: Form={0}. Model={1}".format(frm.to_dict(), model_to_dict(mod)))
    update_model_from_dict(mod, frm, ignore_unknown=True)
    # print("AFTER: Form={0}. Model={1}".format(frm.to_dict(), model_to_dict(mod)))


def db_connect():
    db.connect()


def db_close(http_resp):
    db.close()
    return http_resp
