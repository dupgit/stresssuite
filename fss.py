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

"""fss stands for FileSystemStress

Collection of tools and functions to stress your filesystem and
test its limits. Use at your own risks
"""

__author__ = "Olivier Delhomme <olivier.delhomme@free.fr>"
__date__ = "07.08.2009"
__version__ = "$Revision: 0.0.1 $"
__credits__ = "Thanks to Python makers"

import os
import stress

def make_directory_test(context):
    """Make directory test

    Creates a number of directories, in one single directory.
    context is a tuple containing :
    . a path where we want to run the test
    . the current path (I order to return correctly after the test)
    . a number that indicates how many directories we want to create
    This last number may be modified in order to reflect an error while
    executing the test

    >>> make_directory_test(('', '', 3))
    (False, ('', '', 3))


    >>> context = fss_tests_init(('/tmp/fss', '~/', 3))
    >>> make_directory_test(('/tmp/fss', '~/', 3))
    (True, ('/tmp/fss', '~/', 3))
    >>> clean_directory(('/tmp/fss', '', 3))
    ('/tmp/fss', '', 3)

    """
    path, current_path, nb_tests = context

    first_err = -1
    i = 0

    if path != '':
        for i in range(nb_tests):
            dir = path + '/' + str(i)
            try:
                os.mkdir(dir)
            except (OSError, IOError), err:
                if first_err == -1:
                    first_err = i

    if first_err != -1:
        print("Test could not perform to the end ! Test finished at %d"\
              % first_err)
        nb_tests = first_err
        context = path, current_path, nb_tests
        return (False, context)
    else:
        if i == 0:
            return (False, context)
        else:
            return (True, context)

# End of make_directory_test function


def fss_tests_init(context):
    """Inits FileSystem tests

    Get its basepath before changing it to the test directory

    >>> context = fss_tests_init(('/tmp/fss', '', 3))
    >>> path, current_path, nb_tests = context
    >>> path == '/tmp/fss' and nb_tests == 3 and current_path != ''
    True

    """

    path, current_path, nb_tests = context

    current_path = os.getcwd()
    try:
        os.chdir(path)
    except (OSError, IOError), err:
        try:
            os.makedirs(path)
            os.chdir(path)
        except OSError, err:
            print("%s" % str(err))
            context = '', current_path, nb_tests
            return context

    context = path, current_path, nb_tests
    return context

# End of fss_tests_init function


def fss_tests_final(context):
    """Finishes the FileSystem tests

    Removes all the directories contained in the test directory
    and returns to the original location
    """

    path, current_path, nb_tests = context

    clean_directory(context)

    if current_path != '':
        try:
            os.chdir(current_path)
        except OSError, err:
            print("%s" % str(err))
            return context

    context = path, current_path, nb_tests
    return context

# End of fss_tests_final function


def fss_tests_vary(step, context):
    """Function to vary nb_tests in context tuple

    >>> fss_tests_vary(2, ('/tmp/fss', '', 3))
    ('/tmp/fss', '', 6)
    """


    path, current_path, nb_tests = context

    nb_tests *= step

    context = path, current_path, nb_tests
    return context

# End of fss_tests_vary function


def fss_print_c(what, context):
    """Function to resume context to a string with mimimun length

    >>> fss_print_c('print', ('/tmp/fss', '', 3))
    'Tests : 3'

    >>> fss_print_c('config', ('/tmp/fss', '', 3))
    'Number of files/directories created'

    >>> fss_print_c('vary', ('/tmp/fss', '', 3))
    3
    """

    path, current_path, nb_tests = context

    if what == 'print':
        return 'Tests : ' + str(nb_tests)
    elif what == 'config':
        return 'Number of files/directories created'
    elif what == 'vary':
        return nb_tests

# End of fss_print_c function


def clean_directory(context):
    """Removes all created files or directories (if any) from the
    FileSystem tests.

    >>> clean_directory(('', '', 3))
    ('', '', 3)

    >>> clean_directory(('/tmp/fss', '', 3))
    ('/tmp/fss', '', 3)

    """

    path, current_path, nb_tests = context

    if path != '':
        for i in range(nb_tests):
            a_file = path + '/' + str(i)
            try:
                os.remove(a_file)
            except OSError, err:
                try:
                    os.rmdir(a_file)
                except OSError, err:
                    pass

    return context

# End of clean_directory function


def make_files_test(context):
    """Creates a huge number of files

    All files are created in one directory.
    context is a tuple containing :
    . a path where we want to run the test
    . the current path (I order to return correctly after the test)
    . a number that indicates how many files we want to create

    >>> make_files_test(('', '', 3))
    (False, ('', '', 3))

    ... fss_tests_init(('/tmp/fss', '~/', 3))
    >>> make_files_test(('/tmp/fss', '~/', 3))
    ... clean_directory(('/tmp/fss', '', 3))
    (True, ('/tmp/fss', '~/', 3))

    """
    path, current_path, nb_tests = context

    first_err = -1
    i = 0

    if path != '':
        for i in range(nb_tests):
            a_file_name = path + '/' + str(i)
            try:
                a_file = file(a_file_name, 'w', 0)
                a_file.close()
            except (OSError, IOError), err:
                if first_err == -1:
                    first_err = i

    if first_err != -1:
        print("Test could not perform to the end ! Test finished at %d"\
              % first_err)
        nb_tests = first_err
        context = path, current_path, nb_tests
        return (False, context)
    else:
        if (i == 0):
            return (False, context)
        else :
            return (True, context)

# End of make_files_test function


def write_to_the_file(a_file, file_buffer, file_size):
    """Writes file_buffer to a file

    Writes file_buffer to a file until it reaches file_size.
    If file_size is not a multiple of file_buffer's len then
    the files are truncated to the closest multiple.
    """

    buffer_size = len(file_buffer)

    if (file_size > 0 and buffer_size > 0):

        max = file_size / buffer_size

        for i in range(max):
            try:
                a_file.write(file_buffer)
            except:
                return False

        return True
    else:
        return False

# End of write_to_the_file function


def make_zero_filed_files_test(context):
    """Creates a defined number of zero filed files

    All files are created in one directory.
    context is a tuple containing :
    . a path where we want to run the test
    . the current path (I order to return correctly after the test)
    . a number that indicates how many files we want to create
    . a buffer of the proper size
    . a size for the file (in bytes)


    >>> context = mzfft_init(('/tmp/mzfft', '', 3, '    ', 512))
    >>> make_zero_filed_files_test(('/tmp/mzfft', '', 3, '    ', 512))
    ... clean_directory(('/tmp/mzfft', '', 3))
    (True, ('/tmp/mzfft', '', 3, '    ', 512))

    >>> make_zero_filed_files_test(('', '', 3, '    ', 512))
    (False, ('', '', 3, '    ', 512))

    """
    path, current_path, nb_tests, file_buffer, file_size = context

    first_err = -1
    i = 0
    result = True

    if path != '':
        for i in range(nb_tests):
            a_file_name = path + '/' + str(i)
            try:
                a_file = file(a_file_name, 'wb', 0)
                result = write_to_the_file(a_file, file_buffer, file_size)
            except:
                if first_err == -1:
                    first_err = i

            if result == False:
                if first_err == -1:
                    first_err = i

            try:
                a_file.close()
            except:
                if first_err == -1:
                    first_err = i

    if first_err != -1:
        print("Test could not perform to the end ! Test finished at %d"\
              % first_err)
        nb_tests = first_err
        context = path, current_path, nb_tests, file_buffer, file_size
        return (False, context)
    else:
        if i == 0:
            return (False, context)
        else:
            return (True, context)

# End  of make_zero_filed_files_test function


def mzfft_init(context):
    """Inits all necessary stuff for the make_zero_filed_files_test

    context is a tuple containing :
    . a path where we want to run the test
    . the current path (I order to return correctly after the test)
    . a number that indicates how many files we want to create
    . a buffer of the proper size
    . a size for the file (in bytes)

    >>> context = mzfft_init(('/tmp/mzfft', '', 3, '    ', 512))
    >>> path, current_path, nb_tests, file_buffer, file_size = context
    >>> path == '/tmp/mzfft' and nb_tests == 3
    True
    >>> file_buffer == '    ' and file_size == 512 and current_path != ''
    True

    """

    path, current_path, nb_tests, file_buffer, file_size = context

    current_path = os.getcwd()
    try:
        os.chdir(path)
    except (OSError, IOError), err:
        try:
            os.makedirs(path)
            os.chdir(path)
        except OSError, err:
            print("%s" % str(err))
            context = '', current_path, nb_tests, file_buffer, file_size
            return context

    context = path, current_path, nb_tests, file_buffer, file_size
    return context

# End of mzfft_init function


def mzfft_final(context):
    """Finishes make_zero_filed_files test

    Removes all the Files contained in the test directory
    and returns to the original location

    """

    path, current_path, nb_tests, file_buffer, file_size = context

    clean_context = path, current_path, nb_tests

    clean_directory(clean_context)

    if current_path != '':
        try:
            os.chdir(current_path)
        except OSError, err:
            print("%s" % str(err))
            return context

    context = path, current_path, nb_tests, file_buffer, file_size
    return context

# End of mzfft_final function


def mzfft_vary_file_size(step, context):
    """A vary function for the make_zero_filed_files test

    >>> mzfft_vary_file_size(2, ('/tmp/mzfft', '', 3, '    ', 512))
    ('/tmp/mzfft', '', 3, '    ', 1024)
    """

    path, current_path, nb_tests, file_buffer, file_size = context

    file_size *= step

    context = path, current_path, nb_tests, file_buffer, file_size
    return context

# End of mzfft_vary function


def mzfft_print_c(what, context):
    """Function to resume context to a string with mimimun length

    >>> mzfft_print_c('print', ('/tmp/mzfft', '', 3, '    ', 512))
    'T : 3 ; Bs : 4 ; Fs : 512'

    >>> mzfft_print_c('config', ('/tmp/mzfft', '', 3, '    ', 512))
    'File size (creating 3 files with a buffer of 4 bytes)'

    >>> mzfft_print_c('vary', ('/tmp/mzfft', '', 3, '    ', 512))
    512
    """

    path, current_path, nb_tests, file_buffer, file_size = context

    if what == 'print':
        return 'T : ' + str(nb_tests) + ' ; Bs : ' +  \
                str(len(file_buffer)) + ' ; Fs : ' + str(file_size)
    elif what == 'config':
        return 'File size (creating %d files with a buffer of %d bytes)' % \
               (nb_tests, len(file_buffer))
    elif what == 'vary':
        return file_size

# End of mzfft_print_c function


def mzfft_make_context_list(basepath, current_path, nb_tests, file_buffer, \
                            file_size, nb_threads):
    """Make a context list for the FileSystem test suite

    >>> mzfft_make_context_list('/tmp/mzfft', '', 3, '    ', 512, 2)
    [('/tmp/mzfft/0', '', 3, '    ', 512), ('/tmp/mzfft/1', '', 3, '    ', 512)]
    """

    context_list = []
    for i in range(nb_threads):
        a_context = basepath + '/' + str(i), current_path, nb_tests, \
                    file_buffer, file_size
        context_list.append(a_context)

    return context_list

# End of mzfft_make_context_list function


def make_buffer(debug, buffer_size):
    """ Creates a buffer of buffer_size len

    >>> make_buffer(False, 3)
    '   '

    >>> make_buffer(True, -1)
    ''

    >>> make_buffer(False, -1)
    ''
    """

    a_buffer = '' # b''

    try:
        for i in range(buffer_size):
            a_buffer += ' '

    except err:
        if debug == True:
            print('%s' % str(err))
        return ''

    return a_buffer

# End of make_buffer function


def fss_make_context_list(basepath, current_path, nb_times, nb_threads):
    """Make a context list for the FileSystem test suite

    >>> fss_make_context_list('/tmp/mzfft', '', 3, 2)
    [('/tmp/mzfft/0', '', 3), ('/tmp/mzfft/1', '', 3)]
    """

    context_list = []
    for i in range(nb_threads):
        a_context = basepath + '/' + str(i), current_path, nb_times
        context_list.append(a_context)

    return context_list

# End of fss_make_context_list


def FileSystem_Tests(basepath, nb_threads, step, debug, buffer_size):
    """Filesystem test collector

    Collects all defined tests for the FileSystem tests and returns it
    as a TestSuite
    """

    stressfs = stress.TestSuite('Files', 'Files related tests')

    # Test 0 : Directories Creation
    dir_context = fss_make_context_list(basepath, '', 100, nb_threads)

    dir_funcs = fss_tests_init, make_directory_test, fss_tests_final, \
                fss_tests_vary, fss_print_c

    how_many_directories = stress.Test('Directory creation',    \
      'Creates directories in one single directory', dir_funcs, \
      dir_context, step, debug)

    stressfs.add_test(how_many_directories)

    # Test 1 : Files Creation
    file_context = fss_make_context_list(basepath, '', 512, nb_threads)

    file_funcs = fss_tests_init, make_files_test, fss_tests_final, \
                 fss_tests_vary, fss_print_c

    how_many_files = stress.Test('Files creation',         \
      'Creates files in one single directory', file_funcs, \
      file_context, step, debug)

    stressfs.add_test(how_many_files)

    # Test 2 : Zero Filed Files Creation (file_size variation)
    a_buffer = make_buffer(debug, buffer_size)

    if len(a_buffer) > 0 :
        mzfft_context = mzfft_make_context_list(basepath, '', 2048, a_buffer,  \
                                                512, nb_threads)

        mzfft_funcs = mzfft_init, make_zero_filed_files_test, mzfft_final,     \
                      mzfft_vary_file_size, mzfft_print_c

        mzfft = stress.Test('Zero filed files creation',
        'Creates zero filed files (sile size vary - buffer size is an option)',\
        mzfft_funcs, mzfft_context, step, debug)

        stressfs.add_test(mzfft)

    elif debug == True:
        print('Could not add Zero filed files creation test to TestSuite !')

    if debug == True:
        print('%s' % str(stressfs))

    return stressfs

# End of FileSystem_Tests function
