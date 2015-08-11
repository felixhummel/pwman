pwman
=====
Simple manager for nginx basic auth files. Think htpasswd (but not quite) as lib. Writes SSHA hashes.

Dependencies
------------
Python 2.7 and libzip headers.

Ubuntu::

    sudo apt-get install libzip-dev

`Virtualenv <http://www.virtualenv.org/en/latest/>`__ (optional)::

    sudo apt-get install python-virtualenv

Install
-------
In a virtualenv (recommended)::

    # go where pwman should live
    mkdir -p ~/lib/python/pwman
    cd ~/lib/python/pwman

    # create virtualenv
    virtualenv .

    # install using virtualenv's pip (>= 0.8.2)
    ./bin/pip install https://github.com/felixhummel/pwman/archive/1.0.0.zip

    # add ~/bin to your PATH if you have not done so already
    cd ~/bin
    ln -s ~/lib/python/pwman/bin/pwman

    # use
    pwman --help

Globally::

    sudo pip install https://github.com/felixhummel/pwman/archive/1.0.0.zip
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

