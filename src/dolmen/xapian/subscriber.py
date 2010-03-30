# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.xapian.interfaces import IIndexable, IOperationFactory
from zope.security.proxy import removeSecurityProxy
from zope.lifecycleevent import (
    IObjectAddedEvent, IObjectModifiedEvent, IObjectRemovedEvent)


@grok.subscribe(IIndexable, IObjectAddedEvent)
def objectAdded(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)
    IOperationFactory(object).add()


@grok.subscribe(IIndexable, IObjectModifiedEvent)
def objectModified(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)    
    IOperationFactory(object).modify()


@grok.subscribe(IIndexable, IObjectRemovedEvent)
def objectDeleted(object, event):
    if removeSecurityProxy:
        object = removeSecurityProxy(object)    
    IOperationFactory(object).remove()
