#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QToolTip, QMessageBox, QGridLayout,
        QLabel, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox)
from PyQt5.QtCore import QCoreApplication
from MyPyMata.pymata import PyMata
from functools import wraps
import matplotlib.pyplot as plt

def tryExceptDecorator(moreThenSelf=0):
    def innerTryExceptDecorator(f):
        @wraps(f)
        def inner(*args,**kwargs):
            try:
                if moreThenSelf:
                    return f(*args,**kwargs)
                else:
                    return f(args[0])
            except Exception as e:
                print("Problem with "+f.__name__ + ":")
                print(str(e))
        return inner
    return innerTryExceptDecorator
class Example(QWidget):
        
    def __init__(self):
        super().__init__()
        self.motorVector = {'motor2':0,'motor3':0,'motor6':0,'motor7':0}
        self.port = ""
        self.pedMin = 260
        self.pedMax = 499
        self.board = ""
        self.initUI()

    def initUI(self):
       
        self.generalVBox = QVBoxLayout()
        self.generalVBox.addStretch(1)
        self.grid = QGridLayout()

        # Connecting section
        self.portLabel = QLabel('Port:')
        self.portEdit = QLineEdit("")
        self.portCombo = QComboBox()
        self.portCombo.addItems(["/dev/tty.usbserial-A9CZ7XPL", "/dev/tty.usbmodem1421",])
        self.portEdit.setFixedWidth(200)
        self.connectButton = QPushButton('Connect', self)
        self.connectButton.clicked.connect(self.connectToArduino)

        self.connectHBox = QHBoxLayout()
        self.connectHBox.addStretch(1)

        # Multi-engines setting
        self.modifyPedestalsCheckbox = QCheckBox("Change pedestals values")        

        self.pedestalsLabel = QLabel('Set engines from {} to {}:'.format(self.pedMin, self.pedMax))
        self.pedestalsEdit = QLineEdit("260")
        self.pedestalsEdit.setFixedWidth(50)
        self.pedestalsEdit.setMaxLength(3)
        self.pedestalsButton = QPushButton('Set', self)
        self.pedestalsButton.clicked.connect(self.setPedestals)

        self.pedestalsUpButton = QPushButton('+1', self)
        self.pedestalsDownButton = QPushButton('-1', self)
        self.pedestalsUpButton.clicked.connect(self.setPedestalsUpDown)
        self.pedestalsDownButton.clicked.connect(self.setPedestalsUpDown)
        self.pedestals5UpButton = QPushButton('+5', self)
        self.pedestals5DownButton = QPushButton('-5', self)
        self.pedestals5UpButton.clicked.connect(self.setPedestalsUpDown)
        self.pedestals5DownButton.clicked.connect(self.setPedestalsUpDown)        

        self.pedestalsOneVBox = QVBoxLayout()
        self.pedestalsOneVBox.addStretch(1)

        self.pedestalsFiveVBox = QVBoxLayout()
        self.pedestalsFiveVBox.addStretch(1)

        self.pedestalsHBox = QHBoxLayout()
        self.pedestalsHBox.addStretch(1)

        # Other commands
        self.writeDataLabel = QLabel('Write data:')
        self.writeDataButton = QPushButton('0x13', self)
        self.writeDataButton.clicked.connect(self.writeData)

        self.startCorrectionLabel = QLabel('Start correction:')
        self.startCorrectionButton = QPushButton('0x14', self)
        self.startCorrectionButton.clicked.connect(self.startCorrection)

        self.startCalibrationLabel = QLabel('Calibration:')
        self.startCalibrationButton = QPushButton('0x18', self)
        self.startCalibrationButton.clicked.connect(self.startCalibration)

        self.landingLabel = QLabel('Landing:')
        self.landingButton = QPushButton('0x19', self)
        self.landingButton.clicked.connect(self.landing)

        self.sysexHBox = QHBoxLayout()
        self.sysexHBox.addStretch(1)

        # Single-engine setting
        self.motorValue2 = QLineEdit('0')
        self.motorValue3 = QLineEdit('0')
        self.motorValue6 = QLineEdit('0')
        self.motorValue7 = QLineEdit('0')

        self.plusMotor2 = QPushButton('+1 motor2', self)
        self.plusMotor3 = QPushButton('+1 motor3', self)
        self.plusMotor6 = QPushButton('+1 motor6', self)
        self.plusMotor7 = QPushButton('+1 motor7', self)
        
        self.minusMotor2 = QPushButton('-1 motor2', self)
        self.minusMotor3 = QPushButton('-1 motor3', self)
        self.minusMotor6 = QPushButton('-1 motor6', self)
        self.minusMotor7 = QPushButton('-1 motor7', self)
       
        self.plusMotor2.clicked.connect(self.addOne)
        self.plusMotor3.clicked.connect(self.addOne)
        self.plusMotor6.clicked.connect(self.addOne)
        self.plusMotor7.clicked.connect(self.addOne)

        self.minusMotor2.clicked.connect(self.minusOne)
        self.minusMotor3.clicked.connect(self.minusOne)
        self.minusMotor6.clicked.connect(self.minusOne)
        self.minusMotor7.clicked.connect(self.minusOne)

        # Plots
        self.exampleLabel = QLabel('Example data stored:')
        self.exampleLine = QLineEdit('')
        self.exampleLine.setFixedWidth(300)
        self.exampleButton = QPushButton('Load', self)
        self.exampleButton.clicked.connect(self.extractExample)
        self.plotsLine = QLineEdit('2 4 8')
        self.plotsButton = QPushButton('Show', self)
        self.plotsButton.clicked.connect(self.showPlots)
       
        self.exampleHBox = QHBoxLayout()
        self.exampleHBox.addStretch(1)
        self.plotsHBox = QHBoxLayout()
        self.plotsHBox.addStretch(1)

        #qbtn = QPushButton('Quit', self)
        #qbtn.setToolTip('Click to close the application')
        #qbtn.clicked.connect(QCoreApplication.instance().quit)
        #qbtn.resize(qbtn.sizeHint())
        #qbtn.move(50, 50) 

        self.connectHBox.addWidget(self.portLabel)
        self.connectHBox.addWidget(self.portEdit)
        self.connectHBox.addWidget(self.portCombo)
        self.connectHBox.addWidget(self.connectButton)
        self.generalVBox.addLayout(self.connectHBox)
        
        self.pedestalsHBox.addWidget(self.pedestalsLabel)
        self.pedestalsHBox.addWidget(self.pedestalsEdit)
        self.pedestalsHBox.addWidget(self.pedestalsButton)
        self.pedestalsOneVBox.addWidget(self.pedestalsUpButton)
        self.pedestalsOneVBox.addWidget(self.pedestalsDownButton)
        self.pedestalsFiveVBox.addWidget(self.pedestals5UpButton)
        self.pedestalsFiveVBox.addWidget(self.pedestals5DownButton)

        self.pedestalsHBox.addLayout(self.pedestalsOneVBox)
        self.pedestalsHBox.addLayout(self.pedestalsFiveVBox) 
        self.generalVBox.addWidget(self.modifyPedestalsCheckbox)
        self.generalVBox.addLayout(self.pedestalsHBox)

        self.sysexHBox.addWidget(self.writeDataLabel)
        self.sysexHBox.addWidget(self.writeDataButton)
        self.sysexHBox.addWidget(self.startCorrectionLabel)
        self.sysexHBox.addWidget(self.startCorrectionButton)
        self.sysexHBox.addWidget(self.startCalibrationLabel)
        self.sysexHBox.addWidget(self.startCalibrationButton)
        self.sysexHBox.addWidget(self.landingLabel)
        self.sysexHBox.addWidget(self.landingButton)
        self.generalVBox.addLayout(self.sysexHBox)

        self.grid.addWidget(self.plusMotor2, 1, 0)
        self.grid.addWidget(self.plusMotor3, 1, 1)
        self.grid.addWidget(self.plusMotor6, 1, 2)
        self.grid.addWidget(self.plusMotor7, 1, 3)

        self.grid.addWidget(self.minusMotor2, 2, 0)
        self.grid.addWidget(self.minusMotor3, 2, 1)
        self.grid.addWidget(self.minusMotor6, 2, 2)
        self.grid.addWidget(self.minusMotor7, 2, 3)

        self.grid.addWidget(self.motorValue2, 3, 0)
        self.grid.addWidget(self.motorValue3, 3, 1)
        self.grid.addWidget(self.motorValue6, 3, 2)
        self.grid.addWidget(self.motorValue7, 3, 3)

        self.generalVBox.addLayout(self.grid)

        self.exampleHBox.addWidget(self.exampleLabel)
        self.exampleHBox.addWidget(self.exampleLine)
        self.exampleHBox.addWidget(self.exampleButton)
        self.generalVBox.addLayout(self.exampleHBox)
        self.plotsHBox.addWidget(self.plotsLine)
        self.plotsHBox.addWidget(self.plotsButton)
        self.generalVBox.addLayout(self.plotsHBox)

        self.setLayout(self.generalVBox)
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('My app')
        self.show()

    @tryExceptDecorator(0)
    def connectToArduino(self):
        self.port = str(self.portEdit.text())
        if self.port == "":
            self.port = self.portCombo.currentText()
        print("Connecting to: {}".format(self.port))

        self.board = PyMata(self.port)
        self.board.set_pin_mode(2,self.board.PWM,self.board.DIGITAL)
        self.board.set_pin_mode(3,self.board.PWM,self.board.DIGITAL)
        self.board.set_pin_mode(6,self.board.PWM,self.board.DIGITAL)
        self.board.set_pin_mode(7,self.board.PWM,self.board.DIGITAL)

    @tryExceptDecorator(0)
    def setPedestals(self):
        tempPedestal = 0
        try:
            tempPedestal = int(self.pedestalsEdit.text())
        except:
            print("Bad conversion to int")
            return
        if tempPedestal > 259 and tempPedestal < 500:
            print("Setting all pedestals to: {}".format(str(tempPedestal)))
            for key in self.motorVector.keys():
                self.motorVector[key] = tempPedestal
            self.updateTexts()
            if(self.modifyPedestalsCheckbox.isChecked()):
                self.board.send_single_pedestal(tempPedestal)
            else:
                self.board.send_single_value(tempPedestal)
        else:
            print("Pedestals out of range")

    @tryExceptDecorator(0)
    def writeData(self):
        print("Send write data sysex")
        self.board._command_handler.send_sysex(0x13)

    @tryExceptDecorator(0)
    def startCorrection(self):
        print("Send auto correction sysex")
        self.board._command_handler.send_sysex(0x14)

    @tryExceptDecorator(0)
    def startCalibration(self):
        print("Send calibration sysex")
        self.board._command_handler.send_sysex(0x18)

    @tryExceptDecorator(0)
    def landing(self):
        print("Send landing sysex")
        self.board._command_handler.send_sysex(0x19)

    @tryExceptDecorator(0)
    def addOne(self):
        sender = self.sender()
        for key in self.motorVector.keys():
            if key in sender.text():
                print("addOne in " + key)
                if self.motorVector[key] + 1 > self.pedMax:
                    print("Out of range")
                else:
                    self.motorVector[key] += 1
                    self.updateTexts()
                    if(self.modifyPedestalsCheckbox.isChecked()):
                        self.board.send_pedestal_motor(int(key[-1:]),self.motorVector[key])
                    else:
                        self.board.send_single_motor(int(key[-1:]),self.motorVector[key])

    @tryExceptDecorator(0)
    def minusOne(self):
        sender = self.sender()
        for key in self.motorVector.keys():
            if key in sender.text():
                print("minusOne in " + key)
                if self.motorVector[key] - 1 < self.pedMin:
                    print("Out of range")
                else:
                    self.motorVector[key] -= 1
                    self.updateTexts()
                    if(self.modifyPedestalsCheckbox.isChecked()):
                        self.board.send_pedestal_motor(int(key[-1:]),self.motorVector[key])
                    else:
                        self.board.send_single_motor(int(key[-1:]),self.motorVector[key])    
                    
    @tryExceptDecorator(0)
    def setPedestalsUpDown(self):
        sender = self.sender()
        senderTextInt = int(sender.text())
        print("All pedestals",sender.text())
        for key in self.motorVector.keys():
            if self.motorVector[key] + (senderTextInt) > self.pedMax or self.motorVector[key] + (senderTextInt) < self.pedMin:
                print("Out of range")
            else:
                self.motorVector[key] = self.motorVector[key] + (senderTextInt)
                if(self.modifyPedestalsCheckbox.isChecked()):
                    self.board.send_pedestal_motor(int(key[-1:]),self.motorVector[key])
                else:
                    self.board.send_single_motor(int(key[-1:]),self.motorVector[key])
        self.updateTexts()

    @tryExceptDecorator(0)
    def updateTexts(self):
        self.motorValue2.setText(str(self.motorVector['motor2']))
        self.motorValue3.setText(str(self.motorVector['motor3']))
        self.motorValue6.setText(str(self.motorVector['motor6']))
        self.motorValue7.setText(str(self.motorVector['motor7']))

    @tryExceptDecorator(0)
    def showPlots(self):
        plotsString = str(self.plotsLine.text()).split()
        print(plotsString)
        data = [[ x[i] for x in self.board.graph_data ] for i in range(len(self.board.graph_data[0]))]
        for element in plotsString:
            plt.plot(data[int(element)])
        plt.show()
        
    @tryExceptDecorator(0)
    def extractExample(self):
        if(len(self.board.graph_data) > 0 ):
            print("First entry in data:")
            print(self.board.graph_data[0])
            self.exampleLine.setText(str(self.board.graph_data[0]))
        else:
            print("No data available!!!")

        
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
