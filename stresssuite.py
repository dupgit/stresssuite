#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#  Tools to manage the stress suites. Use at your own risks !
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

#  $Id: $

"""Program used to manage stress suites.

It contains a FileSystem Stress Suite (fss module).
Use --list option to have a list of all available suites and tests
To know more about how to use the program, use --help option.
"""

__author__ = "Olivier Delhomme <olivier.delhomme@free.fr>"
__date__ = "07.08.2009"
__version__ = "$Revision: 0.0.1 $"
__credits__ = "Thanks to Python makers"

import os
import sys
import getopt

import stress
import fss


class Collection:
    """A class to manage testsuites in the stresssuite program

    suite_list : a list of stress suites
    debug : a boolean saying wether we are in debug mode or not
    """

    suite_list = []
    debug = False

    def __init__(self):
        self.suite_list = []
        debug = False


    def add_suite(self, stress_suite):
        """Adds a stress suite to the collection"""
        self.suite_list.append(stress_suite)


    def find_suite_by_name(self, name):
        """Search for a stress suite named 'name'

        Returns the named stress suite or None
        """

        max = len(self.suite_list)
        for i in range(max):
            if self.suite_list[i].name == name:
                return self.suite_list[i]

        if self.debug == True:
            print("TestSuite with name '%s' was not found !" % name)

        return None


    def find_test_by_name(self, name):
        """Search for a test named 'name' across all testsuites

        If one or more test have the same name, only the first one is
        returned. None is return if no test has been found.
        """
        max = len(self.suite_list)
        for i in range(max):
            testlist = self.suite_list[i].testlist
            testmax = len(testlist)
            for j in range(testmax):
                if testlist[j].name == name:
                    return testlist[j]

        if self.debug == True:
            print("Test with name '%s' was not found !" % name)

        return None


    def run_one_stress_suite_vary(self, name, nb_times=1):
        """Runs one stress suite named 'name'

        Runs only one stress suite named 'name'. If nb_times is
        provided then a vary test is run on all tests of the test
        suite.
        """

        a_suite = self.find_suite_by_name(name)
        if a_suite != None:
            a_suite.run_test_suite_once_vary(nb_times)
        elif self.debug == True:
            print("Testsuite %s was not found !" % name)


    def run_all_stress_suites_vary(self, nb_times=1):
        """Runs all stress tests from all tests suites"""

        max = len(self.suite_list)
        for i in range(max):
            self.suite_list[i].run_test_suite_once_vary(nb_times)


    def list_all_suites(self):
        """Lists all suites and tests available in the collection"""

        max = len(self.suite_list)
        for i in range(max):
            self.suite_list[i].list_tests()


    def print_stats(self):
        """Prints all stats for all tests in all tests suites of this
        Collection"""

        max = len(self.suite_list)
        for i in range(max):
            self.suite_list[i].print_stats()


    def save_in_gnuplot(self):
        """Saves results in gnplot files"""
        max = len(self.suite_list)
        for i in range(max):
            self.suite_list[i].save_in_gnuplot()

    def set_debug_mode(self, debug):
        """Sets debug mode for everyone"""

        self.debug = debug
        max = len(self.suite_list)
        for i in range(max):
            self.suite_list[i].set_debug_mode(debug)

# End of Class Collection


class Options:
    """A class to manage command line options

    runs        : int, how many runs to do
    print_stats : boolean, says wether to print the stats or not
    debug       : boolean, says wether to go into debug mode or not
    list        : boolean, says wether to list the tests or not
    testname    : string, name of one test
    testsuite   : string, name of one test suite
    gnuplot     : boolean, says wether to save to gnuplot formated files or not
    """
    runs = 0
    print_stats = True
    debug = False
    list = False
    testname = ''
    testsuite = ''
    base_path = '/tmp'
    nb_threads = 1
    step = 2
    buffer_size = 512
    gnuplot = False

    def __init__(self):
        self.runs = 0
        self.print_stats = True
        self.debug = False
        self.list = False
        self.testname = ''
        self.testsuite = ''
        self.base_path = '/tmp'
        self.nb_threads = 1
        self.step = 2
        self.buffer_size = 512
        self.gnuplot = False

# Help message for main program
def usage():
  print("""
  NAME
      stress-suite

  SYNOPSIS
      stress-suite [OPTIONS]...

  DESCRIPTION
      Runs File related TestSuites

  OPTIONS
      When two exclusive options are specified (like -o and -m for
      instance), the selected one is the last specified on the command
      line.

      -h, --help
        Show this help

      -d, --debug
        More verbose

      -l, --list
        Show all tests with their contexts. When this option is used, it
        will prevail over -o or -m options

      -o, --once
        Runs all tests only once

      -n, --no-stats
        Does not print any stats at the end of the tests

      --gnuplot
        Export results (stats) to gnuplot formated files

      -m NUM, --multiple=NUM
        Tell to run the tests exactly NUM times

      --threads=NUM
        Tell the numbers of threads for one test (one by default)

      --buffer-size=NUM
        Tells the buffer size to use when creating files (512 by default)

      -s, --step=NUM
        Used in the vary function to step the algorithm (generally it
        is used to multiply the number of tests but it depends on the
        test itself to do what it wants with this value)

      -p PATH, --path=PATH
        Tells which path to use to run stresssuite program.
        '/tmp' by default

      --testname='NAME'
        Selects one test specificaly

      --testsuite='NAME'
        Selects one entire test suite specificaly. If --testname is
        specified at the same time then --testsuite option is ignored

    NAME must be a name as listed by -l or --list option

  EXAMPLE
      ./stresssuite.py -d -p /home/dup/tmp -m 10
      ./stresssuite.py -d -p /home/dup/tmp/stressfs --testsuite='Files'\
        --m 4 -s 10 --threads=5
      ./stresssuite.py --list

  """)
# End of function usage()

def transform_to_int(opt, arg):
    """transform 'arg' argument from the command line to an int where
    possible"""

    try :
        arg = int(arg)
    except:
        print("Error (%s), NUM must be an integer. Here '%s'" % \
              (str(opt), str(arg)))
        sys.exit(2)

    if arg > 0:
        return arg
    else:
        print("Error (%s), NUM must be positive. Here %d" % (str(opt), \
            arg))
        sys.exit(2)

# End of transform_to_int function


def parse_command_line(my_opts):
    short_options = "hlondm:p:s:"
    long_options = ["help", "list", "once", "no-stats", "debug",     \
                    "multiple=", 'testname=', 'testsuite=', 'path=', \
                    'threads=', 'step=', 'buffer-size=', 'gnuplot']

    # Read options and arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError, err:
        # print help information and exit with error :
        print("%s" % str(err))
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if my_opts.debug == True:
            print("opt = %s" % opt)
            print("arg = %s" % arg)

        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-l', '--list'):
            my_opts.list = True
        elif opt in ('-o', '--once'):
            my_opts.runs = 1
        elif opt in ('-n', '--no-stats'):
            my_opts.print_stats = False
        elif opt in ('-m', '--multiple'):
            my_opts.runs = transform_to_int(opt, arg)
        elif opt in ('-d', '--debug'):
            my_opts.debug = True
        elif opt in ('--testname'):
            my_opts.testname = arg
        elif opt in ('--testsuite'):
            my_opts.testsuite = arg
        elif opt in ('-p', '--path'):
            my_opts.base_path = arg
        elif opt in ('--threads'):
            my_opts.nb_threads = transform_to_int(opt, arg)
        elif opt in ('-s', '--step'):
            my_opts.step = transform_to_int(opt, arg)
        elif opt in ('--buffer-size'):
            my_opts.buffer_size = transform_to_int(opt, arg)
        elif opt in ('--gnuplot'):
            my_opts.gnuplot = True

    return my_opts
# End function parse_command_line()


def init_all_tests(collec, base_path, nb_threads, step, debug, buffer_size):
    """Inits the collection

    Add all tests_suites to the collection
    """

    # Add here your own stress suite !

    stressfs = fss.FileSystem_Tests(base_path, nb_threads, step, debug, \
                                    buffer_size)
    collec.add_suite(stressfs)

    return collec
# End of function init_all_tests()


def main():

    my_opts = Options()
    collec = Collection()

    # parsing options from the command line
    my_opts = parse_command_line(my_opts)

    collec = init_all_tests(collec, my_opts.base_path,        \
                            my_opts.nb_threads, my_opts.step, \
                            my_opts.debug, my_opts.buffer_size)

    if my_opts.debug == True:
       print("Debug mode is on")
       print("BasePath is '%s'" % my_opts.base_path)
       collec.set_debug_mode(True)

    if my_opts.list == True:
        collec.list_all_suites()
        sys.exit(0)

    # Running the tests

    if my_opts.testname != '':
        if my_opts.debug == True:
            print("Selected testname is : %s" % my_opts.testname)

        a_test = collec.find_test_by_name(my_opts.testname)

        if a_test != None:
            a_test.start_vary(my_opts.runs)

            if my_opts.print_stats == True:
                a_test.print_stats()

            if my_opts.gnuplot == True:
                a_test.save_in_gnuplot()

    elif my_opts.testsuite != '':
        if my_opts.debug == True:
            print("Selected testsuite is : %s" %my_opts.testsuite)

        a_testsuite = collec.find_suite_by_name(my_opts.testsuite)

        if a_testsuite != None:
            a_testsuite.run_test_suite_once_vary(my_opts.runs)

            if my_opts.print_stats == True:
                a_testsuite.print_stats()

            if my_opts.gnuplot == True:
                a_testsuite.save_in_gnuplot()

    else:
        collec.run_all_stress_suites_vary(my_opts.runs)

        # Printing results if stated
        if my_opts.print_stats == True:
            collec.print_stats()

        if my_opts.gnuplot == True:
            collec.save_in_gnuplot()

# End of main function


if __name__=="__main__" :
  main()
