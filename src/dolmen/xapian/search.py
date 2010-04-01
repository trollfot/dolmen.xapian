# -*- coding: utf-8 -*-

import logging
import time
import xappy

from threading import local
from zope import interface
from dolmen.xapian.interfaces import IIndexSearch

log = logging.getLogger('dolmen.xapian')


class ConnectionHub(object):
    """Search connection storage and retrieval with automatic
    reconnections with connection aging, connections are all thread
    local.
    """
    # max time in seconds till we refresh a connection
    auto_refresh_delta = 20

    def __init__(self, index_path):
        self.store = local()
        self.modified = time.time()
        self.index_path = index_path

    def invalidate(self):
        self.modified = time.time()

    def get(self):
        conn = getattr(self.store, 'connection', None)

        now = time.time()
        if self.modified + self.auto_refresh_delta < now:
            self.modified = now

        if conn is None:
            self.store.connection = conn = xappy.SearchConnection(
                self.index_path)
            self.store.opened = now

        opened = getattr(self.store, 'opened')

        if opened < self.modified:
            log.warn("Reopening Connection")
            conn.reopen()
            self.store.opened = now

        return conn


class IndexSearch(object):
    """A base implementation of an IIndexSearch.
    Calling an instance of this class will return a valid
    search connection.
    """
    interface.implements(IIndexSearch)

    def __init__(self, index_path):
        self._index_path = index_path
        self.hub = ConnectionHub(index_path)

    def __call__(self):
        return self.hub.get()

    def invalidate(self):
        self.hub.invalidate()
