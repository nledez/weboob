# -*- coding: utf-8 -*-

# Copyright(C) 2012 Romain Bignon
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

from weboob.capabilities.housing import ICapHousing, City, Housing
from weboob.tools.backend import BaseBackend

from .browser import PapBrowser


__all__ = ['PapBackend']


class PapBackend(BaseBackend, ICapHousing):
    NAME = 'pap'
    MAINTAINER = u'Romain Bignon'
    EMAIL = 'romain@weboob.org'
    VERSION = '0.b'
    DESCRIPTION = 'French housing website'
    LICENSE = 'AGPLv3+'
    BROWSER = PapBrowser

    def search_housings(self, query):
        cities = [c.id for c in query.cities if c.backend == self.name]
        with self.browser:
            for housing in self.browser.search_housings(cities,
                                                        query.area_min, query.area_max,
                                                        query.cost_min, query.cost_max):
                yield housing

    def get_housing(self, housing):
        if isinstance(housing, Housing):
            id = housing.id
        else:
            id = housing

        with self.browser:
            return self.browser.get_housing(id)

    def search_city(self, pattern):
        with self.browser:
            for city in self.browser.search_geo(pattern):
                c = City(city['id'])
                c.name = city['name']
                yield c

    def fill_housing(self, housing, fields):
        with self.browser:
            return self.browser.get_housing(housing.id)

    OBJECTS = {Housing: fill_housing,
              }