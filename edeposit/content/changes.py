# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute, implements, classImplements
from zope.component import adapts
from zope import schema
from functools import partial

class IChanges(Interface):
    """ item at list of changes should provide IApplicableChange interface """
    def getChanges(self):
        pass

class IApplicableChange(Interface):
    def apply(self):
        pass

class SetterApply(object):
    implements(IApplicableChange)
    
    def __init__(self, setter, newValue):
        self.setter = setter
        self.newValue = newValue
        
    def apply(self):
        self.setter(self.newValue)

class ObjSetterApply(SetterApply):
    def __init__(self, obj, attrName, value):
        super(ObjSetterApply,self).__init__(partial(setattr, obj, attrName), value)

