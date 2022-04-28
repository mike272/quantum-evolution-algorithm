from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QFrame, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QLabel,
                             QPushButton,QSpinBox, QDialog, QLineEdit,
                             QCheckBox, QDialogButtonBox, QWidget, QProgressBar,
                             QListView, QTextBrowser, QApplication, QSpacerItem,
                             QSizePolicy, QListWidget, QListWidgetItem)
from pathlib import Path
import sys
from random import randint

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
        self.fitnessLayout = QVBoxLayout()

        ## VISUALIZATION

        self.visualizationLabel = QLabel("Best performing model statistics\n(Epoch: <epoch>, use buttons to navigate)")
        #self.visualizationLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.visualizationWidget = QWidget()
        self.visualizationWidget.setStyleSheet("background-color: white; border: 1px solid black;")

        self.visualizationButtonsLayout = QHBoxLayout()
        self.previousModelButton = QPushButton("Previous")
        self.previousModelButton.clicked.connect(self.startTraining)
        self.nextModelButton = QPushButton("Next")
        self.nextModelButton.clicked.connect(self.testModel)

        self.progressBar = QProgressBar(minimum = 0, maximum = 100, value = 10)
        self.progressBarLabel = QLabel("This will describe what is happening right now\n(What process is running)")

        
        ## BOTTOM BUTTONS
        self.buttonsLayout = QHBoxLayout()
        self.startTrainingButton = QPushButton("Start evolution")
        self.startTrainingButton.clicked.connect(self.startTraining)
        self.testModelButton = QPushButton("Test on an image...")
        self.testModelButton.clicked.connect(self.testModel)


        ## BASIC SETTINGS
        self.modelNameTextBox = QLineEdit()
        self.modelNameTextBox.setText(str(self.settings.model_name))

        self.epochsTextBox = QLineEdit()
        self.epochsTextBox.setText(str(self.settings.epochs))

        self.batchSizeTextBox = QLineEdit()
        self.batchSizeTextBox.setText(str(self.settings.batch_size))

        self.mutationRateTextBox = QLineEdit()
        self.mutationRateTextBox.setText(str(self.settings.mutation_rate))

        self.babiesCountTextBox = QLineEdit()
        self.babiesCountTextBox.setText(str(self.settings.babies_count))

        self.leadersCountTextBox = QLineEdit()
        self.leadersCountTextBox.setText(str(self.settings.leaders_count))

        self.bitsCountTextBox = QLineEdit()
        self.bitsCountTextBox.setText(str(self.settings.bits_count))

        self.initialBitsTextBox = QLineEdit()
        self.initialBitsTextBox.setText(str(self.settings.initial_bits))

        self.validationSplitTextBox = QLineEdit()
        self.validationSplitTextBox.setText(str(self.settings.validation_split))

   

        ## CONSOLE STUFF
        self.consoleSettingsLayout = QHBoxLayout()
        self.verboseCheckBox = QCheckBox()
        self.verboseCheckBox.setChecked(False)

        self.printSummaryCheckBox = QCheckBox()
        self.printSummaryCheckBox.setChecked(False)
        
        self.consoleSpacer = QSpacerItem(10, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.consoleLayout = QVBoxLayout()
        self.consoleLabel = QLabel("Console output")
        #self.consoleLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.consoleWidget = QWidget()
        self.consoleWidget.setMinimumHeight(150)
        self.consoleWidget.setStyleSheet("background-color: black;")
        self.consoleText = QTextBrowser(self.consoleWidget)
        self.consoleText.setText("This will show console output")
        self.consoleText.setStyleSheet("color: white;")
        

        ## LAYERS SETTINGS
        self.fitnessLabel = QLabel("Current epoch fitness")
        self.fitnessList = QListWidget()
        self.fitnessList.setStyleSheet("background-color: white; border: 1px solid black;")

        self.build_layout()

        print("Build complete")
        self.mainDialog.show()
        sys.exit(self.app.exec_())

    def build_layout(self):

        ## LEFT

        self.visualizationAndProgressLayout.addWidget(self.visualizationLabel, 1)
        self.visualizationAndProgressLayout.addWidget(self.visualizationWidget, 8)

        self.visualizationButtonsLayout.addWidget(self.previousModelButton)
        self.visualizationButtonsLayout.addWidget(self.nextModelButton)

        self.visualizationAndProgressLayout.addLayout(self.visualizationButtonsLayout, 2)

        self.visualizationAndProgressLayout.addWidget(self.progressBar,2)
        self.visualizationAndProgressLayout.addWidget(self.progressBarLabel,1)

        self.buttonsLayout.addWidget(self.startTrainingButton)
        self.buttonsLayout.addWidget(self.testModelButton)

        self.visualizationAndProgressLayout.addLayout(self.buttonsLayout, 2)

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
                description="Mutation rate:",
                tooltip="Chance of evolution, recommended is 1/BITS_COUNT"
            ),
            describedWidget(
                widget=self.babiesCountTextBox,
                description="Babies count:",
                tooltip="TODO enforce specific values"
            ),
            describedWidget(
                widget=self.leadersCountTextBox,
                description="Leaders count:",
                tooltip="TODO enforce specific values"
            ),
            describedWidget(
                widget=self.bitsCountTextBox,
                description="Bits count:",
                tooltip="TODO enforce specific values"
            ),
            describedWidget(
                widget=self.initialBitsTextBox,
                description="Initial bits:",
                tooltip="TODO enforce specific values"
            ),
            describedWidget(
                widget=self.validationSplitTextBox,
                description="Validation split:",
                tooltip="Percentage of images used for validation, 0-0.95"
            )
        ])

        self.configurationAndConsoleLayout.addItem(self.consoleSpacer)
        self.configurationAndConsoleLayout.addWidget(self.consoleLabel, 1)
        self.configurationAndConsoleLayout.addWidget(self.consoleWidget, 3)

        self.addDescribedWidget(parent=self.consoleSettingsLayout, listWidgets=[
            describedWidget(
                widget=self.verboseCheckBox,
                description="Additional verbose:",
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
        
        self.fitnessLayout.addWidget(self.fitnessLabel)
        self.fitnessLayout.addWidget(self.fitnessList,5)

        for i in range(0,20):
            b = format(i,'b').zfill(self.settings.bits_count)
            self.fitnessList.addItem(QListWidgetItem(f"{b}   fitness: {round(randint(0,100)/100,2)}"))

        self.mainLayout.addLayout(self.fitnessLayout, 1)


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