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
import sys
import logging

import pkg_resources
import requests


__version__ = pkg_resources.require('pasteraw')[0].version

LOG_FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)
LOG = logging.getLogger(__name__)

ENDPOINT = 'http://pasteraw.com/api/v1'


def create_paste(content):
    r = requests.post(
        ENDPOINT + '/pastes', data={'content': content}, allow_redirects=False)

    if r.status_code == 302:
        return r.headers['Location']
    else:
        if r.text:
            LOG.exception(r.text)
        else:
            LOG.exception('Unable to read response from pasteraw.')
        sys.exit(1)


def main(args):
    LOG.debug('File-Count:', len(args.files))

    content = ''
    for line in fileinput.input(args.files):
        content += line

    LOG.debug('Content-Length:', len(content))

    print create_paste(content)

    sys.exit(0)


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
        print pkg_resources.require('pasteraw')[0]
        sys.exit()

    main(args)


if __name__ == '__main__':
    cli()
