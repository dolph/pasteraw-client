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


def create_paste(endpoint, content):
    r = requests.post(
        endpoint + '/pastes', data={'content': content}, allow_redirects=False)

    if r.status_code == 302:
        return r.headers['Location']
    if r.status_code == 413:
        return 'Maximum content length exceeded: %d bytes' % len(content)
    else:
        if r.text:
            LOG.exception(r.text)
        else:
            LOG.exception('Unable to read response from pasteraw.')
        raise SystemExit(1)


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

    print(create_paste(args.endpoint, content))

    raise SystemExit()


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
