#!/usr/bin/env python

import multiprocessing

def this_is_a_test(yes, test):
    if yes == True:
        for i in range(30):
            test = test + 'a'
            print test
            sleep(1)
    else:
        for i in range(25):
            test = test + 'b'
            print test
            sleep(1)


pool = multiprocessing.Pool()
prout = 'ggg'
result1 = pool.apply_async(this_is_a_test, (True, prout))
result2 = pool.apply_async(this_is_a_test, (False, prout))
result1.get
result2.get
