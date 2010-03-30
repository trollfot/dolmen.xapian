####################################################################
# Copyright (c) Kapil Thangavelu <kapil.foss@gmail.com. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
####################################################################

"""
$Id: $
"""

from zope import interface, schema

OP_ADDED = 'added'
OP_DELETED = 'deleted'
OP_MODIFED = 'modified'

# occassionally on low index timeouts its possible that object
# is added that hasn't yet been committed, so we get an unresolved
# error. allow for retrying operations which can't resolve a context
# one time.
OP_REQUEUE = object()

# For Testing purposes, using asynchronous indexing in a separate thread
# can be hard to debug, the following two settings can force synchronoug
# operation

# Utilizing this flag will have the indexer search synchronously
# for all changes
DEBUG_SYNC = False

# In order to utilize synchronous indexing the following,
# variable needs to be set to a xappy index connection.
DEBUG_SYNC_IDX = None

# This will turn on logging to the ore.xapian log channel,
# the logging for this channel needs to be configured by the application
DEBUG_LOG = True


class IIndexable(interface.Interface):
    """Marker interface for content to be indexed
    """


class IIndexer( interface.Interface ):
    """Indexes an object into the index
    """
    def index(connection):
        """Indexes an object into the connection
        """


class IIndexOperation(interface.Interface):

    oid = schema.ASCIILine(
        description=u"The identifier for the content")
    
    resolver_id = schema.ASCIILine(
        description=u"The resolver used to find the content")
    
    def process( connection ):
        """Processes an index operation
        """

class IDeleteOperation( IIndexOperation ): pass
class IModifyOperation( IIndexOperation ): pass
class IAddOperation( IIndexOperation ): pass        

class IOperationFactory( interface.Interface ):
    """
    creates operations, customizable by context, useful for creating classes
    of indexers across an entire class of objects (rdb, svn, fs, etc).
    """

    def add( ):
        """
        create an add operation
        """

    def modify( ):
        """
        create a modify operation
        """

    def delete( ):
        """
        create a delete operation
        """

class IResolver( interface.Interface ):
    """
    provides for getting an object identity and resolving an object by
    that identity. these identities are resolver specific, in order
    to resolve them from a document, we need to store the resolver name
    with the document in order to retrieve the appropriate resolver.
    """
    
    scheme = schema.TextLine(title=u"Resolver Scheme",
                             description=u"Name of Resolver Utility")

    def id( object ):
        """
        return the document id represented by the object
        """
        
    def resolve( document_id ):
        """
        return the object represented by a document id
        """

class IIndexConnection( interface.Interface ):
    """
    a xapian index connection
    """

class ISearchConnection( interface.Interface ):
    """
    a xapian search connection
    """

class IIndexSearch( interface.Interface ):
    """
    an access mediator to search connections, to allow for better reuse
    of search connections, avoid the need to carry constructor parameters
    when getting a search connection, and for the framework to provide
    for automatic reopening of connections when the index is modified.
    """

    def __call__( ):
        """
        return a search connection
        """
