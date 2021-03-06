#!/usr/bin/env python
# -*- encoding: utf8 -*-
#
#  Module that defines classes in order to do stress tests
#
#  (C) Copyright 2009 Olivier Delhomme
#  e-mail : olivier.delhomme@free.fr
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

""" module providing tools in order to do stress tests

Class TestSuite : a collection of tests
Class Test : one single test
"""

__author__ = "Olivier Delhomme <olivier.delhomme@free.fr>"
__date__ = "07.08.2009"
__version__ = "Revision: 0.0.1"
__credits__ = "Thanks to Python makers"

import os
import threading
import multiprocessing
import time


class TestSuite:
    """Class TestSuite : a collection of tests

    Provides methods and properties to manage a set of tests. These
    tests are grouped together in a testlist. You should group tests
    that are similar (as the filesystem tests for instance)

    properties :
        name         : name of the TestSuite itself
        description  : description of the TestSuite
        testlist     : list of available tests (fill with add_test method)
    """

    name = ''
    description = ''
    testlist = []

    def __init__(self, name, desc=''):
        """creates a newly create TestSuite

        name        : name of the TestSuite
        description : description of the TestSuite (optionnal)
        """
        self.name = name
        self.description = desc
        self.testlist = []


    def add_test(self, test):
        """add a test to the TestSuite

        test : A valid Test object
        It will be added to the testlist
        """
        self.testlist.append(test)


    def run_test_suite_once(self):
        """Runs all tests in the TestSuite

        Each test in the TestSuite is run only once
        """

        for a_test in self.testlist:
            a_test.start_once()


    def run_test_suite_once_vary(self, nb_times):
        """Runs all tests in the TestSuite

        nb_times : Tells how many times each test will be ran
        Each test of the TestSuite is run nb_times. Between each test,
        the vary function of the test is called in order to enable a
        change in the Test context. The whole TestSuite itself is run
        only once.
        """

        for a_test in self.testlist:
            a_test.start_vary(nb_times)


    def print_stats(self, stats):
        """Print running statistics

        Print statistics on the tests sessions that have already ran
        for each test of the TestSuite
        """
        print("Results for TestSuite '%s'" % self.name)

        for a_test in self.testlist:
            a_test.print_stats(stats)


    def save_in_gnuplot(self, path, stats):
        """Saving things to gnuplot files

        """

        for a_test in self.testlist:
            a_test.save_in_gnuplot(path, stats)


    def print_stats_by_name(self, name, stats):
        """Print running statistics

        Print statistics on test named 'name' from sessions that have
        already ran
        """
        print("Results for TestSuite '%s' and test '%s'" % \
             (self.name, name))

        a_test = self.find_test_by_name(name)

        if a_test != None:
            a_test.print_stats(stats)
        elif self.debug == True:
            print("Testname %s was not found !" % name)


    def set_debug_mode(self, debug):
        """Sets debug mode to all tests of the test suite"""

        print("Setting debug mode for all tests for testsuite '%s'" % \
              self.name)

        for a_test in self.testlist:
            print(" - test : %s" % a_test.name)
            a_test.debug = debug

        print("")


    def list_tests(self):
        """List all available tests

        List all available tests from the TestSuite. Prints name,
        description and init context if any of each test
        """

        print("Test list for TestSuite '%s' (%s) " %  \
             (self.name, self.description))

        i = 0
        for a_test in self.testlist:
            print("%03d : '%s' : %s " % (i, a_test.name, a_test.description))
            i += 1

        print("")


    def find_test_by_name(self, name):
        """Search for test 'name' in the test suite

        If two or more tests have the same name, the first one is
        returned. None is returned if no test is found.
        """

        for a_test in self.testlist:
            if a_test.name == name:
                return a_test

        return None


    def run_test_vary_by_name(self, name, nb_times=1):
        """Runs one test named 'name'

        Test may be ran more than once if nb_times is specified.
        """

        a_test = self.find_test_by_name(name)

        if a_test != None:
            a_test.start_vary(nb_times)
        elif self.debug == True:
            print("Testname %s was not found !" % name)

# End for Class TestSuite


class Test:
    """Class Test : one single 'test'

    Provides methods and properties for one single test. See fss.py
    example to know exactly how to use this class.
    init, final and vary func takes one parameter : context as a list of
    contexts for specific execution context (uppon to the test to define
    its  context).

    Properties   :
    name         : name for the test
    description  : description for the test
    context_list : execution context must be a list of contexts for
                   multiprocessed tests. Number of elements will
                   determine the number of processes to create
    init_func    : function being called at init time before test
                   execution.
    exec_func    : function being executed by the test. takes only one argument
                   as the context. Must return a tuple : (boolean, context)
    final_func   : function being called at the end of the test
                   execution
    vary_func    : function being used to vary the context between
                   succesive calls
    print_c_func : function that should return a string that resume the
                   context to a maximum of 37 charaters (context changes
                   only a little beetween succesive calls)
                   Takes 2 arguments : what and context
                   what is automatic and have 3 values : 'print', 'config' and
                   'vary' :
                    - print  : the function must return a 37 max char lenght
                               string
                    - config : the function must return a string with the name of
                               the variable beeing stepped
                    - vary   : the function must return an integer with the value
                               of the variable beeing stepped
    times        : list of list of execution times tuples
                   (cpu, real_time, context)
    process_times: list of execution time tuples for one process
    debug        : debug mode : on = True (verbose), off = False
    lock         : Lock() to avoid unwanted side effects with processes
    ok_to_go     : Event() to say to all processes "ready... heady...
                   steady.... GOOOoooo !!"
    step         : an integer to indicate to the vary function a step (it
                   can be used as the conceptor of the vary function
                   wants)
    result       : result for the test : True test succeded and can
                   continue again. False : the test failed and must stop
    """

    # default functions (init, test, final and vary) for the default
    # test
    def default_init(self, context):
        print("This is the default init")


    def default_test(self, context):
        print("This is the default test")


    def default_final(self, context):
        print("This is the default final")


    def default_vary(self, step, context):
        return None

    def default_print_c(self, what, context):
        return 'default context'

    def __init__(self, name, desc='', functions=(default_init, default_test, \
                 default_final, default_vary, default_print_c), \
                 context_list=None, step=2, debug=False):
        """Initialises one test

        Takes as first argument which is the name of the test, a second one
        which is the description for the test.
        'functions' is a tuple of functions that you must provide (in that
        order), an init function, a test function, a final function, a vary
        function and print_context function.
        context_list is a list of contexts to be used by the tests. The number
        of elements will determine the number of processes to execute. Step is a
        number that will be used to increment some variable in the test. At
        last you can use a boolean to tell if you want a verbose mode (debug
        mode - False by default )
        """

        init_func, exec_func, final_func, vary_func, print_c_func = functions

        self.name = name
        self.description = desc
        self.exec_func = exec_func
        self.init_func = init_func
        self.final_func = final_func
        self.vary_func = vary_func
        self.print_c_func = print_c_func
        self.context_list = context_list
        self.debug = debug
        self.times = []
        self.process_times = []
        self.lock = multiprocessing.Lock()
        self.ok_to_go = multiprocessing.Event()
        self.step = step
        self.result = True
        self.nb_process = 0

    def start_test(self, child_conn, i, vary, context):
        """Starts the test in a multiprosessed way

        Takes an index (i) that tells which context is used in the
        context_list and take one boolean argument, which tells wether
        to run the vary function or not (by default it will not) and the
        context itself.
        When the test is processed, init function is called with the
        context; then the test itself is called (and the time it took is
        recorded) ; then the final function is called (you may
        clean things or such here). If a vary test has been launched
        then the vary function is called at last.
        context is safe to edit (not self.context_list)
        """

        if self.debug == True:
            print("Now running test '%s' ; context : %s" %
                 (self.name, str(context)))
            print("start_test(%s, %d, %s, %s)" %
                 (str(child_conn), i, str(vary), str(context)))

        context = self.init_func(context)
        child_conn.send(1) # Sending that initialisation is done.

        # Wait for the event "start"
        self.ok_to_go.wait()

        if self.debug == True:
            print("Test started")

        begin_cpu = time.clock()
        begin_time = time.time()

        result, context = self.exec_func(context)

        end_time = time.time()
        end_cpu = time.clock()

        # This calculation is here to record the exact test context time
        a_time = end_cpu - begin_cpu, end_time - begin_time, context

        context = self.final_func(context)

        if (vary == True and result == True):
            context = self.vary_func(self.step, context)

        # Puting all results in a tuple and send it in the connection
        a_tuple = a_time, context, result

        child_conn.send(a_tuple)
        child_conn.close()

        if self.debug == True:
            print("Test ended")
            print("")


    def start_once(self, vary=False):
        """Starts the test only once

        Tests are launched each in process
        """
        if self.result == True:

            nb_process = len(self.context_list)
            process_list = []
            self.process_times = []
            self.nb_process = 0

            for i in xrange(nb_process):
                if self.debug == True:
                    print('Spawing a new process...')
                parent_conn, child_conn = multiprocessing.Pipe()
                a_process = multiprocessing.Process(target=self.start_test,    \
                                                    args=(child_conn, i, vary, \
                                                    self.context_list[i]))
                a_process.start()
                a_tuple = a_process, parent_conn
                process_list.append(a_tuple)
                if self.debug == True:
                    print('%s' % str(a_process))


            # Sending the event to really start
            # waiting that the last process finishes its init ...

            for process_context in process_list:
                (a_process, parent_conn) = process_context
                self.nb_process += parent_conn.recv()

            if self.debug == True:
                print('%d =? %d' % (self.nb_process, nb_process))

            self.ok_to_go.set()

            i = 0
            for process_context in process_list:
                (a_process, parent_conn) = process_context

                a_tuple = parent_conn.recv()
                (a_time, context, result) = a_tuple

                self.process_times.append(a_time)
                self.context_list[i] = context
                self.result = self.result and result
                i += 1

                a_process.join()

            # Every processes has joined and we have now the times in the
            # list process_times
            self.ok_to_go.clear()
            self.times.append(self.process_times)
            del self.process_times


    def start_vary(self, nb_times):
        """Start a vary test nb_times times"""

        for i in xrange(nb_times):

            if self.debug == True:
                print('Run number %d / %d :' % (i+1, nb_times))

            if self.result == True:
                if i == (nb_times - 1):
                    self.start_once(False)
                else:
                    self.start_once(True)
            else:
                return None


    def print_normal_stats(self):
        """Prints normal statistics for the running session"""

        nb_tests = len(self.times)
        if nb_tests > 0:
            avg_cpu = 0
            avg_real = 0
            print("Results for test '%s'" % self.name)
            print("%s;%s;%s;%s" % ('Tests'.center(8),  \
                  'CPU'.center(15), 'real time'.center(15), \
                  'context'.center(38)))
            nb_process = len(self.times[0])

            i = 0
            for times in self.times:
                i += 1
                j = 0
                for result in times:
                    j += 1
                    cpu_time, real_time, context = result
                    avg_cpu += cpu_time
                    avg_real += real_time
                    cpu_str = '%5.02f' % cpu_time
                    real_str = '%5.04f' % real_time
                    context_resumed = self.print_c_func('print', context)
                    print("%3d.%3d ; %s ; %s ; %s" %(i, j, \
                          cpu_str.rjust(13),          \
                          real_str.rjust(13),        \
                          str(context_resumed).rjust(37)))

            avg_cpu_str = '%5.04f' % (avg_cpu/(nb_tests * nb_process))
            avg_real_str = '%5.04f' % (avg_real/(nb_tests * nb_process))
            print("Averages : %s ; %s (over %d tests of %d processes)" %        \
                  (avg_cpu_str, avg_real_str, nb_tests, nb_process))
            print("")
        else:
            print("%s - No tests has been ran !" % self.name)


    def print_cumulative_stats(self):
        """Prints cumulative statistics for the running session"""

        nb_tests = len(self.times)
        if nb_tests > 0:
            print("Results for test '%s'" % self.name)
            print("%s;%s;%s;%s;%s" % ('Tests'.center(8),          \
                  'CPU'.center(13), 'real time'.center(13), \
                  'processes'.center(11), 'context'.center(31)))
            nb_process = len(self.times[0])

            i = 0
            for times in self.times:
                i += 1
                cpu_total = 0
                real_total = 0

                for result in times:
                    cpu_time, real_time, context = result
                    cpu_total += cpu_time
                    real_total += real_time

                cpu_str = '%5.04f' % (cpu_total)
                real_str = '%5.04f' % (real_total)
                context_resumed = str(self.print_c_func('vary', context))
                print("%s;%s ;%s ;%s;%s" % (str(i).center(8),                 \
                      cpu_str.rjust(12), real_str.rjust(12),                  \
                      str(nb_process).center(11), context_resumed.rjust(31)))

            print("")
        else: # here nb_tests <= 0
            print("%s - No tests has been ran !" % self.name)


    def print_stats(self, stats):
        """Prints statistics on the running sessions of the test

        Each running session is timed (cpu and real time). These times
        are saved along with the context used for the test (in a list
        of list). This method prints all thoses values.
        """

        if stats == 1:
            self.print_normal_stats()
        else:
            self.print_cumulative_stats()


    def save_in_gnuplot_normal(self, path):
        """Saves statistics on the running session in a gnuplot ready file in a
normal way."""

        if os.path.exists(path):
            file_name = '%s/%s.p' % (path, self.name)
        else:
            try:
                os.makedirs(path)
                file_name = '%s/%s.p' % (path, self.name)
            except:
                if self.debug == True:
                    print('Error while trying to make path %s' % path)
                return None

        try:
            gnuplot = open(file_name, 'w')
            gnuplot.write('set terminal png transparent nocrop enhanced small \
size 1280,960\n')

            nb_tests = len(self.times)
            if nb_tests > 0:
                nb_process = len(self.times[0])
                cpu_time, real_time, context = self.times[0][0]
                inverse = []

                gnuplot.write('set title "Results for test %s (%d processes)"\n' \
                               % (self.name, nb_process))
                gnuplot.write('set ylabel "time (in s)"\n')
                gnuplot.write('set xlabel "%s"\n' % \
                              self.print_c_func('config', context))
                process_str = 'plot \'-\' title "Process 0" with lines'

                for i in xrange(nb_process-1):
                    process_str += ', \'-\' title "Process ' + str(i+1) + \
                                  '" with lines'
                    inverse.append([])

                gnuplot.write(process_str + '\n')
                inverse.append([])

                for i in xrange(nb_tests):
                    nb_process = len(self.times[i])
                    self.process_times = self.times[i]
                    for j in xrange(nb_process):
                        cpu_time, real_time, context = self.process_times[j]
                        inverse[j].append(self.process_times[j])

                for j in xrange(nb_process):
                    a_process = inverse[j]
                    for i in xrange(nb_tests):
                        cpu_time, real_time, context = a_process[i]
                        gnuplot.write('%d %f\n' %                         \
                                     (self.print_c_func('vary', context), \
                                     real_time))
                    gnuplot.write('e\n')

                gnuplot.close()

            else:
                if self.debug == True:
                    print("%s - No tests has been ran !" % self.name)

                return None

        except:
            if self.debug == True:
                print('Something went wrong while trying to open %s file' %
                       file_name)

            return None

    # End of save_in_gnuplot_normal() function


    def save_in_gnuplot_cumulative(self, path):
        """Saves statistics on the running session in a gnuplot ready file in a
normal way."""

        if os.path.exists(path):
            file_name = '%s/%s.p' % (path, self.name)
        else:
            print('Error while trying to openning path %s' % path)
            return None

        try:
            gnuplot = open(file_name, 'a+')

            nb_tests = len(self.times)
            if nb_tests > 0:
                nb_process = len(self.times[0])
                cpu_time, real_time, context = self.times[0][0]
                inverse = []

                for times in self.times:
                    cpu_total = 0
                    real_total = 0
                    for result in times:
                        cpu_time, real_time, context = result
                        cpu_total += cpu_time
                        real_total += real_time

                    gnuplot.write('%d %f %f\n' %                          \
                                     (self.print_c_func('vary', context), \
                                     cpu_total, real_total))

                gnuplot.write('e\n')
                gnuplot.close()

            else:
                if self.debug == True:
                    print("%s - No tests has been ran !" % self.name)
                return None

        except:
            if self.debug == True:
                print('Something went wrong while trying to open %s file' %
                       file_name)
            return None

        # End of save_in_gnuplot_cumulative() function


    def save_in_gnuplot(self, path, stats):
        """Saves statistics on the running session in a gnuplot ready file

        Each running session is timed (cpu and real time). These times
        are saved along with the context used for the test (in a list
        of list). This method saves all thoses values into a gnuplot ready
        file
        """

        if stats == 1:
            self.save_in_gnuplot_normal(path)
        else:
            self.save_in_gnuplot_cumulative(path)



    name = ''                      # name for the test
    description = ''               # description for the test
    context_list = None            # execution context list
    init_func = default_init       # function being called at init time
                                   # before test execution
    exec_func = default_test       # function being executed by the test
    final_func = default_final     # function being called at the end of
                                   # the test execution
    vary_func = default_vary       # function being used to vary the
                                   # context between succesive calls
    print_c_func = default_print_c # function that must resume the
                                   # context into a maximum of 37
                                   # printable characters
    times = []                     # execution times tuples
                                   # (cpu, real_time, context)
    debug = False                  # debug mode on = True ; off = False
    process_times = []             # list of execution times for one
                                   # process
    lock = None                    # lock to manage a critical section
                                   # in the process
    ok_to_go = None                # A specific signal send to the
                                   # processes in order that they all
                                   # begin at the same time (more or
                                   # less)
    step = 2                       # A step for the vary function

# End for Class Test

