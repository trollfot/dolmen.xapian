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

import Queue, threading, time

from logging import getLogger

from dolmen.xapian import interfaces

# we do async indexing with all indexing operations put into this queue
index_queue = Queue.Queue()

log = getLogger('dolmen.xapian')

# async queue processor
class QueueProcessor( object ):

    # Flush every _n_ changes to the db
    FLUSH_THRESHOLD = 20

    # Poll every _n_ seconds for changes
    POLL_TIMEOUT = 60

    indexer_running = False
    indexer_thread = None

    def __init__( self, connection ):
        self.connection = connection 

    def operations( self ):
        # iterator never ends, just sleeps when no results to process
        while self.indexer_running:
            # get an operation in blocking fashion
            try:
                op = index_queue.get(True, self.POLL_TIMEOUT )
            except Queue.Empty:
                yield None
            else:
                yield op                

    def __call__( self ):
        # number of documents indexed since last flush
        op_delta = 0

        # loop through queue iteration
        for op in self.operations():

            # on timeout the op is none
            if op is None:
                # if we indexed anything since the last flush, flush it now
                if op_delta:
                    if interfaces.DEBUG_LOG:
                        log.info("QueueProcessor:Timeout Flushing Index %s Pending Ops"%op_delta)
                    self.connection.flush()
                    op_delta = 0
                continue
            # process the operation
            if interfaces.DEBUG_LOG:
                log.debug("Processing Operation %r %r"%(op.document_id, op))
            try:
                result = op.process(self.connection)
            except:
                log.exception("Error During Operation %r %r" %
                              (op.document_id, op))
                continue
            
            op_delta += 1
            
            if op_delta % self.FLUSH_THRESHOLD == 0:
                if interfaces.DEBUG_LOG:
                    log.info("QueueProcessor:Delta Flushing Index %s Pending Ops"%op_delta)
                self.connection.flush()
                op_delta = 0
            
    @classmethod
    def start(klass, connection, silent=False):
        if klass.indexer_running:
            if silent:
                return
            raise SyntaxError("Indexer already running")

        if interfaces.DEBUG_LOG:
            log.info("Starting QueueProcessor Thread")
            log.debug("Index Fields Defined")
            
        klass.indexer_running = True
        indexer = klass(connection)
        klass.indexer_thread = threading.Thread(target=indexer)
        klass.indexer_thread.setDaemon(True)
        klass.indexer_thread.start()
        return indexer

    @classmethod
    def stop(klass):
        if not klass.indexer_running:
            return

        if interfaces.DEBUG_LOG:
            log.info("Stopping QueueProcessor Thread")
            
        klass.indexer_running = False
        klass.indexer_thread.join()

        if interfaces.DEBUG_LOG:
            log.info("Stopped QueueProcessor Thread")    
