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

# $Id: $

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
    """
    path, current_path, nb_tests = context

    first_err = -1

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
        return False
    else:
        return True

# End of make_directory_test function


def fss_tests_init(context):
    """Inits FileSystem tests

    Get its basepath before changing it to the test directory
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

    path, current_path, nb_tests = context

    nb_tests *= step

    context = path, current_path, nb_tests
    return context

# End of fss_tests_vary function


def clean_directory(context):
    """Removes all created files or directories (if any) from the
    FileSystem tests.
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
    """
    path, current_path, nb_tests = context

    first_err = -1

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
        return False
    else:
        return True

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
    """
    path, current_path, nb_tests, file_buffer, file_size = context

    first_err = -1

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
        return False
    else:
        return True

# End  of make_zero_filed_files_test function


def mzfft_init(context):
    """Inits all necessary stuff for the make_zero_filed_files_test

    context is a tuple containing :
    . a path where we want to run the test
    . the current path (I order to return correctly after the test)
    . a number that indicates how many files we want to create
    . a buffer of the proper size
    . a size for the file (in bytes)
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
    """A vary function for the make_zero_filed_files test"""

    path, current_path, nb_tests, file_buffer, file_size = context

    file_size *= step

    context = path, current_path, nb_tests, file_buffer, file_size
    return context

# End of mzfft_vary function


def mzfft_make_context_list(basepath, current_path, nb_tests, file_buffer, \
                            file_size, nb_threads):
    """Make a context list for the FileSystem test suite"""

    context_list = []
    for i in range(nb_threads):
        a_context = basepath + '/' + str(i), current_path, nb_tests, \
                    file_buffer, file_size
        context_list.append(a_context)

    return context_list

# End of mzfft_make_context_list function


def make_buffer(debug, buffer_size):
    """ Creates a buffer of buffer_size len"""

    a_buffer = b''

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
    """Make a context list for the FileSystem test suite"""

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
    how_many_directories = stress.Test('Directory creation',         \
      'Creates directories in one single directory', fss_tests_init, \
      make_directory_test, fss_tests_final, fss_tests_vary,          \
      dir_context, step, debug)

    stressfs.add_test(how_many_directories)

# Test 1 : Files Creation
    file_context = fss_make_context_list(basepath, '', 512, nb_threads)
    how_many_files = stress.Test('Files creation',              \
      'Creates files in one single directory', fss_tests_init,  \
      make_files_test, fss_tests_final, fss_tests_vary,         \
      file_context, step, debug)

    stressfs.add_test(how_many_files)

# Test 2 : Zero Filed Files Creation (file_size variation)
    a_buffer = make_buffer(debug, buffer_size)
    if len(a_buffer) > 0 :
        mzfft_context = mzfft_make_context_list(basepath, '', 512, a_buffer,   \
                                                512, nb_threads)
        mzfft = stress.Test('Zero filed files creation',
        'Creates zero filed files (sile size vary - buffer size is an option)',\
        mzfft_init, make_zero_filed_files_test, mzfft_final,                   \
        mzfft_vary_file_size, mzfft_context, step, debug)

        stressfs.add_test(mzfft)
    elif debug == True:
        print('Could not add Zero filed files creation test to TestSuite !')

    return stressfs

# End of FileSystem_Tests function
