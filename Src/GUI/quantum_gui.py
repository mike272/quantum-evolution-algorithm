from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QFrame, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QLabel,
                             QPushButton,QSpinBox, QDialog, QLineEdit,
                             QCheckBox, QDialogButtonBox, QWidget, QProgressBar,
                             QListView, QTextBrowser, QApplication, QSpacerItem,
                             QSizePolicy)
from pathlib import Path
import sys

from Src.settings import Settings

class describedWidget:
    def __init__(self, widget:QWidget, description="", tooltip=""):
        self.widget = widget
        self.description = description
        self.tooltip = tooltip

class QuantumGUI(object):
    def __init__(self, settings:Settings):

        self.settings = settings

        self.app = QApplication(sys.argv)

        self.mainDialog = QDialog()
        self.mainDialog.setWindowTitle("Quantum Evolution GUI")
        self.mainDialog.setWindowModality(Qt.NonModal)
        self.mainDialog.setMinimumSize(800, 500)
        self.mainLayout = QHBoxLayout(self.mainDialog)

        self.visualizationAndProgressLayout = QVBoxLayout()
        self.configurationAndConsoleLayout = QVBoxLayout()
        self.layersConfigurationLayout = QVBoxLayout()

        ## VISUALIZATION

        self.visualizationLabel = QLabel("Best performing model statistics")
        self.visualizationWidget = QWidget()
        self.visualizationWidget.setStyleSheet("background-color: white; border: 1px solid black;")

        self.progressBar = QProgressBar(minimum = 0, maximum = 100, value = 10)
        self.progressBarLabel = QLabel("This will describe what is happening right now\n(What process is running)")

        
        ## BOTTOM BUTTONS
        self.buttonsLayout = QHBoxLayout()
        self.startTrainingButton = QPushButton("Start training")
        self.startTrainingButton.clicked.connect(self.startTraining)
        self.testModelButton = QPushButton("Test on an image...")
        self.testModelButton.clicked.connect(self.testModel)


        ## BASIC SETTINGS
        self.modelNameTextBox = QLineEdit()
        self.modelNameTextBox.setText(str(self.settings.model_name))

        self.babiesCountTextBox = QLineEdit()
        self.babiesCountTextBox.setText(str(self.settings.babies_count))

        self.leadersCountTextBox = QLineEdit()
        self.leadersCountTextBox.setText(str(self.settings.leaders_count))

        self.initialBitsCountTextBox = QLineEdit()
        self.initialBitsCountTextBox.setText(str(self.settings.initial_bits_count))

        self.initialBitsCountTextBox = QLineEdit()
        self.initialBitsCountTextBox.setText(str(self.settings.initial_bits))

        self.epochsTextBox = QLineEdit()
        self.epochsTextBox.setText(str(self.settings.epochs))

        self.batchSizeTextBox = QLineEdit()
        self.batchSizeTextBox.setText(str(self.settings.batch_size))

        self.mutationRateTextBox = QLineEdit()
        self.mutationRateTextBox.setText(str(self.settings.mutation_rate))

        self.validationSplitTextBox = QLineEdit()
        self.validationSplitTextBox.setText(str(self.settings.validation_split))

   

        ## CONSOLE STUFF
        self.consoleSettingsLayout = QHBoxLayout()
        self.verboseCheckBox = QCheckBox()
        self.verboseCheckBox.setChecked(False)

        self.printSummaryCheckBox = QCheckBox()
        self.printSummaryCheckBox.setChecked(False)
        
        self.consoleSpacer = QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.consoleLayout = QVBoxLayout()
        self.consoleLabel = QLabel("Console output")
        self.consoleLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.consoleWidget = QWidget()
        self.consoleWidget.setStyleSheet("background-color: black;")
        self.consoleText = QTextBrowser(self.consoleWidget)
        self.consoleText.setText("This will show console output")
        self.consoleText.setStyleSheet("color: white;")
        

        ## LAYERS SETTINGS
        self.convLayersLabel = QLabel("Convolutional Layers")
        #self.convLayersLabel.setStyleSheet("font-size: 14px; ")
        self.convLayersList = QWidget()
        self.convLayersList.setStyleSheet("background-color: white;")

        self.middleLayerLabel = QLabel("Middle layer")
        #self.middleLayerLabel.setStyleSheet("font-size: 14px;")
        self.middleLayerTextBox = QLineEdit()
        self.middleLayerTextBox.setText(str(self.settings.middle_layer))
        
        self.denseLayersLabel = QLabel("Dense Layers")
        #self.denseLayersLabel.setStyleSheet("font-size: 14px;")
        self.denseLayersList = QWidget()
        self.denseLayersList.setStyleSheet("background-color: white;")


        self.build_layout()

        print("Build complete")
        self.mainDialog.show()
        sys.exit(self.app.exec_())

    def build_layout(self):

        ## LEFT

        self.visualizationAndProgressLayout.addWidget(self.visualizationWidget, 8)
        self.visualizationAndProgressLayout.addWidget(self.progressBar,1)
        self.visualizationAndProgressLayout.addWidget(self.progressBarLabel,1)
        
        self.buttonsLayout.addWidget(self.startTrainingButton)
        self.buttonsLayout.addWidget(self.loadModelButton)
        self.buttonsLayout.addWidget(self.testModelButton)

        self.visualizationAndProgressLayout.addLayout(self.buttonsLayout, 1)

        self.mainLayout.addLayout(self.visualizationAndProgressLayout, 2)

        ## MIDDLE

        self.addDescribedWidget(parent=self.configurationAndConsoleLayout, listWidgets=[
            describedWidget(
                widget=self.modelNameTextBox,
                description="Name:",
                tooltip="Name of the model"
            ),
            describedWidget(
                widget=self.epochsTextBox,
                description="Epochs:",
                tooltip="Number of epochs, must be an int"
            ),
            describedWidget(
                widget=self.batchSizeTextBox,
                description="Batch size:",
                tooltip="Number of images in a single batch, must be an int"
            ),
            describedWidget(
                widget=self.mutationRateTextBox,
                description="Learning rate:",
                tooltip="Speed of gradient descent, must be 0.001 - 0.1"
            ),
            describedWidget(
                widget=self.validationSplitTextBox,
                description="Validation split:",
                tooltip="Percentage of images used for validation, 0.05-0.95"
            ),
            describedWidget(
                widget=self.optimizerTextBox,
                description="Optimizer:",
                tooltip="TODO enforce specific values"
            )
        ])

        self.configurationAndConsoleLayout.addItem(self.consoleSpacer)
        self.configurationAndConsoleLayout.addWidget(self.consoleLabel,1)
        self.configurationAndConsoleLayout.addWidget(self.consoleWidget, 3)

        self.addDescribedWidget(parent=self.consoleSettingsLayout, listWidgets=[
            describedWidget(
                widget=self.verboseCheckBox,
                description="TF Verbose:",
                tooltip="TODO"
            ),
            describedWidget(
                widget=self.printSummaryCheckBox,
                description="Print summary:",
                tooltip="Print model summary in console"
            )
        ])

        self.configurationAndConsoleLayout.addLayout(self.consoleSettingsLayout,2)

    
        self.mainLayout.addLayout(self.configurationAndConsoleLayout, 1)

        ## RIGHT
        
        self.layersConfigurationLayout.addWidget(self.convLayersLabel)
        self.layersConfigurationLayout.addWidget(self.convLayersList,5)

        self.layersConfigurationLayout.addWidget(self.middleLayerLabel)
        self.layersConfigurationLayout.addWidget(self.middleLayerTextBox)

        self.layersConfigurationLayout.addWidget(self.denseLayersLabel)
        self.layersConfigurationLayout.addWidget(self.denseLayersList,5)

        self.mainLayout.addLayout(self.layersConfigurationLayout, 1)


    def loadModel(self):
        pass


    def testModel(self):
        pass
        '''
        if self.customSettings.isChecked():
            self.hideableWidget.show()
            self.mainDialog.adjustSize()
        else:
            self.hideableWidget.hide()
            self.mainDialog.adjustSize()
        '''

    def startTraining(self):
        pass
        '''
        self.doc = self.app.activeDocument()

        if self.exportDirTextBox.text() == "" \
            and self.doc \
                and self.doc.fileName():
                    self.exportPath = Path(self.doc.fileName()).parents[0]
                    self.exportDirTextBox.setText(str(self.exportPath))

        self.mainDialog.setWindowTitle("Automatic Spritesheet Exporter")
        self.mainDialog.setSizeGripEnabled(True)
        self.mainDialog.show()
        self.mainDialog.activateWindow()
        self.mainDialog.setDisabled(False)
        

    def changeExportDir(self):
        self.exportDirDialog = QFileDialog()
        self.exportDirDialog.setWindowTitle("Choose Export Directory")
        self.exportDirDialog.setSizeGripEnabled(True)
        self.exportDirDialog.setDirectory(str(self.exportPath))

        self.exportPath = self.exportDirDialog.getExistingDirectory()
        if self.exportPath != "":
            self.exportDirTextBox.setText(str(self.exportPath))

    def confirmButton(self):
        self.mainDialog.setDisabled(True)

        # Basic
        self.exp.exportName = self.exportNameTextBox.text()
        self.exp.exportDir = Path(self.exportDirTextBox.text())
        
        # Advanced
        self.exp.layerNameSplit = self.layerNameSplitTextBox.text()
        self.exp.backgroundLayerName = self.backgroundLayerNameTextBox.text()
        self.exp.referenceLayerName = self.referenceLayerNameTextBox.text()

        self.exp.convertToGrayScale = self.grayscaleSettings.isChecked()
        self.exp.exportMergedMode = self.exportMergedSettings.isChecked()
        self.exp.exportVisibleInstead = self.exportVisibleSettings.isChecked()

        self.exp.scaleImage = self.scaleSheetSettings.isChecked()
        self.exp.scaleAmount = self.scaleAmount.value()

        self.exp.rows = self.rows.value()
        self.exp.columns = self.columns.value()
            
        self.exp.export()
        self.mainDialog.hide()
        '''

    def addDescribedWidget(self, parent, listWidgets: List[describedWidget], align=Qt.AlignLeft):
        layout = QGridLayout()
        row = 0
        for widget in listWidgets:
            label = QLabel(widget.description)
            if widget.description != "":
                label.setBuddy(widget.widget)
                layout.addWidget(label, row, 0)
            layout.addWidget(widget.widget, row, 1)
            if widget.tooltip != "":
                widget.widget.setToolTip(widget.tooltip)
                label.setToolTip(widget.tooltip)
            row += 1
        layout.setAlignment(align)
        parent.addLayout(layout)
        return layout