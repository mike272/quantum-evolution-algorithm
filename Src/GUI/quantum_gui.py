from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QFrame, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QLabel,
                             QPushButton,QSpinBox, QDialog, QLineEdit,
                             QCheckBox, QDialogButtonBox, QWidget, QProgressBar,
                             QListView, QTextBrowser, QApplication, QSpacerItem,
                             QSizePolicy, QListWidget, QListWidgetItem, QGroupBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import sys
from random import randint
from Src.GUI.stylesheets import *

from Src.settings import Settings

class describedWidget:
    def __init__(self, widget:QWidget, description="", tooltip=""):
        self.widget = widget
        self.description = description
        self.tooltip = tooltip

class QuantumGUI(object):
    visualizationLayout:QVBoxLayout

    progressBar:QProgressBar
    progressBarLabel:QLabel

    startEvolutionButton:QPushButton
    startVisualizationButton:QPushButton

    configurationLayout:QVBoxLayout

    epochsTextBox:QLineEdit
    mutationRateTextBox:QLineEdit
    babiesCountTextBox:QLineEdit
    leadersCountTextBox:QLineEdit
    bitsCountTextBox:QLineEdit
    initialBitsTextBox:QLineEdit
    verboseCheckBox:QCheckBox

    fitnessLayout:QVBoxLayout


    fitnessLabel:QLabel
    fitnessList:QWidget

    previousEpochButton:QPushButton
    nextEpochButton:QPushButton

    def __init__(self, settings:Settings):

        self.settings = settings

        self.app = QApplication(sys.argv)

        self.mainDialog = QDialog()
        self.mainDialog.setWindowTitle("Quantum Evolution GUI")
        self.mainDialog.setWindowModality(Qt.NonModal)
        self.mainDialog.setMinimumSize(800, 500)
        self.mainLayout = QHBoxLayout(self.mainDialog)

        self.buildVisualizationLayout()
        self.buildConfigurationLayout()
        self.buildFitnessLayout()

        self.mainDialog.show()
        self.app.exec_()

    def buildVisualizationLayout(self):
        self.visualizationLayout = QVBoxLayout()

        self.buildPlotWidget()
        self.buildProgressBar()
        self.buildTrainingButtons()

        self.mainLayout.addLayout(self.visualizationLayout, 2)
        
    def buildConfigurationLayout(self):
        self.configurationLayout = QVBoxLayout()

        self.buildConfigurationFields()

        self.mainLayout.addLayout(self.configurationLayout, 1)

    def buildFitnessLayout(self):
        self.fitnessLayout = QVBoxLayout()
        
        self.buildFitnessList()
        self.buildFitnessButtons()

        self.mainLayout.addLayout(self.fitnessLayout, 1)


    def buildPlotWidget(self):

        visualizationWidget = QGroupBox()
        visualizationWidget.setStyleSheet(VISUALIZATION_PANEL_STYLESHEET)

        plotLayout = QVBoxLayout()
        plotLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        visualizationWidget.setLayout(plotLayout)   

        self.figure = plt.figure(figsize=(8,8))
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, None)
        toolbar.setStyleSheet(TOOLBAR_STYLESHEET)

        plotLayout.addWidget(toolbar)
        plotLayout.addWidget(self.canvas)

        self.visualizationLayout.addWidget(visualizationWidget, 8)

    def buildProgressBar(self):
        self.progressBar = QProgressBar(minimum = 0, maximum = 100, value = 10)

        self.progressBarLabel = QLabel("This will describe what is happening right now\n(What process is running)")

        self.visualizationLayout.addWidget(self.progressBar,2)
        self.visualizationLayout.addWidget(self.progressBarLabel,1)

    def buildTrainingButtons(self):
        buttonsLayout = QHBoxLayout()

        self.startEvolutionButton = QPushButton("Start evolution")
        self.startEvolutionButton.clicked.connect(self.startTraining)

        self.startVisualizationButton = QPushButton("Start visualization")
        self.startVisualizationButton.clicked.connect(self.testModel)

        buttonsLayout.addWidget(self.startEvolutionButton)
        buttonsLayout.addWidget(self.startVisualizationButton)

        self.visualizationLayout.addLayout(buttonsLayout, 1)

    def buildConfigurationFields(self):
        self.epochsTextBox = QLineEdit()
        self.epochsTextBox.setText(str(self.settings.epochs))

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

        self.floatsPrecisionTextBox = QLineEdit()
        self.floatsPrecisionTextBox.setText(str(self.settings.initial_bits))

        self.verboseCheckBox = QCheckBox()
        self.verboseCheckBox.setChecked(False)

        self.addDescribedWidget(parent=self.configurationLayout, listWidgets=[
            describedWidget(
                widget=self.epochsTextBox,
                description="Epochs:",
                tooltip="Number of epochs, must be an int"
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
                widget=self.floatsPrecisionTextBox,
                description="Float precision:",
                tooltip="TODO enforce specific values"
            ),
            describedWidget(
                widget=self.verboseCheckBox,
                description="Additional verbose:",
                tooltip="TODO"
            ),
        ])


    def buildFitnessList(self):
        self.fitnessLabel = QLabel("Current epoch fitness (x/x)")

        self.fitnessList = QListWidget()
        self.fitnessList.setStyleSheet("background-color: white; border: 1px solid black;")

        self.fitnessLayout.addWidget(self.fitnessLabel)
        self.fitnessLayout.addWidget(self.fitnessList,5)

        for i in range(0,200):
            b = format(i,'b').zfill(self.settings.bits_count)
            self.fitnessList.addItem(QListWidgetItem(f"{b}   fitness: {round(randint(0,100)/100,2)}"))

    def buildFitnessButtons(self):
        fitnessButtonsLayout = QHBoxLayout()

        self.previousEpochButton = QPushButton("Previous")
        self.previousEpochButton.clicked.connect(self.startTraining)

        self.nextEpochButton = QPushButton("Next")
        self.nextEpochButton.clicked.connect(self.testModel)

        fitnessButtonsLayout.addWidget(self.previousEpochButton,1)
        fitnessButtonsLayout.addWidget(self.nextEpochButton,1)

        self.fitnessLayout.addLayout(fitnessButtonsLayout)

    def loadModel(self):
        pass

    def testModel(self):
        pass

    def startTraining(self):
        pass
        
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