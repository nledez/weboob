# -*- coding: utf-8 -*-

# Copyright(C) 2012 Florent Fourcot
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


import sys

from weboob.capabilities.bill import ICapBill, Detail
from weboob.tools.application.repl import ReplApplication


__all__ = ['Boobill']


class Boobill(ReplApplication):
    APPNAME = 'boobill'
    VERSION = '0.b'
    COPYRIGHT = 'Copyright(C) 2012 Florent Fourcot'
    DESCRIPTION = 'Console application allowing to get and download bills.'
    CAPS = ICapBill
    DEFAULT_FORMATTER = 'table'

    def main(self, argv):
        self.load_config()
        return ReplApplication.main(self, argv)

    def do_subscriptions(self, line):
        """
        subscriptions

        List subscriptions
        """
        for backend, subscription in self.do('iter_subscription'):
            self.add_object(subscription)
            self.format(subscription)
        self.flush()

    def do_details(self, id):
        """
        details Id

        Get details of a subscription.
        """

        id, backend_name = self.parse_id(id)
        if not id:
            print >>sys.stderr, 'Error: please give an subscription ID (hint: use subscriptions command)'
            return 2
        names = (backend_name,) if backend_name is not None else None

        def do(backend):
            return backend.get_details(id)

        # XXX: should be generated by backend?
        mysum = Detail()
        mysum.label = "Sum"
        mysum.infos = "Generated by boobill"
        mysum.price = 0.
        for backend, detail in self.do(do, backends=names):
            self.format(detail)
            mysum.price = detail.price + mysum.price

        self.format(mysum)
        self.flush()

    def do_history(self, id):
        """
        history Id

        Get the history of a subscription.
        """

        id, backend_name = self.parse_id(id)
        if not id:
            print >>sys.stderr, 'Error: please give an subscription ID (hint: use subscriptions command)'
            return 2
        names = (backend_name,) if backend_name is not None else None

        def do(backend):
            return backend.iter_history(id)

        for backend, history in self.do(do, backends=names):
            self.format(history)
        self.flush()
