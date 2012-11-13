pwman
=====
Simple manager for nginx basic auth files. Think htpasswd (but not quite) as lib. Writes SSHA hashes.

Dependencies
------------
Python 2.7 and libzip headers.

Ubuntu::

    sudo apt-get install libzip-dev

Install
-------
In a virtual env (recommended)::

    # go where pwman should live
    mkdir -p ~/lib/python/pwman
    cd ~/lib/python/pwman

    # create and activate virtualenv
    virtualenv .
    . bin/activate

    # install (requires pip >= 0.8.2)
    pip install git+https://github.com/felixhummel/pwman.git

    # deactivate virtualenv
    deactivate

    # add ~/bin to your PATH if you have not done so already
    cd ~/bin
    ln -s ~/lib/python/pwman/bin/pwman

    # use
    pwman --help

Globally::

    sudo pip install git+https://github.com/felixhummel/pwman.git
    pwman --help

Enjoy!

Uninstall
---------
The virtual env::

    rm -r ~/bin/pwman ~/lib/python/pwman

Develop
-------
First timer::

    virtualenv .
    . bin/activate
    python setup.py develop

Next time::

    . bin/activate

Testing
-------
This project uses `tox <http://tox.testrun.org/latest/index.html>`__.

Install tox::

    sudo apt-get install tox

Run::

    tox

This creates a virtualenv in `.tox/py27` and runs all tests.

- Coverage docs: http://nedbatchelder.com/code/coverage/

.. vim: set ft=rst :

