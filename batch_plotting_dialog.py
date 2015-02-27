# -*- coding: utf-8 -*-
"""
.. module:: batch_plotting_dialog
    :platform: Linux, Windows
    :synopsis: GUI for batch plotting

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
import ctypes, sys
from PyQt4.QtCore import QCoreApplication, QDir, QFile, QFileInfo, QIODevice, \
                        QSizeF, Qt
from PyQt4.QtGui import QDialog, QFileDialog, QListWidgetItem, QMessageBox, \
                        QPrintDialog, QPrinter, QAbstractPrintDialog, QPainter, \
                        QProgressDialog, QApplication
from PyQt4.QtXml import QDomDocument
from batch_plotting import Ui_BatchPlottingDialog
from qgis.core import *
from surveying_util import get_vector_layers_by_type, get_features
from base_classes import tr

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
        self.ui.OutputTab.setCurrentIndex(2)
        # if batch_plotting is True -> plotting by selected polygons
        #                     False -> plot map canvas
        self.batch_plotting = batch_plotting
        if not self.batch_plotting:
            self.setWindowTitle(tr("Plot by Template"))
            self.ui.OutputTab.setTabEnabled(0,False)
            self.ui.OutputTab.setTabEnabled(1,False)

        # event handlers
        self.ui.PlotButton.clicked.connect(self.onPlotButton)
        self.ui.TempDirButton.clicked.connect(self.onTempDirButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.TemplateList.setSortingEnabled(True)

        # set paths        
        self.plugin_dir = QDir().cleanPath( QFileInfo(__file__).absolutePath() )
        self.templatepath = QDir(self.plugin_dir).absoluteFilePath("template")
        self.pdfpath = ""
        
        if self.batch_plotting:
            self.ui.OutputPDFEdit.setText( QgsAtlasComposition(None).filenamePattern() )
            self.ui.SingleFileCheckbox.stateChanged.connect(self.changedSingleFileCheckbox)
        else:
            # set scale to map canvas scale
            self.ui.ScaleCombo.insertItem(0,"%d"%round(self.iface.mapCanvas().scale()))
            self.ui.ScaleCombo.insertItem(0,"<extent>")
            self.ui.ScaleCombo.setCurrentIndex(0)

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
        # if batch plotting is false only map canvas will be in the list
        if not self.batch_plotting:
            self.ui.LayersComboBox.addItem(tr("<Map view>"))
            self.ui.LayersComboBox.setCurrentIndex(0)
            return
        # if batch plotting is true fill layers combo
        polygon_layers = get_vector_layers_by_type(QGis.Polygon)
        if polygon_layers is None:
            return
        for layer in polygon_layers:
            self.ui.LayersComboBox.addItem(layer.name(),layer)
            
        # get current layer name
        try:
            actlayer_name = self.iface.activeLayer().name()
        except (AttributeError):
            actlayer_name = ""

        if self.ui.LayersComboBox.findText(oldSelectedLayer) == -1:
            self.ui.LayersComboBox.setCurrentIndex( self.ui.LayersComboBox.findText(actlayer_name) )
        else:
            self.ui.LayersComboBox.setCurrentIndex( self.ui.LayersComboBox.findText(oldSelectedLayer) )

    def fillTemplateList(self):
        """ Fill the listbox of composer template files.
        """
        if self.ui.TemplateList.currentItem() is not None:
            oldSelectedTemplate = self.ui.TemplateList.currentItem().text()
        else:
            oldSelectedTemplate = ""
        self.ui.TemplateList.clear()
        
        tempdir = QDir(self.templatepath)
        if  tempdir.exists():
            fileinfolist = tempdir.entryInfoList(["*.qpt"], QDir.Files | QDir.NoDotAndDotDot | QDir.NoSymLinks, QDir.NoSort)
            for fi in fileinfolist:
                item = QListWidgetItem(fi.fileName())
                self.ui.TemplateList.addItem(item)
                if fi.fileName() == oldSelectedTemplate:
                    self.ui.TemplateList.setCurrentItem( item )

    def onTempDirButton(self):
        """ Change the directory that contains print composer templates.
        """
        templatepath = QFileDialog.getExistingDirectory(self, 
                        tr("Select Directory"),
                        self.templatepath,
                        QFileDialog.ShowDirsOnly)
        if templatepath!="":
            self.templatepath = templatepath
        self.fillTemplateList()
        
    def changedSingleFileCheckbox(self, state):
        self.ui.OutputPDFEdit.setEnabled(not state)
        
    def onPlotButton(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        # check if one layer is selected
        if self.ui.LayersComboBox.currentIndex() == -1:
            QMessageBox.warning(self, tr("Warning"), tr("Select a layer!"))
            self.ui.LayersComboBox.setFocus()
            return
        # check if one composition template is selected
        if self.ui.TemplateList.selectedItems() == []:
            QMessageBox.warning(self, tr("Warning"), tr("Select a composer template!"))
            self.ui.TemplateList.setFocus()
            return
        template_filename = QDir(self.templatepath).absoluteFilePath(
                                      self.ui.TemplateList.currentItem().text())
        
        # get the scale
        if self.ui.ScaleCombo.currentText()=="<extent>":
            scale = -1
        else:
            try:
                scale = int(self.ui.ScaleCombo.currentText())
            except (ValueError):
                QMessageBox.warning(self, tr("Warning"), tr("Scale must be a positive integer value!"))
                self.ui.ScaleCombo.setFocus()
                return
            if scale<=0:
                QMessageBox.warning(self, tr("Warning"), tr("Scale must be a positive integer value!"))
                self.ui.ScaleCombo.setFocus()
                return
        
        # get composer name
        composer_name = self.ui.ComposerEdit.text()
        
        #check if there are selected items on polygon layers
        if self.batch_plotting:
            selected_layer = self.ui.LayersComboBox.itemData(self.ui.LayersComboBox.currentIndex())
            selected_polygons = get_features(selected_layer.name(),QGis.Polygon,True)
            if selected_polygons is None:
                QMessageBox.warning(self, tr("Warning"),
                    tr("Select at least one polygon on layer '%s'!"%selected_layer.name()))
                return
        
        # check output setting
        if self.ui.OutputTab.currentIndex() == 0:    # to PDF
            if not self.ui.SingleFileCheckbox.checkState():
                if len( self.ui.OutputPDFEdit.text() ) == 0:
                    res = QMessageBox.warning(self, tr("Warning"),
                        tr("The filename pattern is empty. A default one will be used."),
                        QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
                    if res == QMessageBox.Cancel:
                        return
                    self.ui.OutputPDFEdit.setText( QgsAtlasComposition(None).filenamePattern() )
        elif self.ui.OutputTab.currentIndex() == 1:  # to Printer
            # no need for checking
            pass
        elif self.ui.OutputTab.currentIndex() == 2:  # to Composer View
            # no need for checking yet
            pass

        # get map renderer of map canvas        
        renderer = self.iface.mapCanvas().mapRenderer()
        self.composition = QgsComposition(renderer)

        # if plot to Composer View the composition must be set 
        # before loading the template 
        # otherwise composer's item properties doesn't appear
        if self.ui.OutputTab.currentIndex() == 2:  # to Composer View
            if len(composer_name)==0:
                composer = self.iface.createNewComposer()
            else: 
                composer = self.iface.createNewComposer(composer_name)
            composer.setComposition(self.composition)

        # read template file and add to composition
        template_file = QFile( template_filename )
        template_file.open(QIODevice.ReadOnly | QIODevice.Text)
        template_content = template_file.readAll()
        template_file.close()
        document = QDomDocument()
        document.setContent(template_content)
        self.composition.loadFromTemplate(document)

        # if batch_plotting is True create an atlas composition
        if self.batch_plotting:
            # get composer map item and set new scale and the grid
            cmap = self.composition.getComposerMapById(0)
            cmap.setNewScale(scale)
            cmap.setGridIntervalX(scale/10)
            cmap.setGridIntervalY(scale/10)
            cmap.setAtlasDriven(True)
            cmap.setAtlasScalingMode( QgsComposerMap.Fixed )

            # set atlas composition parameters
            atlas = self.composition.atlasComposition()
            atlas.setEnabled(True)
            atlas.setCoverageLayer( selected_layer )
            atlas.setHideCoverage(False)
            atlas.setFilenamePattern( self.ui.OutputPDFEdit.text() )
            atlas.setSingleFile( self.ui.SingleFileCheckbox.checkState() )
            atlas.setSortFeatures(False)
            atlas.setFilterFeatures(True)
            selected_ids = [f.id() for f in selected_layer.selectedFeatures()]
            filter_id_string = ','.join([str(sid) for sid in selected_ids])
            atlas.setFeatureFilter("$id in (" + filter_id_string + ")")

            # print the complete atlas composition
            if self.ui.OutputTab.currentIndex() == 0:    # to PDF
                self.composition.setAtlasMode( QgsComposition.ExportAtlas )
                
                if self.pdfpath=="":
                    self.pdfpath = QgsProject.instance().homePath().encode(sys.getfilesystemencoding())
                    
                if self.ui.SingleFileCheckbox.checkState():
                    #print to single pdf (multi-page)
                    outputFileName = QDir(self.pdfpath).absoluteFilePath("qgis.pdf")
                    outputFileName = QFileDialog.getSaveFileName(self,
                       tr( "Choose a file name to save the map as" ),
                       outputFileName,
                       tr( "PDF Format" ) + " (*.pdf *.PDF)" )
                    if not outputFileName:
                        return
                    if not outputFileName.lower().endswith(".pdf"):
                        outputFileName += ".pdf"
                    self.pdfpath = QDir(outputFileName).absolutePath()
                else:
                    #print to more pdf
                    outputDir = QFileDialog.getExistingDirectory( self,
                        tr( "Directory where to save PDF files" ),
                        self.pdfpath,
                        QFileDialog.ShowDirsOnly )
                    if not outputDir:
                        return
                    # test directory (if it exists and is writable)
                    if not QDir(outputDir).exists() or not QFileInfo(outputDir).isWritable():
                        QMessageBox.warning( self, tr( "Unable to write into the directory" ),
                            tr( "The given output directory is not writable. Cancelling." ) )
                        return
                    self.pdfpath = outputDir
                
                printer = QPrinter()
                painter = QPainter()
                if not len(atlas.featureFilterErrorString()) == 0:
                    QMessageBox.warning( self, tr( "Atlas processing error" ),
                        tr( "Feature filter parser error: %s" % atlas.featureFilterErrorString() ) )
                    return

                atlas.beginRender()

                if self.ui.SingleFileCheckbox.checkState():
                    #prepare for first feature, so that we know paper size to begin with
                    atlas.prepareForFeature(0)
                    self.composition.beginPrintAsPDF(printer, outputFileName)
                    # set the correct resolution
                    self.composition.beginPrint(printer)
                    printReady =  painter.begin(printer)
                    if not printReady:
                        QMessageBox.warning( self, tr( "Atlas processing error" ),
                              tr( "Error creating %s." % outputFileName ) )
                        return
                    
                progress = QProgressDialog( tr( "Rendering maps..." ), tr( "Abort" ), 0, atlas.numFeatures(), self )
                QApplication.setOverrideCursor( Qt.BusyCursor )
                
                for featureI in range(0, atlas.numFeatures()):
                    progress.setValue( featureI+1 )
                    # process input events in order to allow aborting
                    QCoreApplication.processEvents()
                    if progress.wasCanceled():
                        atlas.endRender()
                        break
                    if not atlas.prepareForFeature( featureI ):
                        QMessageBox.warning( self, tr( "Atlas processing error" ),
                              tr( "Atlas processing error" ) )
                        progress.cancel()
                        QApplication.restoreOverrideCursor()
                        return
                    if not self.ui.SingleFileCheckbox.checkState():
                        multiFilePrinter = QPrinter()
                        outputFileName = QDir( outputDir ).filePath( atlas.currentFilename() ) + ".pdf"
                        self.composition.beginPrintAsPDF( multiFilePrinter, outputFileName )
                        # set the correct resolution
                        self.composition.beginPrint( multiFilePrinter )
                        printReady = painter.begin( multiFilePrinter )
                        if not printReady:
                            QMessageBox.warning( self, tr( "Atlas processing error" ),
                                tr( "Error creating %s." % outputFileName ) )
                            progress.cancel()
                            QApplication.restoreOverrideCursor()
                            return
                        self.composition.doPrint( multiFilePrinter, painter )
                        painter.end()
                    else:
                        # start print on a new page if we're not on the first feature
                        if featureI > 0:
                            printer.newPage()
                        self.composition.doPrint( printer, painter )
                    
                atlas.endRender()
                if self.ui.SingleFileCheckbox.checkState():
                    painter.end()
                QApplication.restoreOverrideCursor()

            elif self.ui.OutputTab.currentIndex() == 1:  # to Printer
                # if To Printer is selected set the printer
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
                
                QApplication.setOverrideCursor(Qt.BusyCursor)
                #prepare for first feature, so that we know paper size to begin with
                self.composition.setAtlasMode( QgsComposition.ExportAtlas )
                atlas.prepareForFeature(0)

                # set orientation                
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

                self.composition.beginPrint( self.printer )
                painter = QPainter(self.printer)
                if not len(atlas.featureFilterErrorString()) == 0:
                    QMessageBox.warning( self, tr( "Atlas processing error" ),
                        tr( "Feature filter parser error: %s" % atlas.featureFilterErrorString() ) )
                    QApplication.restoreOverrideCursor()
                    return

                atlas.beginRender()
                progress = QProgressDialog( tr( "Rendering maps..." ), tr( "Abort" ), 0, atlas.numFeatures(), self )
                for featureI in range(0, atlas.numFeatures()):
                    progress.setValue( featureI+1 )
                    # process input events in order to allow cancelling
                    QCoreApplication.processEvents()
                    if progress.wasCanceled():
                        atlas.endRender()
                        break
                    if not atlas.prepareForFeature( featureI ):
                        QMessageBox.warning( self, tr( "Atlas processing error" ),
                              tr( "Atlas processing error" ) )
                        progress.cancel()
                        QApplication.restoreOverrideCursor()
                        return

                    # start print on a new page if we're not on the first feature
                    if featureI > 0:
                        self.printer.newPage()
                    self.composition.doPrint( self.printer, painter )
                
                atlas.endRender()
                painter.end()
                QApplication.restoreOverrideCursor()

            elif self.ui.OutputTab.currentIndex() == 2:  # to Composer View
                # create new composer
                self.composition.setAtlasMode( QgsComposition.PreviewAtlas )
                composer.composerWindow().on_mActionAtlasPreview_triggered(True)
                atlas.parameterChanged.emit()
                # Increase the reference count of the composer object 
                # for not being garbage collected.
                # If not doing this composer would lost reference and qgis would crash 
                # when referring to this composer object or at quit.
                ctypes.c_long.from_address( id(composer) ).value += 1
        else:
            # if batch_plotting is False open a QgsComposerView with current map canvas
            cmap = self.composition.getComposerMapById(0)
            # set the new extent of composer map item
            newextent = self.iface.mapCanvas().mapRenderer().extent()
            currentextent = cmap.extent()
            canvas_ratio = newextent.width()/newextent.height()
            map_ratio = currentextent.width()/currentextent.height()
            if map_ratio < canvas_ratio:
                dh = newextent.width() / map_ratio - newextent.height()
                newextent.setYMinimum( newextent.yMinimum() - dh / 2 )
                newextent.setYMaximum( newextent.yMaximum() + dh / 2 )
            else:
                dw = map_ratio * newextent.height() - newextent.width()
                newextent.setXMinimum( newextent.xMinimum() - dw / 2 )
                newextent.setXMaximum( newextent.xMaximum() + dw / 2 )
            cmap.setNewExtent(newextent)
            # set the new scale of composer map item
            if scale>0:
                cmap.setNewScale(scale)
            sc = cmap.scale()
            # set the grid interval according to the scale
            cmap.setGridIntervalX(sc/10)
            cmap.setGridIntervalY(sc/10)
            # Increase the reference count of the composer object 
            # for not being garbage collected.
            # If not doing this composer would lost reference and qgis would crash 
            # when referring to this composer object or at quit.
            ctypes.c_long.from_address( id(composer) ).value += 1

        self.accept()

    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.reject()
    
