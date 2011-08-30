# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Noé Rubinstein
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

from .backend import GenericComicReaderBackend, DisplayPage

__all__ = ['MangatoshokanBackend']

class MangatoshokanBackend(GenericComicReaderBackend):
    NAME = 'mangatoshokan'
    DESCRIPTION = 'Mangatoshokan manga reading site'
    DOMAIN = "www.mangatoshokan.com"
    IMG_SRC_XPATH = "//img[@id='readerPage']/@src"
    PAGE_LIST_XPATH = "(//select[@class='headerSelect'])[1]/option/@value"
    PAGE_TO_LOCATION = 'http://%s%%s' % DOMAIN
    ID_TO_URL = 'http://www.mangatoshokan.com/read/%s'
    ID_REGEXP = r'[^/]+(?:/[^/]+)*'
    URL_REGEXP = r'.+mangatoshokan.com/read/(%s).+' % ID_REGEXP
    PAGES = { r'http://.+\.mangatoshokan.com/read/.+': DisplayPage }