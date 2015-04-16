# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute, implements, classImplements

class IEmailSender(Interface):
    def send():
        pass


