# -*- coding: utf-8 -*-
"""
.. module:: batch_plotting_dialog
    :platform: Linux, Windows
    :synopsis: GUI for batch plotting

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
import os, glob, ctypes
from PyQt4.QtCore import QFile, QIODevice, QSizeF
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox, QListWidgetItem, \
                        QPrintDialog, QPrinter, QAbstractPrintDialog, QPainter
from PyQt4.QtXml import QDomDocument
from batch_plotting import Ui_BatchPlottingDialog
from base_classes import *
from surveying_util import *

class BatchPlottingDialog(QDialog):
    """ Class for batch plotting dialog
    """
    def __init__(self, iface):
        """ Initialize dialog data and event handlers
        """
        super(BatchPlottingDialog, self).__init__()
        self.ui = Ui_BatchPlottingDialog()
        self.ui.setupUi(self)
        self.iface = iface

        # event handlers
        self.ui.PlotButton.clicked.connect(self.onPlotButton)
        self.ui.TempDirButton.clicked.connect(self.onTempDirButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.TemplateList.setSortingEnabled(True)
        
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.dirpath = os.path.join(self.plugin_dir, 'template')

        self.printer = None
        
    def showEvent(self, event):
        """ Reset dialog when receives a show event.
        """
        self.fillLayersCombo()
        self.fillTemplateList()

    def fillLayersCombo(self):
        """ Fill the polygon layers combobox.
        """
        oldSelectedLayer = self.ui.LayersComboBox.itemText( self.ui.LayersComboBox.currentIndex() )
        self.ui.LayersComboBox.clear()
        polygon_layers = get_vector_layers_by_type(QGis.Polygon)
        self.ui.LayersComboBox.addItems(polygon_layers)
        self.ui.LayersComboBox.setCurrentIndex( self.ui.LayersComboBox.findText(oldSelectedLayer) )

    def fillTemplateList(self):
        """ Fill the listbox of composer template files.
        """
        if self.ui.TemplateList.currentItem() is not None:
            oldSelectedTemplate = self.ui.TemplateList.currentItem().text()
        else:
            oldSelectedTemplate = ""
        self.ui.TemplateList.clear()
        if  os.path.exists(self.dirpath):
            pattern = os.path.join(self.dirpath,'*.qpt')
            for temp in glob.iglob(pattern):
                tname = os.path.basename(temp)
                item = QListWidgetItem(tname)
                self.ui.TemplateList.addItem(item)
                if tname == oldSelectedTemplate:
                    self.ui.TemplateList.setCurrentItem( item )

    def onTempDirButton(self):
        """ Change the directory that contains print composer templates.
        """
        dirpath = str(QFileDialog.getExistingDirectory(self, 
                        "Select Directory",self.dirpath))
        if dirpath!="":
            self.dirpath = dirpath 
        self.fillTemplateList()
        
    def onPlotButton(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        if self.ui.LayersComboBox.currentIndex() == -1:
            QMessageBox.warning(self, tr("Warning"), tr("Select a layer!"))
            self.ui.LayersComboBox.setFocus()
            return
        if self.ui.TemplateList.selectedItems() == []:
            QMessageBox.warning(self, tr("Warning"), tr("Select a composer template!"))
            self.ui.TemplateList.setFocus()
            return
        
        self.template_file = os.path.join(self.dirpath,
            self.ui.TemplateList.currentItem().text())
        try:
            scale = int(self.ui.ScaleCombo.currentText())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Scale must be an integer value!"))
            self.ui.ScaleCombo.setFocus()
            return

        #check if there are selected items on polygon layers
        selected_layer = self.ui.LayersComboBox.currentText()
        selected_polygons = get_features(selected_layer,QGis.Polygon,True)
        if selected_polygons is None:
            QMessageBox.warning(self, tr("Warning"),
                tr("Select at least one polygon on layer '%s'!"%selected_layer))
            return
        
        # check output setting
        if self.ui.OutputTab.currentIndex() == 0:    # to PDF
            # TODO checkings
            pass
        elif self.ui.OutputTab.currentIndex() == 1:  # to Printer
            pass 
        elif self.ui.OutputTab.currentIndex() == 2:  # to Composer View
            # TODO checkings
            pass

        # read template file
        template_file = QFile( self.template_file )
        template_file.open(QIODevice.ReadOnly | QIODevice.Text)
        template_content = template_file.readAll()
        template_file.close()
        document = QDomDocument()
        document.setContent(template_content)
        
        if self.ui.OutputTab.currentIndex() == 1:  # to Printer
            # setting up printer
            if self.printer is None:
                self.printer = QPrinter()
                self.printer.setFullPage(True)
                self.printer.setColorMode(QPrinter.Color)
            # open printer setting dialog
            pdlg = QPrintDialog(self.printer,self)
            pdlg.setModal(True)
            pdlg.setOptions(QAbstractPrintDialog.None)
            if not pdlg.exec_() == QDialog.Accepted:
                return

        # plot all selected polygon
        i = 0
        composer = None
        for polygon in selected_polygons:
            # get map renderer of map canvas        
            renderer = self.iface.mapCanvas().mapRenderer()
            self.composition = QgsComposition(renderer)
            self.composition.loadFromTemplate(document)

            #adjust polygon size to map
            bbox = polygon.boundingBox()
            cmapItems = self.composition.composerMapItems()
            for cmap in cmapItems:
                extent = cmap.extent()
                polygon_ratio = bbox.width()/bbox.height()
                map_ratio = extent.width()/extent.height()
                if map_ratio < polygon_ratio:
                    dh = bbox.width() / map_ratio - bbox.height()
                    bbox.setYMinimum( bbox.yMinimum() - dh / 2 );
                    bbox.setYMaximum( bbox.yMaximum() + dh / 2 );
                else:
                    dw = map_ratio * bbox.height() - bbox.width()
                    bbox.setXMinimum( bbox.xMinimum() - dw / 2 );
                    bbox.setXMaximum( bbox.xMaximum() + dw / 2 );
                cmap.setNewExtent(bbox)
                cmap.setNewScale(scale)
                cmap.setGridIntervalX(scale/10)
                cmap.setGridIntervalY(scale/10)
            
            # plot polygons according to the selected output type
            if self.ui.OutputTab.currentIndex() == 0:    # to PDF
                # create pdf
                i += 1
                fname = "composition_%03d.pdf" % i
                self.composition.exportAsPDF( os.path.join(self.plugin_dir,"temp",fname))
            elif self.ui.OutputTab.currentIndex() == 1:  # to Printer
                # setting up printer
                if self.composition.paperWidth() > self.composition.paperHeight():
                    self.printer.setOrientation(QPrinter.Landscape)
                    self.printer.setPaperSize(
                        QSizeF(self.composition.paperHeight(), self.composition.paperWidth()),
                        QPrinter.Millimeter)
                else:
                    self.printer.setOrientation(QPrinter.Portrait)
                    self.printer.setPaperSize(
                        QSizeF(self.composition.paperWidth(), self.composition.paperHeight()),
                        QPrinter.Millimeter)
                self.printer.setResolution(self.composition.printResolution())

                # send composition to printer
                self.composition.beginPrint(self.printer)
                p = QPainter()
                ready = p.begin(self.printer);
                if not ready:
                    # error beginning print
                    return
                self.composition.doPrint(self.printer, p);
                p.end()
            elif self.ui.OutputTab.currentIndex() == 2:  # to Composer View
                # create new composer (show composer window then hide)
                # (later last composer window will be shown)
                composer = self.iface.createNewComposer() 
                composer.composerWindow().hide()
                composer.setComposition(self.composition)
                # Increase the reference count of the composer object 
                # for not being garbage collected.
                # If not doing this composer would lost reference and qgis would crash 
                # when referring to this composer object or at quit.
                ctypes.c_long.from_address( id(composer) ).value += 1
        
        # the last created composer will be shown
        if composer is not None:
            composer.composerWindow().show()

        # in case of PDF output get a message about successfully creation
        if self.ui.OutputTab.currentIndex() == 0:    # to PDF
            QMessageBox.information(self, tr("Batch plotting"),
                tr("%d PDF files were successfully created!"%i))

        self.accept()
        
    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.reject()
    
