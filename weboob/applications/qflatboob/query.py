# -*- coding: utf-8 -*-

# Copyright(C) 2010-2012 Romain Bignon
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

from PyQt4.QtGui import QDialog, QListWidgetItem
from PyQt4.QtCore import SIGNAL, Qt

from weboob.tools.application.qt import QtDo, HTMLDelegate

from .ui.query_ui import Ui_QueryDialog

class QueryDialog(QDialog):
    def __init__(self, weboob, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_QueryDialog()
        self.ui.setupUi(self)

        self.weboob = weboob
        self.ui.resultsList.setItemDelegate(HTMLDelegate())
        self.ui.citiesList.setItemDelegate(HTMLDelegate())

        self.search_process = None

        self.connect(self.ui.cityEdit, SIGNAL('returnPressed()'), self.searchCity)
        self.connect(self.ui.resultsList, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.insertCity)
        self.connect(self.ui.citiesList, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.removeCity)

    def keyPressEvent(self, event):
        """
        Disable handler <Enter> and <Escape> to prevent closing the window.
        """
        event.ignore()

    def searchCity(self):
        pattern = unicode(self.ui.cityEdit.text())
        self.ui.resultsList.clear()
        self.ui.cityEdit.clear()
        self.ui.cityEdit.setEnabled(False)

        self.search_process = QtDo(self.weboob, self.addResult)
        self.search_process.do('search_city', pattern)

    def addResult(self, backend, city):
        if not backend or not city:
            self.search_process = None
            self.ui.cityEdit.setEnabled(True)
            return
        item = QListWidgetItem()
        item.setText('<b>%s</b> (%s)' % (city.name, backend.name))
        item.setData(Qt.UserRole, city)
        self.ui.resultsList.addItem(item)
        self.ui.resultsList.sortItems()

    def insertCity(self, i):
        item = QListWidgetItem()
        item.setText(i.text())
        item.setData(Qt.UserRole, i.data(Qt.UserRole))
        self.ui.citiesList.addItem(item)

    def removeCity(self, item):
        print item
        self.ui.citiesList.removeItemWidget(item)