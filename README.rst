===============
pasteraw-client
===============

Pipe `stdin` directly to a raw pastebin. Get a URL back. Go be productive.

Installation
------------

.. image:: https://img.shields.io/pypi/v/pasteraw.svg
   :target: https://pypi.python.org/pypi/pasteraw

From PyPi::

    $ pip install pasteraw

Command line usage
------------------

Given a file::

    $ cat somefile
    Lorem ipsum.

Pipe the file to `pasteraw` and get back a URL to a raw paste of that file::

    $ cat somefile | pasteraw
    http://cdn.pasteraw.com/9lvwkwgrgji5gbhjygxgaqcfx3hefpb

Do whatever you want with the URL. For example, open it in your web browser::

    $ open $(!!)

Python library usage
--------------------

To use `pasteraw.com <http://pasteraw.com/>`_::

    >>> c = pasteraw.Client()
    >>> url = c.create_paste('Lorem ipsum.')
    >>> print(url)
    http://cdn.pasteraw.com/9lvwkwgrgji5gbhjygxgaqcfx3hefpb

If you're using your own deployment of `pasteraw
<https://github.com/dolph/pasteraw>`_, pass your own API endpoint to the
client::

    >>> c = pasteraw.Client('http://pasteraw.example.com/api/v1')
