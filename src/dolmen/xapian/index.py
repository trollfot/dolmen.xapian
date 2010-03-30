# -*- coding: utf-8 -*-

import xappy
import grokcore.component as grok

from zope import schema
from zope.interface import providedBy
from dolmen.xapian.interfaces import IIndexer, IIndexable


class DefaultContentIndexer(grok.Adapter):
    """This is the default implementation an IIndexer.
    It can be subclassed in order to be modified.
    """
    grok.context(IIndexable)
    grok.provides(IIndexer)

    def document(self, connection):
        """Returns a xapian index document from the context.
        Introspecting the connection provides the relevant fields available.
        """
        doc = xappy.UnprocessedDocument()
        for iface in providedBy(self.context):
            for field in schema.getFields(iface).values():
                if not isinstance(field, (schema.Text, schema.ASCII)):
                    continue
                value = field.query(self.context)
                if value is None:
                    value = u''
                if not isinstance(value, (str, unicode)):
                    value = unicode(value)
                doc.fields.append(xappy.Field(field.__name__, value))
        return doc
