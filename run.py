# INFO: #
# ===================================

import sys, Queue
sys.path.append('Database_Module')
sys.path.append('HTTP_Front_Module')
sys.path.append('Memory_Module')
sys.path.append('Sync_Module')
from Database_Server import *
dbrun = run
from HTTP_Server_Com import *
httprun = run
from Memory_Server import *
memrun = run
from Sync_Server import *
syncrun = run

def do_work():
    func = q.get
    print 'starting {}'
    func()

def make_threads_and_queue(num, size):
    global q
    q = Queue.Queue(size)
    for i in xrange(num):
        t = Thread(target=do_work)
        t.deamon = True
        t.start()

def run():
    make_threads_and_queue(4,4)
    q.put(memrun)
    q.put(dbrun)
    q.put(httprun)
    q.put(syncrun)
'''
Exciting. Satisfying. Period.
.
'''
