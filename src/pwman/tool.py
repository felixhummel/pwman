#!/usr/bin/python
"""Manage htpasswd files for basic auth.

Usage:
    pwman [-c] <filename> <username> [<comment>]
    pwman -D <filename> <username>
    pwman -b [-c] [-D] <filename> <username> <password> [<comment>]
    pwman -p <username> <password>

Options:
  -h --help     Show this screen.
  --version     Show version.
  -c            Create a new htpasswd file, overwriting any existing file.
  -b            Use the password from the command line rather than prompting for it.
  -D            Remove the given user from the password file.
  -p            Print a hash for given user
"""
# TODO http://pythonpaste.org/scripttest/modules/scripttest.html maybe?
import pkg_resources
__version__ = pkg_resources.get_distribution("pwman").version

import getpass
import os
import sys
import random

from docopt import docopt

import pwman

def main():
    args = docopt(__doc__, version=__version__)

    batch = args['-b']
    delete_user = args['-D']
    create_file = args['-c']
    print_flag = args['-p']

    username = args['<username>']

    filename = args['<filename>']
    # check for file existence if neither create nor print given
    if not create_file and filename is not None and not os.path.exists(filename):
        sys.stderr.write('File does not exist: "{0}"\n'.format(filename))
        sys.stderr.write('You can create it with -c\n')
        sys.exit(1)

    password = args['<password>']
    if not any([batch, delete_user, print_flag]):
        password = getpass.getpass()

    if print_flag:
        print pwman.hash(username, password)
        sys.exit(0)

    passwdfile = pwman.AuthFile(filename, create=create_file)

    if delete_user:
        passwdfile.delete(username)
    else:
        nu = pwman.NewEntry(username, password, args['<comment>'])
        passwdfile.update(nu)

    passwdfile.save()

if __name__ == '__main__':
    main()
