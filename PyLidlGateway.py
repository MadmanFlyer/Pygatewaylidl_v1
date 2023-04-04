
#!/usr/bin/python3
# -*-coding:Utf-8 -*

from difflib import Match
import sys,os, time
import platform
from random import randint
import serial,serial.tools.list_ports

#interface import
import PySide6


from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QMessageBox, QWidget, QGridLayout, QTextEdit, QGroupBox, QVBoxLayout,QHBoxLayout, QComboBox, QLabel
#from PySide6.QtWidgets import QApplication, QMainWindow,QDesktopWidget, QTextEdit, QLineEdit, QPushButton, QMessageBox, QWidget, QGridLayout, QTextEdit, QGroupBox, QVBoxLayout,QHBoxLayout, QComboBox, QLabel

from PySide6.QtGui import QIcon, QScreen

__prgm__ = 'Serial Monitor : Lidl (Silvercrest) Smart Home Gateway Flash Process                                MF v1.0'
__version__ = '0.0.1'

def find_USB_device(USB_DEV_NAME=None):
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(myports)
    usb_port_list = [p[0] for p in myports]
    usb_device_list = [p[1] for p in myports]
    print(usb_device_list)

    if USB_DEV_NAME is None:
        return myports
    else:
        USB_DEV_NAME=str(USB_DEV_NAME).replace("'","").replace("b","")
        for device in usb_device_list:
            print("{} -> {}".format(USB_DEV_NAME,device))
            print(USB_DEV_NAME in device)
            if USB_DEV_NAME in device:
                print(device)
                usb_id = device[device.index("COM"):device.index("COM")+4]
            
                print("{} port is {}".format(USB_DEV_NAME,usb_id))
                return usb_id
                
class GroupClass(QGroupBox):
    def __init__(self,widget,title="Connection Configuration"):
        super().__init__(widget)
        self.widget=widget
        self.title=title
        self.sep="-"
        self.id=-1
        self.name=''
        self.portlist=find_USB_device()
        self.items=[p[0] for p in self.portlist]#["COM1","COM2"]
        self.baudlist=["9600","38400","115200"]
        self.itemsb=self.baudlist
        self.actionlist=["Exit soft","Explanation","Gateway connection","Access Bootloader","Get root / password","Backup Flash memory","Flash the gateway"]
        self.itemsa=self.actionlist
        self.itemsb=self.baudlist
        self.serial=None
        #self.motionDict={"POSITION BASED":" Describe motion based on position","VELOCITY BASED":" Describe motion based on velocity", "LOOP":" Describe loop motion", "PINGPONG":" Describe pingpong motion", "INTERACTIF":" Describe interactive motion"}
        self.init()
        
    def init(self):

        self.setTitle(self.title)
        
        
        lb_port = QLabel("Select port :")
        lb_baud = QLabel("Select Bauds rate :")
        lb_op = QLabel("Operation :")
        lb_cmd=  QLabel("Command :")
        lb_mon = QLabel("Monitor :")

        self.CB_port=QComboBox()
        self.CB_port.addItems(self.items)
        self.CB_port.setCurrentIndex(self.CB_port.count()-1)

        self.CB_baud = QComboBox()
        self.CB_baud.addItems(self.itemsb)
        self.CB_baud.setCurrentIndex(self.CB_baud.count()-1)
 
        self.CB_op = QComboBox()
        self.CB_op.addItems(self.itemsa)
        self.CB_op.setCurrentIndex(self.CB_op.count()-1)
        
        #btn
        self.bt_connect = QPushButton("Connect")
        self.bt_connect.clicked.connect(self.connect)
        sendBtn = QPushButton("Send")
        sendBtn.clicked.connect(self.sendData)
        bt_go = QPushButton("Execute")
        bt_go.clicked.connect(self.action)
        self.rem=QPushButton("Delete")
        #self.rem.clicked.connect(self.remItem)
        
        self.le_cmd = QLineEdit("")
        self.te_mon = QTextEdit("")
        
        self.fields=QGridLayout()
        self.fields.addWidget(lb_port,0,0,1,1)
        self.fields.addWidget(lb_baud,0,1,1,1)
        self.fields.addWidget(lb_op,2,0,1,1)
        self.fields.addWidget(lb_cmd,3,0,1,1)
        self.fields.addWidget(lb_mon,4,0,1,1)

        self.fields.addWidget(self.CB_port,1,0,1,1)
        self.fields.addWidget(self.CB_baud,1,1,1,1)
        self.fields.addWidget(self.CB_op,2,1,1,1)

        self.fields.addWidget(self.te_mon,5,0,1,3)

        self.fields.addWidget(self.bt_connect,0,2,1,1)
        
        self.fields.addWidget(self.le_cmd,3,1,1,1)
        self.fields.addWidget(sendBtn,3,2,1,1)
        
        self.fields.addWidget(bt_go,2,2,1,1)
        self.fields.addWidget(self.rem,3,2,1,1)
        self.setLayout(self.fields)
    
    def action(self):
        match self.typeBoxaction.currentIndex() :
            case 0: self.exitsoft()              # Exit soft
            case 1: self.explanation()           # Explanation
            case 2: serial00 = self.connect()    # Gateway Connection
            case 3: self.bootmode(serial00)      # Access Bootloader
            case 4: self.flashsave(serial00)     # Get root / password
            case 5: self.rootpwd(serial00)       # Backup Flash memory
            case 6: self.flashgateway(serial00)  # Flash the gateway
        return True

    def explanation(self):
        
        self.te_mon.setText(self.te_mon.toPlainText()+"\n********** -- Explanation -- **********\n")
        self.te_mon.setText(self.te_mon.toPlainText()+"1 - Connect Gateway to USB/TTL converter (3V3 and +5V of USB/TTL converter is not connected): ")
        self.te_mon.setText(self.te_mon.toPlainText()+"\n\t J1.1-> void \t J1.2-> GND \t J1.3-> RX \t J1.4-> TX \t J1.5-> void \t J1.6-> void \n")
        self.te_mon.setText(self.te_mon.toPlainText()+"2 - The power on is establsh with the microUSB and a +5V power supply")
        return 0

    def logserial(self):
        print("\n********** -- Gateway Connection -- **********\n")
        s = None
        try :
            ports = serial.tools.list_ports.comports(include_links=False)
            if (len(ports) > 0): # on a trouv� au moins un port actif
                print ("Active port(s) found " + str(len(ports)) + " =>", end="\t") 
                nb = 1
                for port in ports :  # affichage du nom de chaque port
                    print(str(nb) + ": " + port.device + "    ")
                    nb = nb + 1
                portIndex = int(input("Serial port index = "))
                print("Baud rate aivalable =>    1: 9600    2: 38400    3: 115200")
                baudrate = int(input("Baud rate index ="))
                match baudrate:
                    case 1: baudrate = 9600
                    case 2: baudrate = 38400
                    case 3: baudrate = 115200
                print("Connection to port %s ..." % ports[portIndex - 1].device)
                # on �tablit la communication s�rie
                con = 0
                portName = str(ports[portIndex - 1].device)
                while con == 0:
                    try :
                        s = serial.Serial(portName, baudrate, timeout=1)
                        #s = serial.Serial('COM6',38400,timeout=0)
                        s.close()
                        s.open()
                        s.setDTR(False)
                        s.setDTR(True)
                        time.sleep(0.05)
                        print("Ports %s Connected" % ports[portIndex - 1].device)
                        con = 1
                    except :
                        val = input("WARNING !!! Serial port %s is busy, try again to connect ? \r\n n[no] or y[yes] : " % ports[portIndex - 1].device)
                        if (val =="n") : 
                            s = None
                            break
        except : print("!!! Error : No connected !!!")
        return s

    def readData0(self):
        #session.flush() # it is buffering. required to get the data out *now*
        answer=[]
        answer = str(s.readline())
        answer = answer.replace("b'\n'","").replace("\n","").replace("b'","").replace("'","")
        return answer   

    def bootmode(self):
        print("\n********** -- Boot mode -- **********\n")
        return 0

    def flashsave(self):
        print("\n********** -- Backup Gateway Flash -- **********\n")
        return 0

    def rootpwd(self):
        print("\n********** -- Get root/password Gateway -- **********\n")
        return 0

    def flashgateway(self):
        print("\n********** -- Flash Gateway -- **********\n")
        return 0

    def exitsoft(self):
        print("\n********** -- Exit software -- **********\n")
        try :
            s.close()
            s.open()
            s.setDTR(False)
            s.setDTR(True)
            s.close()
        except: pass
        print("")
        print("******************************  End ... Goodbye ******************************")
        print("******************************************************************* MF v1.0 **\n")
        sys.exit()

    def connect(self):
        toto = int(0)
        titi = str(self.bt_connect.text())
        if titi == "Connect" : toto = 1
        bool = False
        self.te_mon.setText("\n>> trying to connect to port %s ..." % self.typeBox.currentText())
        #with serial.Serial(self.typeBox.currentText(), 115200, timeout=1) as self.serial:
        if self.serial is None:   
            while not bool :
                try :
                    baud = int(self.typeBoxBaud.currentText())
                    com = str(self.typeBox.currentText())
                    self.serial=serial.Serial(com, baud, timeout=1)
                    time.sleep(0.05)
                    if self.serial.is_open:
                        self.te_mon.setText(self.te_mon.toPlainText()+"\nPorts %s Connected" % self.typeBox.currentText())
                        self.bt_connect.setText("Disconnect")
                        self.serials.setDTR(False)
                        self.serial.setDTR(True)
                        bool = True
                    bool = True
                except :
                    self.te_mon.setText(self.te_mon.toPlainText()+"\nWARNING !!! Serial port %s is busy" % self.typeBox.currentText())
                    break
        else : self.te_mon.setText("\n>> {} already Opened!\n".format(self.typeBox.currentText()))
        return bool
              
    def sendData(self):
        if self.serial.isOpen():
            if self.title.text() != "":
                self.serial.write(self.title.text().encode())
                answer=self.readData()
                if(self.title.text().encode()=="scan"):
                    print("scanning results -> "+answer.find("0x"))
                else:
                    print(answer.find("0x"))
                self.te_mon.setText(self.te_mon.toPlainText()+"\n"+answer)
                    
    def readData(self):
        #self.serial.flush() # it is buffering. required to get the data out *now*
        answer=""
        while  self.serial.inWaiting()>0: #self.serial.readable() and   
            print(self.serial.inWaiting())
            answer += "\n"+str(self.serial.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
        return answer    
    
            
class SerialInterface(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.width=1000
        self.height=500
        
        self.resize(self.width, self.height)
        self.setWindowIcon(QIcon('./resources/logo-100.png'))
        self.setWindowTitle(__prgm__)
        
        #center window on screen
        qr = self.frameGeometry()
        cp = QScreen().availableGeometry().center()
        qr.moveCenter(cp)
        
        
        #init layout
        centralwidget = QWidget(self)
        centralLayout=QHBoxLayout(centralwidget)
        self.setCentralWidget(centralwidget)
        
        #add connect group
        self.connectgrp=GroupClass(self)
        centralLayout.addWidget(self.connectgrp)
        
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = SerialInterface()
    frame.show()
    sys.exit(app.exec_())
