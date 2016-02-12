# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import fileinput
import logging

import pkg_resources
import requests


__version__ = pkg_resources.require('pasteraw')[0].version

LOG_FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)
LOG = logging.getLogger(__name__)

ENDPOINT = 'http://pasteraw.com/api/v1'


class Error(Exception):
    pass


class MaxLengthExceeded(Error):
    pass


class UnexpectedError(Error):
    pass


class Client(object):
    """A client library for pasteraw.

    To use pasteraw.com:

    >>> c = pasteraw.Client()
    >>> url = c.create_paste('Lorem ipsum.')
    >>> print(url)
    http://cdn.pasteraw.com/9lvwkwgrgji5gbhjygxgaqcfx3hefpb

    If you're using your own pasteraw deployment, pass your own API endpoint to
    the client:

    >>> c = pasteraw.Client('http://pasteraw.example.com/api/v1')

    """

    def __init__(self, endpoint=None):
        """Initialize a pasteraw client for the given endpoint (optional)."""
        self.endpoint = endpoint or ENDPOINT

    def create_paste(self, content):
        """Create a raw paste of the given content.

        Returns a URL to the paste, or raises a ``pasteraw.Error`` if something
        tragic happens instead.

        """
        r = requests.post(
            self.endpoint + '/pastes',
            data={'content': content},
            allow_redirects=False)

        if r.status_code == 302:
            return r.headers['Location']

        if r.status_code == 413:
            raise MaxLengthExceeded('%d bytes' % len(content))

        try:
            error_message = r.json()['error']
        except Exception:
            error_message = r.text

        raise UnexpectedError(error_message)


def main(args):
    LOG.debug('File-Count: %d', len(args.files))

    content = ''
    for line in fileinput.input(args.files):
        content += line

    content_length = len(content)
    LOG.debug('Content-Length: %d', content_length)
    if content_length > args.max_content_length:
        raise SystemExit(
            'Maximum content length (%d bytes) exceeded: %d bytes' % (
                args.max_content_length, content_length))

    client = Client(args.endpoint)

    try:
        url = client.create_paste(content)
        print(url)
    except MaxLengthExceeded as e:
        raise SystemExit('Maximum content length exceeded: %s' % e)


def cli():
    parser = argparse.ArgumentParser(
        prog='pasteraw',
        description='Pipe stdin or files to a raw pastebin.')
    parser.add_argument(
        'files', metavar='file', nargs='*',
        help='one or more file names')
    parser.add_argument(
        '--endpoint', default=ENDPOINT,
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--max-content-length', type=int, default=1048576,
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--debug', action='store_true',
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--version', action='store_true',
        help='show version number and exit')
    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)
    else:
        LOG.setLevel(logging.WARN)

    if args.version:
        print(pkg_resources.require('pasteraw')[0])
        raise SystemExit()

    main(args)


if __name__ == '__main__':
    cli()
