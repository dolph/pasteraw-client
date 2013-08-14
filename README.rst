===============
pasteraw-client
===============

Pipe `stdin` directly to a raw pastebin. Get a URL back. Go be productive.

Installation
------------

From PyPi::

    $ pip install pasteraw

Usage
-----

Given a file::

    $ cat somefile
    Lorem ipsum.

Pipe the file to `pasteraw` and get back a URL to a raw paste of that file::

    $ cat somefile | pasteraw
    http://pasteraw.com/1ekg

Do whatever you want with the URL. For example, open it in your web browser::

    $ open $(!!)
