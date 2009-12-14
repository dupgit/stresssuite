#!/usr/bin/env python
# -*- encoding: utf8 -*-
#
#  testscases for the StressSuite tools !
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

# This file is heavyly based on test_doc.py that you will found in the
# hachoir project thanks to Victor Stinner

import os
import sys
import doctest


def importModule(name):

    mod = __import__(name)
    components = name.split('.')

    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod
#


def testModule(name):

    print('--- Test module "%s"' % name)

    module = importModule(name)
    flags = doctest.REPORT_UDIFF
    failure, nb_test = doctest.testmod(module, optionflags=flags)

    print('--- End of test for module "%s" (%d passed and %d failed)' % \
         (name, nb_test, failure))

    if failure:
        sys.exit(1)
#


def main():

    cwd = os.path.dirname(__file__)
    sys.path.append(cwd)

    # Test some functions/classes
    testModule('fss')
    testModule('cpu_stress')
    testModule('stress')
    testModule('stresssuite')
#


if __name__ == "__main__":
    main()
