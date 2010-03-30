import dolmen.xapian
import unittest, shutil
from zope.testing import doctest
import zope.component
from zope.testing.doctestunit import DocFileSuite

from zope import interface, component
from zope.component.testlayer import ZCMLFileLayer
from zope.component import testing
from zope.lifecycleevent import IObjectModifiedEvent
from zope.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.component.interfaces import IComponentLookup
from zope.component.testlayer import ZCMLFileLayer
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
from zope.interface import Interface
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager, SiteManagerAdapter
from zope.traversing.interfaces import ITraversable
from zope.component.eventtesting import setUp as EventSetup
import transaction

import interfaces, subscriber, operation


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

