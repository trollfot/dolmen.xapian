# -*- coding: utf-8 -*-

import dolmen.xapian
import unittest, shutil
import zope.component
import transaction
import interfaces

from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope import interface, component
from zope.component.testlayer import ZCMLFileLayer
from zope.component.eventtesting import setUp as EventSetup


class DolmenXapianLayer(ZCMLFileLayer):
    def setUp(self):
        ZCMLFileLayer.setUp(self)
        EventSetup()

    def tearDown(self):
        shutil.rmtree('/tmp/tmp.idx')


def test_suite():
    """Testing suite of the package.
    """
    globs = dict(
        implements=interface.implements,
        component=component,
        transaction=transaction,
        interfaces=interfaces)

    readme = DocFileSuite(
        'README.txt', globs=globs,
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
    readme.layer = DolmenXapianLayer(dolmen.xapian)
    suite = unittest.TestSuite()
    suite.addTest(readme)
    return suite

