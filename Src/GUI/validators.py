
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


NUMBER_VALIDATOR = QRegExpValidator(QRegExp("^[0-9]+$"))
FRACTION_VALIDATOR = QRegExpValidator(QRegExp("^0.[0-9]+$"))
