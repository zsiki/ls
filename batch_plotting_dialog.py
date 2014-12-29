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
    def __init__(self, iface, batch_plotting):
        """ Initialize dialog data and event handlers
        """
        super(BatchPlottingDialog, self).__init__()
        self.ui = Ui_BatchPlottingDialog()
        self.ui.setupUi(self)
        self.iface = iface
        # if batch_plotting is True -> plotting by selected polygons
        #                     False -> plot map canvas
        self.batch_plotting = batch_plotting

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

        if not self.batch_plotting:
            self.ui.LayersComboBox.addItem("Map canvas")
            return
        
        registry = QgsMapLayerRegistry.instance()
        layers = registry.mapLayers().values()
        if len(layers) == 0:
            return
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() == QGis.Polygon:
                    self.ui.LayersComboBox.addItem(layer.name(),layer)
            
        #polygon_layers = get_vector_layers_by_type(QGis.Polygon)
        #self.ui.LayersComboBox.addItems(polygon_layers)
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
        selected_layer = self.ui.LayersComboBox.itemData(self.ui.LayersComboBox.currentIndex())
        selected_polygons = get_features(selected_layer.name(),QGis.Polygon,True)
        if selected_polygons is None:
            QMessageBox.warning(self, tr("Warning"),
                tr("Select at least one polygon on layer '%s'!"%selected_layer.name()))
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
        # get map renderer of map canvas        
        renderer = self.iface.mapCanvas().mapRenderer()
        self.composition = QgsComposition(renderer)
        self.composition.loadFromTemplate(document)

        cmap = self.composition.composerMapItems()[0]
        #cmap.setNewExtent(bbox)
        cmap.setNewScale(scale)
        cmap.setGridIntervalX(scale/10)
        cmap.setGridIntervalY(scale/10)
        cmap.setAtlasDriven(True)
        cmap.setAtlasScalingMode( QgsComposerMap.Fixed )

        atlas = self.composition.atlasComposition()
        atlas.setEnabled(True)
        #layer = get_layer_by_name(selected_layer)
        atlas.setCoverageLayer( selected_layer )
        atlas.setHideCoverage(False)
        atlas.setFilenamePattern("'output_'||$feature")
        atlas.setSingleFile(False)   # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        atlas.setSortFeatures(False)   # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        atlas.setFilterFeatures(True)
        selected_ids = [f.id() for f in selected_layer.selectedFeatures()]
        filter_id_string = ','.join([str(sid) for sid in selected_ids])
        atlas.setFeatureFilter("$id in (" + filter_id_string + ")")

        if self.ui.OutputTab.currentIndex() == 0:    # to PDF
            self.composition.setAtlasMode( QgsComposition.ExportAtlas )
            #atlas.beginRender()
            #for i in range(0, atlas.numFeatures()):
            #    atlas.prepareForFeature(i)
            #    myImage = self.composition.printPageAsRaster(0)
            #    myImage.save(output_jpeg)
            #atlas.endRender() 
            pass
        elif self.ui.OutputTab.currentIndex() == 1:  # to Printer
            pass 
        elif self.ui.OutputTab.currentIndex() == 2:  # to Composer View
            # create new composer
            self.composition.setAtlasMode( QgsComposition.PreviewAtlas )
            composer = self.iface.createNewComposer() 
            composer.setComposition(self.composition)
            composer.composerWindow().on_mActionAtlasPreview_triggered(True)
            # Increase the reference count of the composer object 
            # for not being garbage collected.
            # If not doing this composer would lost reference and qgis would crash 
            # when referring to this composer object or at quit.
            ctypes.c_long.from_address( id(composer) ).value += 1

    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.reject()
    
