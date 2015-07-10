#!/usr/bin/env python

# splitmail.py - Simple tool to split your email
# 
# Copyright (C) 2015  Emanuele Di Giacomo <emanuele.digiacomo@gmail.com>
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
# 
# Author: Emanuele Di Giacomo <emanuele.digiacomo@gmail.com>

import os.path
import mailbox
import email.utils
from datetime import datetime
import logging


logger = logging.getLogger("splitmail")


def splitbox(boxfile, fmt, filtermsg=None, copy=True, dry_run=False):
    box = mailbox.mbox(boxfile)

    for k, m in box.iteritems():
        if filtermsg is None or not filtermsg(m):
            continue
        h = dict(m.items())
        t = email.utils.parsedate_tz(m.get('Date'))
        h['Date'] = datetime.utcfromtimestamp(email.utils.mktime_tz(t))
        f = fmt.format(**h)
        logger.info("Saving message %s in mailbox %s", k, f)
        if not dry_run:
            outbox = mailbox.mbox(f, create=True)
            outbox.lock()
            outbox.add(m)
            outbox.unlock()
            outbox.close()

        if not copy:
            logger.info("Removing message %s", k)
            if not dry_run:
                box.lock()
                box.discard(k)
                box.unlock()

    box.close()


def parse_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d')


def create_filtermsg(untildate):
    def wrapper(m):
        if untildate is None:
            return True
        t = email.utils.parsedate_tz(m.get('Date'))
        d = datetime.utcfromtimestamp(email.utils.mktime_tz(t))
        return d < untildate
    return wrapper


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('mailbox', metavar='MAILBOX')
    parser.add_argument('-o', '--output-dir', metavar='PATH', default=None)
    parser.add_argument('-a', '--archive-name', metavar='NAME', default=None)
    parser.add_argument('-p', '--prefix', metavar='NAME', default='')
    parser.add_argument('-s', '--suffix', metavar='NAME', default='_{Date:%Y}')
    parser.add_argument('-c', '--copy', action='store_true', default=False)
    parser.add_argument('-n', '--dry-run', action='store_true', default=False)
    parser.add_argument('-D', '--date', type=parse_datetime, default=None)
    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    if args.archive_name is None:
        args.archive_name = os.path.basename(args.mailbox)

    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.mailbox)

    fmt = os.path.join(args.output_dir,
                       args.prefix + args.archive_name + args.suffix)
    splitbox(args.mailbox, fmt, 
             filtermsg=create_filtermsg(args.date),
             copy=args.copy, dry_run=args.dry_run)
