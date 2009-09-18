#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#  Tools to stress your filesystem. Use at your own risks !
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

"""cpu_stress tries to load cpu usage

Collection of tools and functions to stress your cpu(s)
"""

__author__ = "Olivier Delhomme <olivier.delhomme@free.fr>"
__date__ = "09.09.2009"
__version__ = "$Revision: 0.0.1 $"
__credits__ = "Thanks to Python makers"

import os
import base64
import stress


def cpu_encode_stress_test(context):
    """Does base64 and rot13 functions to stress the cpu(s)

    >>> cpu_encode_stress_test(('My string', 10))
    (True, ('My string', 10))

    >>> cpu_encode_stress_test(('My string', -10))
    (False, ('My string', -10))
    """

    a_string, nb_tests = context

    if nb_tests > 0:

        decoded = a_string

        for i in range(nb_tests):
            encoded = base64.b64encode(decoded)
            decoded = base64.b64decode(encoded)
            decoded = decoded.encode('rot13')

        context = a_string, nb_tests

        return (True, context)

    else:
        return (False, context)

# End of cpu_encode_stress_test() function


def cpu_est_init(context):
    """Inits cpu stress tests

    Nothing to do !

    >>> cpu_est_init(('My string', 10))
    ('My string', 10)
    """

    return context

# End of cpu_est_init() function


def cpu_est_final(context):
    """Finalize cpu stress tests

    Nothing to do !

    >>> cpu_est_final(('My string', 10))
    ('My string', 10)
    """

    return context

# End of cpu_est_final() function


def cpu_est_vary(step, context):
    """Vary function for cpu stress tests

    >>> cpu_est_vary(2, ('My string', 10))
    ('My string', 20)

    >>> cpu_est_vary(0, ('My string', 10))
    ('My string', 10)

    >>> cpu_est_vary(-1, ('My string', 10))
    ('My string', 10)

    >>> cpu_est_vary(2, ('My string', -10))
    ('My string', -10)

    >>> cpu_est_vary(-1, ('My string', -10))
    ('My string', -10)
    """

    a_string, nb_tests = context

    if nb_tests > 0 and step > 0:
        nb_tests *= step

    context = a_string, nb_tests

    return context

# End of cpu_est_vary() function


def cpu_est_print_c(what, context):
    """Function to resume context to a string with mimimun length

    >>> cpu_est_print_c('print', ('My string', 10))
    'Tests : 10'

    >>> cpu_est_print_c('config', ('My string', 10))
    'Number of runs'

    >>> cpu_est_print_c('vary', ('My string', 10))
    10

    >>> cpu_est_print_c('nawak', ('My string', 10))

    """

    a_string, nb_tests = context

    if what == 'print':
        return 'Tests : ' + str(nb_tests)
    elif what == 'config':
        return 'Number of runs'
    elif what == 'vary':
        return nb_tests

# End of cpu_est_print_c() function


def make_cpu_est_context_list(nb_threads, a_string, nb_tests):
    """Build context list for Cpu Encode Stress Test

    >>> make_cpu_est_context_list(2, 'My string', 10)
    [('My string', 10), ('My string', 10)]

    >>> make_cpu_est_context_list(-2, 'My string', 10)
    []

    """

    context_list = []

    for i in range(nb_threads):
        a_context = a_string, nb_tests
        context_list.append(a_context)

    return context_list

# End of make_cpu_est_context_list() function


def Cpu_Tests(nb_threads, step, debug):
    """Cpu test collector

    >>> a_testsuite = Cpu_Tests(2, 2, True)
    >>> a_testsuite.name == 'CPU'
    True
    >>> a_testsuite.description == 'Cpu related tests'
    True
    >>> a_testsuite.testlist[0].name == 'Cpu encode stress'
    True
    """

    stresscpu = stress.TestSuite('CPU', 'Cpu related tests')


    # Test 0 -- Cpu Encode Stress Test
    cpu_est_funcs = cpu_est_init, cpu_encode_stress_test, cpu_est_final, \
                    cpu_est_vary, cpu_est_print_c

    a_string = """This is an example string to be computed by the alogrithm in
    order to do some cpu cycles to load it a bit. It is not supposed to consume
    memory. If one sees a bug, please report to the author or current
    maintainer"""

    nb_tests = 20000L

    cpu_est_context_list = make_cpu_est_context_list(nb_threads, a_string, \
                                                     nb_tests)

    if (cpu_est_context_list != []):
        cest = stress.Test('Cpu encode stress', \
                           'Stress the cpu(s) with base64 and rot13 functions',\
                           cpu_est_funcs, cpu_est_context_list, step, debug)

        stresscpu.add_test(cest)


    return stresscpu

# End  of Cpu_Tests() function

