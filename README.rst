webthing-ws
===========

A  `WebThing <https://iot.mozilla.org/wot/>`_ WebSocket consumer and API client.

Installation
------------

The module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.

.. code:: bash

    $ pip3 install webthing-ws

On a Fedora-based system or on a CentOS/RHEL host with EPEL 8.

.. code:: bash

    $ sudo dnf -y install webthing-ws

Usage
-----

The file ``example.py`` contains an example about how to use this module.

Development
-----------

For development is recommended to use a ``venv``. Create it in the directory
after cloning the Git repository.

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ python3 setup.py develop

License
-------

``webthing-ws`` is licensed under MIT, for more details check LICENSE.
