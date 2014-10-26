# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SurveyingCalculation
                                 A QGIS plugin
 To solve surveying calculations
                              -------------------
        begin                : 2014-10-17
        git sha              : $Format:%H$
        copyright            : (C) 2014 by DigiKom Kft.
        email                : mail@digikom.hu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# generic python modules
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant, QFile
from PyQt4.QtGui import QAction, QIcon, QMenu, QMessageBox, QFileDialog
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
import os.path
import re
from shutil import copyfile

# plugin specific python modules
from surveying_calculation_dialog import SurveyingCalculationDialog
from totalstations import *

class SurveyingCalculation:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'surveying_calculation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SurveyingCalculationDialog()

        # Declare instance attributes

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SurveyingCalculation', message)

    def add_action(self, icon_path, text, callback, enabled_flag=True,
        add_to_menu=True, add_to_toolbar=True, status_tip=None,
        whats_this=None, parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str
        :param text: Text that should be shown in menu items for this action.
        :type text: str
        :param callback: Function to be called when the action is triggered.
        :type callback: function
        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str
        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget
        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        self.actions.append(action)
        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SurveyingCalculation/icon.png'
        #self.add_action(
        #    icon_path,
        #    text=self.tr(u'Surveying Calculation'),
        #    callback=self.run,
        #    parent=self.iface.mainWindow())
        # build menu
        self.actions = []
        #self.menu = self.tr(u'&SurveyingCalculation')
        self.menu = QMenu()
        self.menu.setTitle(self.tr(u'&SurveyingCalculation'))
        self.sc_load = QAction(self.tr("Load fieldbook"), self.iface.mainWindow())
        self.sc_help = QAction(self.tr("Help"), self.iface.mainWindow())
        self.sc_about = QAction(self.tr("About"), self.iface.mainWindow())
        self.menu.addActions([self.sc_load, self.sc_help, self.sc_about])
        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[len(actions) - 1]
        menu_bar.insertMenu(lastAction, self.menu)

        self.sc_load.triggered.connect(self.load_fieldbook)
        self.sc_about.triggered.connect(self.about)
        self.sc_help.triggered.connect(self.help)

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SurveyingCalculation')
        self.toolbar.setObjectName(u'SurveyingCalculation')

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # TODO can we remove next?
        #for action in self.actions:
        #    self.iface.removePluginMenu(
        #        self.tr(u'&SurveyingCalculation'),
        #        action)
        #    self.iface.removeToolBarIcon(action)
        del self.menu
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
    
    def load_fieldbook(self):
        """
            Load an electric fieldbook form file (GSI, JOB/ARE, ...)
        """
        fname = QFileDialog.getOpenFileName(self.iface.mainWindow(),
            self.tr('Electric fieldbook'),
            filter= self.tr('Leica GSI (*.gsi);;Geodimeter JOB/ARE (*.job *.are);;Sokkia SDR (*.sdr)'))
        if fname:
            # file selected
            # ask for table name
            ofname = QFileDialog.getSaveFileName(self.iface.mainWindow(),
                self.tr('QGIS fieldbook'),
                os.path.split(fname)[0],
                filter=self.tr('DBF file (*.dbf)'))
            if not ofname:
                return
            if QFile(ofname).exists():
                # overwrite question
                ret = QMessageBox.warning(self.iface.mainWindow(),
                    self.tr("SurveyingCalculation"),
                    self.tr("Do you want to overwrite existing table?"),
                    QMessageBox.Yes | QMessageBox.Default,
                    QMessageBox.Cancel | QMessageBox.Escape)
                if ret == QMessageBox.Cancel:
                    return
            # make a copy of dbf template
            copyfile(os.path.join(self.plugin_dir, 'template', 'fb_template.dbf'), ofname)
            fb_dbf = QgsVectorLayer(ofname, os.path.basename(ofname), "ogr")
            QgsMapLayerRegistry.instance().addMapLayer(fb_dbf)
            if re.search('\.gsi$', fname):
                fb = LeicaGsi(fname)
            elif re.search('\.job', fname) or re.search('\.are$', fname):
                fb = JobAre(fname)
            elif re.search('\.sdr$', fname):
                fb = Sdr(fname)
            else:
                QMessageBox.warning(self.iface.mainWindow(),
                    self.tr('File warning'),
                    self.tr('Unknown fieldbook type'),
                    self.tr('OK'))
                return
            i = 1    # ordinal number for fieldbook records
            fb_dbf.startEditing()
            fb.open()
            while True:
                # get next observation/station data from fieldbook
                r = fb.parse_next()
                if r is None:
                    break    # end of file
                # add row to fieldbook table
                record = QgsFeature()
                # add & initialize attributes
                record.setFields(fb_dbf.pendingFields(), True)
                j = fb_dbf.dataProvider().fieldNameIndex('id')
                if j != -1:
                    record.setAttribute(j, i)
                for key in r:
                    j = fb_dbf.dataProvider().fieldNameIndex(key)
                    if j != -1:
                        record.setAttribute(j, r[key])
                fb_dbf.dataProvider().addFeatures([record])
                i += 1
            fb_dbf.commitChanges()
        return

    def about(self):
        """
            About box of the plugin
        """
        QMessageBox.information(self.iface.mainWindow(),
            self.tr('About'),    
            self.tr('Surveying Calculation Plugin\n\n (c) DigiKom Kft 2014 http://digikom.hu mail (at) digikom.hu\nVersion 0.1a'))

    def help(self):
        # TODO
        pass
