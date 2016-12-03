Title: socketpool连接池
Date: 2016-2-27 03:43
Author: jmpews
Category: socketpool
Tags: socketpool,连接池
Slug: read-socketpool

项目链接地址: https://github.com/benoitc/socketpool

## 如何设计一个socket连接池
1. 首先连接池,必须具有一个queue来保存{连接}
2. 从连接池中get一个(ip,port)的连接，如果存在直接返回socket，如果不存在创建socket(创建socket可以对外提供一个接口factory,用户只需要继承接口并实现具体的方法)
3. 如果连接池满了直接关闭该socket

## pool.py 分析
```
# -*- coding: utf-8 -
#
# This file is part of socketpool.
# See the NOTICE for more information.

import contextlib
import sys
import time

from socketpool.util import load_backend

class MaxTriesError(Exception):
    pass

class MaxConnectionsError(Exception):
    pass

class ConnectionPool(object):
    """Pool of connections

    This is the main object to maintain connection. Connections are
    created using the factory instance passed as an option.

    Options:
    --------

    :attr factory: Instance of socketpool.Connector. See
        socketpool.conn.TcpConnector for an example
    :attr retry_max: int, default 3. Numbr of times to retry a
        connection before raising the MaxTriesError exception.
    :attr max_lifetime: int, default 600. time in ms we keep a
        connection in the pool
    :attr max_size: int, default 10. Maximum number of connections we
        keep in the pool.
    :attr options: Options to pass to the factory
    :attr reap_connection: boolean, default is true. If true a process
        will be launched in background to kill idle connections.
    :attr backend: string, default is thread. The socket pool can use
        different backend to handle process and connections. For now
        the backends "thread", "gevent" and "eventlet" are supported. But
        you can add your own backend if you want. For an example of backend,
        look at the module socketpool.gevent_backend.
    """

    def __init__(self, factory,
                 retry_max=3, retry_delay=.1,
                 timeout=-1, max_lifetime=600.,
                 max_size=10, options=None,
                 reap_connections=True, reap_delay=1,
                 backend="thread"):

        if isinstance(backend, str):
            self.backend_mod = load_backend(backend)
            self.backend = backend
        else:
            self.backend_mod = backend
            self.backend = str(getattr(backend, '__name__', backend))
        self.max_size = max_size
        self.pool = getattr(self.backend_mod, 'PriorityQueue')()
        self._free_conns = 0
        self.factory = factory
        self.retry_max = retry_max
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.max_lifetime = max_lifetime
        if options is None:
            self.options = {"backend_mod": self.backend_mod,
                            "pool": self}
        else:
            self.options = options
            self.options["backend_mod"] = self.backend_mod
            self.options["pool"] = self

        # bounded semaphore to make self._alive 'safe'
        self._sem = self.backend_mod.Semaphore(1)

        self._reaper = None
        # 循环定时调用murder_connections(),清除无效连接
        if reap_connections:
            self.reap_delay = reap_delay
            self.start_reaper()

    def too_old(self, conn):
        return time.time() - conn.get_lifetime() > self.max_lifetime
    # 遍历清除无效连接
    def murder_connections(self):
        current_pool_size = self.pool.qsize()
        if current_pool_size > 0:
            for priority, candidate in self.pool:
                current_pool_size -= 1
                if not self.too_old(candidate):
                    self.pool.put((priority, candidate))
                else:
                    self._reap_connection(candidate)
                if current_pool_size <= 0:
                    break
    # 设置这个循环检测是线程(thread)、协程(gevent)还是其他
    def start_reaper(self):
        self._reaper = self.backend_mod.ConnectionReaper(self,
                delay=self.reap_delay)
        self._reaper.ensure_started()

    def _reap_connection(self, conn):
        if conn.is_connected():
            conn.invalidate()

    @property
    def size(self):
        return self.pool.qsize()

    # 关闭连接池所有连接
    def release_all(self):
        if self.pool.qsize():
            for priority, conn in self.pool:
                self._reap_connection(conn)

    # 释放无效连接或加入连接池，在socket使用完毕后调用
    def release_connection(self, conn):
        if self._reaper is not None:
            self._reaper.ensure_started()

        with self._sem:
            if self.pool.qsize() < self.max_size:
                connected = conn.is_connected()
                if connected and not self.too_old(conn):
                    self.pool.put((conn.get_lifetime(), conn))
                else:
                    self._reap_connection(conn)
            else:
                self._reap_connection(conn)
    # 核心函数，从连接池子获取符合条件的连接，如果不存在，那么根据backend(thread,gevent等)生成一个连接
    def get(self, **options):
        options.update(self.options)

        found = None
        i = self.pool.qsize()
        tries = 0
        last_error = None

        unmatched = []

        # 遍历连接查找符合条件的连接
        while tries < self.retry_max:
            # first let's try to find a matching one from pool

            if self.pool.qsize():
                for priority, candidate in self.pool:
                    i -= 1
                    if self.too_old(candidate):
                        # let's drop it
                        self._reap_connection(candidate)
                        continue

                    matches = candidate.matches(**options)
                    if not matches:
                        # let's put it back
                        unmatched.append((priority, candidate))
                    else:
                        if candidate.is_connected():
                            found = candidate
                            break
                        else:
                            # conn is dead for some reason.
                            # reap it.
                            self._reap_connection(candidate)

                    if i <= 0:
                        break

            if unmatched:
                for candidate in unmatched:
                    self.pool.put(candidate)

            # we got one.. we use it
            if found is not None:
                return found

            # 不存在则创建连接
            try:
                new_item = self.factory(**options)
            except Exception as e:
                last_error = e
            else:
                # we should be connected now
                if new_item.is_connected():
                    with self._sem:
                        return new_item

            tries += 1
            self.backend_mod.sleep(self.retry_delay)

        if last_error is None:
            raise MaxTriesError()
        else:
            raise last_error

    # 奇淫技巧 方便with使用
    @contextlib.contextmanager
    def connection(self, **options):
        conn = self.get(**options)
        try:
            yield conn
            # what to do in case of success
        except Exception as e:
            conn.handle_exception(e)
        finally:
            # 检查该连接是否关闭，如果没有关闭假如连接池
            self.release_connection(conn)
```

## conn.py 分析
```
# -*- coding: utf-8 -
#
# This file is part of socketpool.
# See the NOTICE for more information.

import select
import socket
import time
import random

from socketpool import util

class Connector(object):
    def matches(self, **match_options):
        raise NotImplementedError()

    def is_connected(self):
        raise NotImplementedError()

    def handle_exception(self, exception):
        raise NotImplementedError()

    def get_lifetime(self):
        raise NotImplementedError()

    def invalidate(self):
        raise NotImplementedError()

# Connect类，连接不存在时，创建该类的实例
class TcpConnector(Connector):

    def __init__(self, host, port, backend_mod, pool=None):
        self._s = backend_mod.Socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((host, port))
        self.host = host
        self.port = port
        self.backend_mod = backend_mod
        self._connected = True
        # use a 'jiggle' value to make sure there is some
        # randomization to expiry, to avoid many conns expiring very
        # closely together.
        self._life = time.time() - random.randint(0, 10)
        self._pool = pool

    def __del__(self):
        self.release()

    # 在连接池中查找
    def matches(self, **match_options):
        target_host = match_options.get('host')
        target_port = match_options.get('port')
        return target_host == self.host and target_port == self.port

    def is_connected(self):
        if self._connected:
            return util.is_connected(self._s)
        return False

    def handle_exception(self, exception):
        print('got an exception')
        print(str(exception))

    def get_lifetime(self):
        return self._life

    # 关闭连接，需要接着release()
    def invalidate(self):
        self._s.close()
        self._connected = False
        self._life = -1

    def release(self):
        if self._pool is not None:
            if self._connected:
                self._pool.release_connection(self)
            else:
                self._pool = None

    def send(self, data):
        return self._s.send(data)

    def recv(self, size=1024):
        return self._s.recv(size)
```

## backend_gevent.py gevent模式分析
```
# -*- coding: utf-8 -
#
# This file is part of socketpool.
# See the NOTICE for more information.

import gevent
from gevent import select
from gevent import socket
from gevent import queue

from socketpool.pool import ConnectionPool

try:
    from gevent import lock
except ImportError:
    #gevent < 1.0b2
    from gevent import coros as lock


sleep = gevent.sleep
Semaphore = lock.BoundedSemaphore
Socket = socket.socket
Select = select.select

# 连接池：采用queue实现
class PriorityQueue(queue.PriorityQueue):

    def __next__(self):
        try:
            result = self.get(block=False)
        except queue.Empty:
            raise StopIteration
        return result
    next = __next__

# 循环清理连接池中的无效连接
class ConnectionReaper(gevent.Greenlet):

    running = False

    def __init__(self, pool, delay=150):
        self.pool = pool
        self.delay = delay
        gevent.Greenlet.__init__(self)

    def _run(self):
        self.running = True
        while True:
            gevent.sleep(self.delay)
            self.pool.murder_connections()

    def ensure_started(self):
        if not self.running or self.ready():
            self.start()

```
