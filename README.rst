pwman
=====
Manage Nginx basic auth files.

Implements a subset of commands from ``htpasswd``.

Writes SSHA hashes.


Dependencies
------------
Python 2.7 and libzip headers.

Ubuntu::

    sudo apt-get install libzip-dev

`Virtualenv <http://www.virtualenv.org/en/latest/>`__ (optional)::

    sudo apt-get install python-virtualenv


Install
-------
For the current user (recommended)::

    pip install --user pwman
    # make sure you have $HOME/.local/bin on your PATH
    pwman --help

In a virtualenv::

    # create virtualenv
    mkdir -p ~/lib/python
    virtualenv ~/lib/python/pwman

    # install using virtualenv's pip (>= 0.8.2)
    ~/lib/python/pwman/bin/pip install pwman

    # add ~/bin to your PATH if you have not done so already
    cd ~/bin
    ln -s ~/lib/python/pwman/bin/pwman

    pwman --help

System-wide::

    sudo pip install pwman
    pwman --help

Tested on vanilla Ubuntu 12.04 Server.


Uninstall
---------
The virtual env::

    rm -r ~/bin/pwman ~/lib/python/pwman


Develop
-------
First timer::

    virtualenv .virtualenv
    source .virtualenv/bin/activate
    python setup.py develop

Next time::

    source .virtualenv/bin/activate


Testing
-------
This project uses `tox <http://tox.testrun.org/latest/index.html>`__.

Install tox::

    sudo apt-get install tox

Run::

    tox

This creates a virtualenvs for all supported versions (see `tox.ini`) and runs all tests.

- Coverage docs: http://nedbatchelder.com/code/coverage/

.. vim: set ft=rst :
