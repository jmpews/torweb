# coding:utf-8

from greenlet import greenlet

g3 = None
def test1():
   global g3
   print(12)
   gr2.switch()
   print(34)
   print(90)

def test2():
   g3 = greenlet()
   gr1.parent = g3.parent
   print(56)
   gr1.switch()
   print(78)

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()