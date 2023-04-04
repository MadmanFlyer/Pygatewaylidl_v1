##############################################

from pyclbr import Function
import sys
import threading
#from tkinter import END
#from turtle import down
import serial
import serial.tools.list_ports
import time

import Pydecode_AES as AES

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout,QStatusBar,QMainWindow,QWidget)

from PySide6.QtGui import QIcon, QScreen,QActionEvent



__prgm__ = 'Serial Monitor : Lidl (Silvercrest) Smart Home Gateway Flash Process                                MF v1.0'
__version__ = '0.0.1'
__baudrate__ = ["75","110","134","150","300","600","1200","1800","2400","4800","7200","9600","14400","19200","38400","57600","115200","128000"]
__bytesize__ = ["5","6","7","8"]
__parity__ = ["None","Even", "Odd", "Mark","Space"]
__stopbit__ = ["1","1.5","2"]
__flux__ = ["Software Xon / Xoff", "Hardware RTS/CTS", "Hardware DSR/DTR"]
__Dyn__ = True


class Dialog(QDialog):
    #num_grid_rows = 3
    #num_buttons = 4

    def __init__(self):
        super().__init__()

        self._dyn = True
        self.create_menu()
        self.create_gpbox_Serial()
        self.create_gpbox_DispInfo()
        self.create_gpbox_DispSerial()
        self.create_gpbox_KeyDecode()
        self.varprint = ""

        #self.thread_ser = ThreadCom()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.setMenuBar(self._menu_bar)
        main_layout.addWidget(self._gpbox_Serial)
        main_layout.addWidget(self._gpbox_DispInfo)
        main_layout.addWidget(self._gpbox_DispSerial)
        main_layout.addWidget(self._gpbox_KeyDecode)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("Basic Layouts")
        self.refresh()
        
        self.auto = False
        print("SubFrame Interface initialized")

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("Menu", self)
        self._refresh_action = self._file_menu.addAction("Refresh")
        self._tyty_action = self._file_menu.addAction("tyty")
        self._tutu_action = self._file_menu.addAction("tutu")
        self._titi_action = self._file_menu.addAction("titi")
        self._toto_action = self._file_menu.addAction("toto")
        self._exit_action = self._file_menu.addAction("Exit")
        self._file_help = QMenu("Help", self)
        self._help_action = self._file_help.addAction("help")
        self._menu_bar.addMenu(self._file_menu)
        self._menu_bar.addMenu(self._file_help)

        self._exit_action.triggered.connect(self.accept)
        self._refresh_action.triggered.connect(self.refresh)
        self._help_action.triggered.connect(self.menu_help)

    def create_gpbox_Serial(self):
        self._gpbox_Serial = QGroupBox("Connexion parameters")
        self.layout_Serial = QGridLayout()

        lb_ser_port = QLabel("Port")
        lb_ser_baudrate = QLabel("Bauds rate")
        lb_ser_bytesize = QLabel("Byte syze")
        lb_ser_parity= QLabel("Parity")
        lb_ser_stopbits = QLabel("Stop Bits")
        lb_ser_flux = QLabel("Controle Flux")
        

        self.layout_Serial.addWidget(lb_ser_port,0,0,1,1)
        self.layout_Serial.addWidget(lb_ser_baudrate,0,1,1,1)
        self.layout_Serial.addWidget(lb_ser_bytesize,0,2,1,1)
        self.layout_Serial.addWidget(lb_ser_parity,0,3,1,1)
        self.layout_Serial.addWidget(lb_ser_stopbits,0,4,1,1)
        self.layout_Serial.addWidget(lb_ser_flux,0,5,1,1)
        
        self.bt_ser_connect = QPushButton("Connect")
        self.bt_ser_connect.clicked.connect(self.ser_connect)

        self.cb_ser_port = QComboBox()
        self.cb_ser_port.addItems("")
        #self.cb_ser_port.setCurrentIndex(self.cb_ser_port.count()-1)

        self.cb_ser_baudrate = QComboBox()
        self.cb_ser_baudrate.addItems(__baudrate__)
        #self.cb_ser_baudrate.setCurrentIndex(self.cb_ser_baudrate.count()-1)

        self.cb_ser_bytesize = QComboBox()
        self.cb_ser_bytesize.addItems(__bytesize__)
        #self.cb_ser_bytesize.setCurrentIndex(self.cb_ser_stopbits.count()-1)
 
        self.cb_ser_parity = QComboBox()
        self.cb_ser_parity.addItems(__parity__)
        #self.cb_ser_parity.setCurrentIndex(self.cb_ser_parity.count()-1)

        self.cb_ser_stopbits = QComboBox()
        self.cb_ser_stopbits.addItems(__stopbit__)
        #self.cb_ser_stopbits.setCurrentIndex(self.cb_ser_stopbits.count()-1)

        self.cb_ser_flux = QComboBox()
        self.cb_ser_flux.addItems(__flux__)
        #self.cb_ser_flux.setCurrentIndex(self.cb_ser_flux.count()-1)

        self.layout_Serial.addWidget(self.cb_ser_port,1,0,1,1)
        self.layout_Serial.addWidget(self.cb_ser_baudrate,1,1,1,1)
        self.layout_Serial.addWidget(self.cb_ser_bytesize,1,2,1,1)
        self.layout_Serial.addWidget(self.cb_ser_parity,1,3,1,1)
        self.layout_Serial.addWidget(self.cb_ser_stopbits,1,4,1,1)
        self.layout_Serial.addWidget(self.cb_ser_flux,1,5,1,1)
        self.layout_Serial.addWidget(self.bt_ser_connect,1,6,1,1)

                
        def update_port(self):
            if self._dyn and self.cb_ser_port.currentText() !='' :
                self.port = str(self.cb_ser_port.currentText())
                self.cb_ser_baudrate.clear()
                self.cb_ser_parity.clear()
                self.cb_ser_stopbits.clear()
                self.cb_ser_flux.clear()
                s = serial.Serial(self.cb_ser_port.currentText())
                self.cb_ser_baudrate.addItems(list(map(str,s.BAUDRATES)))
                self.cb_ser_bytesize.addItems(list(map(str,s.BYTESIZES)))
                for parity in list(map(str,s.PARITIES)):
                    match parity :
                        case 'N': 
                            p = 0
                            break
                        case 'E': 
                            p = 1
                            break
                        case 'O': 
                            p = 2
                            break
                        case 'M': 
                            p = 3
                            break
                        case 'S':
                            p = 4
                            break
                self.cb_ser_parity.addItem(__parity__[p])
                self.cb_ser_stopbits.addItems(list(map(str,s.STOPBITS)))
                s.close()
                self.cb_ser_flux.addItems(__flux__)
        def update_baudrate(self):
            try : self.baudrate = int(self.cb_ser_baudrate.currentText())
            except : pass
        def update_bytesize(self):
            try : self.bytesize = float(self.cb_ser_bytesize.currentText())
            except : pass
        def update_parity(self):
            try:
                self.parity = ""
                n = 0
                while (self.cb_ser_parity.currentText() != __parity__[n]) and (n <= self.cb_ser_parity.maxCount()): n += 1 
                if self.cb_ser_parity.currentText() == __parity__[n] :
                    #toto = self.cb_ser_parity.currentText()
                    match n :
                        case 0 : self.parity = 'N'
                        case 1 : self.parity = 'E'
                        case 2 : self.parity = 'O'
                        case 3 : self.parity = 'M'
                        case 4 : self.parity = 'S'
            except : pass
        def update_stopbits(self):
            try : self.stopbits = float(self.cb_ser_stopbits.currentText())
            except : pass
        def update_flux(self):
            try:
                self.xonxoff = False
                self.rtscts = False
                self.dsrdtr = False
                n = 0
                #tutu = self.cb_ser_flux.currentText()
                while (self.cb_ser_flux.currentText() != __flux__[n]) and (n <= self.cb_ser_flux.maxCount()): n += 1
                if self.cb_ser_flux.currentText() == __flux__[n] :
                    match n :
                        case 0 : self.xonxoff = True
                        case 1 : self.rtscts = True
                        case 2 : self.dsrdtr = True
            except : pass

        self.cb_ser_port.currentIndexChanged.connect(update_port)
        self.cb_ser_bytesize.currentIndexChanged.connect(update_bytesize)
        self.cb_ser_baudrate.currentIndexChanged.connect(update_baudrate)
        self.cb_ser_parity.currentIndexChanged.connect(update_parity)
        self.cb_ser_stopbits.currentIndexChanged.connect(update_stopbits)
        self.cb_ser_flux.currentIndexChanged.connect(update_flux)

        self._gpbox_Serial.setLayout(self.layout_Serial)

    def create_gpbox_DispInfo(self):
        self._gpbox_DispInfo = QGroupBox("Out monitor")
        layout_DispInfo = QGridLayout()

        #for i in range(Dialog.num_grid_rows):
        #    label = QLabel(f"Line {i + 1}:")
        #    line_edit = QLineEdit()
        #    layout.addWidget(label, i + 1, 0)
        #    layout.addWidget(line_edit, i + 1, 1)

        self.qte_dispinfo = QTextEdit()
        self.qte_dispinfo.setPlainText("")
        self.qte_dispinfo.setReadOnly(True)
        layout_DispInfo.addWidget(self.qte_dispinfo, 0, 0, 4, 4)

        bt_dispinfo_del = QPushButton("delete")
        bt_dispinfo_del.clicked.connect(self.qte_dispinfo.clear)
        layout_DispInfo.addWidget(bt_dispinfo_del, 5, 3, 1, 1)

        layout_DispInfo.setColumnStretch(1, 10)
        self._gpbox_DispInfo.setLayout(layout_DispInfo)

    def printInfo(self,arg="",end='\n'):
        self.qte_dispinfo.setPlainText(self.qte_dispinfo.toPlainText()+arg+end)
        cursor = self.qte_dispinfo.textCursor()
        self.qte_dispinfo.moveCursor(cursor.MoveOperation.End)
        self.qte_dispinfo.repaint()

    def create_gpbox_DispSerial(self):

        self._gpbox_DispSerial = QGroupBox("Serial Monitor")
        layout_DispSerial = QGridLayout()

        self.qte_dispserial = QTextEdit()
        self.qte_dispserial.setPlainText("")
        self.qte_dispserial.setReadOnly(True)
        layout_DispSerial.addWidget(self.qte_dispserial, 0, 0, 5, 5)


        self.bt_ser_read = QPushButton("Read")
        self.bt_ser_read.clicked.connect(self.ser_read)
        layout_DispSerial.addWidget(self.bt_ser_read, 5, 0, 1, 1)

        self.bt_ser_write = QPushButton("Write")
        self.bt_ser_write.clicked.connect(self.ser_write)
        layout_DispSerial.addWidget(self.bt_ser_write, 5, 2, 1, 1)

        self.bt_ser_auto = QPushButton("Auto")
        self.bt_ser_auto.clicked.connect(self.ser_auto)
        layout_DispSerial.addWidget(self.bt_ser_auto, 5, 1, 1, 1)

        bt_dispserial_del = QPushButton("delete")
        bt_dispserial_del.clicked.connect(self.qte_dispserial.clear)
        layout_DispSerial.addWidget(bt_dispserial_del, 5, 4, 1, 1)

        layout_DispSerial.setColumnStretch(0, 10)
        layout_DispSerial.setColumnStretch(1, 10)
        layout_DispSerial.setColumnStretch(2, 10)
        layout_DispSerial.setColumnStretch(3, 2000)
        layout_DispSerial.setColumnStretch(4, 10)
        self._gpbox_DispSerial.setLayout(layout_DispSerial)

    def printSerial(self,arg="",end='\n'):
        self.qte_dispserial.setPlainText(self.qte_dispserial.toPlainText()+arg+end)
        cursor = self.qte_dispserial.textCursor()
        self.qte_dispserial.moveCursor(cursor.MoveOperation.End)
        self.qte_dispserial.repaint()
        test = "Sending discover...\n"
        test += test
        if self.qte_dispserial.toPlainText().find(test) != -1 :
            self.auto = False

    def ser_read(self):
        #s = serial.Serial("COM6", 38400, timeout=1)
        #session.flush() # it is buffering. required to get the data out *now*
        answer=[]
        answer = self.ser.get_data()
        answer = answer.decode('utf-8',errors = 'ignore')
        #answer = answer.replace("b'","")
        answer = answer.replace("\r","")
        #answer = answer.replace("\\n","\n")
        #answer = answer.replace("'","")
        #answer += "\n"
        if answer != '' : self.printSerial(answer,end="") 

    def ser_write(self):
        return 0

    def menu_help(self):
        self.printInfo("********** -- Explanation -- **********")
        self.printInfo("1 - Open the Gateway")
        self.printInfo("2 - Plug Gateway to USB/TTL converter (3V3 and +5V of USB/TTL converter is not connected)")
        self.printInfo("\t J1.1-> void \t J1.2-> GND \t J1.3-> RX \t J1.4-> TX \t J1.5-> void \t J1.6-> void")
        self.printInfo("3 - Connect the Gateway to COMx with 38400bps 8N1 XonXoff")
        self.printInfo("4 - Plug the microUSB Gateway to the power suplly (USB +5V)")
        self.printInfo("2 - The power on is establsh with the microUSB and a +5V power supply")

    def refresh(self):
        self.printInfo("Refresh ports list... => ",end = "")
        try :
            self.ports = serial.tools.list_ports.comports(include_links=False)
            self.cb_ser_port.clear()
            if (len(self.ports) > 0): # There is %s port(s) found
                self.printInfo ("There is %s port(s) found : "  % len(self.ports))
                self._dyn = True
                for port in self.ports :  # scan each port
                    self.cb_ser_port.addItem(str(port.device))
                    self.printInfo("  - " + str(port.device) + ' = ' + str(port.description))
                    self.cb_ser_port.setCurrentIndex(0)
                    self._dyn = False
        except : self.printInfo("!!! Error : No port !!!")
        self._dyn = True

    def ser_connect(self):
        if self.bt_ser_connect.text() == "Connect":
            self.printInfo("%s : connexion...  =>" % str(self.port), end = '\t')
            self.ser = SerialCom()
            d = self.ser.connect(port = str(self.port),
                                    baudrate = int(self.baudrate),
                                    bytesize = int(self.bytesize),
                                    parity = str(self.parity),
                                    stopbit = float(self.stopbits),
                                    xonxoff = bool(self.xonxoff),
                                    rtscts = bool(self.rtscts),
                                    dsrdtr = bool(self.dsrdtr),
                                    timeout = 1)
            match d :
                case -1 : self.printInfo("error : serial port is busy")
                case 0 : self.printInfo("error : threadCom is locked")
                case 1 : self.printInfo("connected")

        elif self.bt_ser_connect.text() == "Disconnect":
            try :
                self.printInfo("%s : disconnexion...  =>" % self.ser.status().port, end = '\t')
                d = self.ser.disconnect()
                match d:
                    case -2 : self.printInfo("error : no existing connection")
                    case -1 : self.printInfo("error during disconnection")
                    case 0 : self.printInfo("error : threadCom is locked")
                    case 1 : self.printInfo("disconnected")
                    case 2 : self.printInfo("aldready disconnected")
            except : self.printInfo("error during disconnection")

        if self.ser.status().isOpen() :
            self.thread_rxData = Thread_GET(self.ser.listen_rxData,self.get_auto,self.ser_read,0.0001)#Thread_timer(0.000001,self.listen_rxData)#,['Repeating'])
            self.thread_rxData.start()
            self.bt_ser_connect.setText("Disconnect")
        else : 
            self.thread_rxData.thr_stop()
            self.bt_ser_connect.setText("Connect")

    def ser_auto(self):
        self.auto = not self.auto
        while self.auto:
            #s = serial.Serial("COM6", 38400, timeout=1)
            #session.flush() # it is buffering. required to get the data out *now*
            answer=[]
            answer = self.ser.get_data()
            answer = answer.decode('utf-8',errors='ignore')
            #answer = answer.replace("b'","")
            answer = answer.replace("\r","")
            #answer = answer.replace("\\n","\n")
            #answer = answer.replace("'","")
            #answer += "\n"
            if answer != '' :
                self.printSerial(answer,end="")
                time.sleep(0.1)
            else : time.sleep(0.5)
 
    def get_auto(self):
        return self.auto

    def create_gpbox_KeyDecode(self):
    
        self._gpbox_KeyDecode = QGroupBox("Key Decode")
        layout_KeyDecode = QGridLayout()

        def Decode():
            kek_str = ""
            auskey_str = ["",""]
            kek_str = self.qle_KD_kek_str.displayText()
            auskey_str[0] = self.qle_KD_auskey_str1.displayText()
            auskey_str[1] = self.qle_KD_auskey_str2.displayText()

        def DispClear():
            self.qle_KD_kek_str.clear()
            self.qle_KD_auskey_str1.clear()
            self.qle_KD_auskey_str2.clear()
            self.qle_KD_auskey.clear()
            self.qle_KD_rootpass.clear()

        lb_KD_kek = QLabel("KEK : ")
        lb_KD_auskey1 = QLabel("AUSKEY line 1 : ")
        lb_KD_auskey2 = QLabel("AUSKEY line 2 : ")
        lb_KD_Rootname= QLabel("Root name = ")
        lb_KD_Rootpass = QLabel("Root pass = ")
        
        layout_KeyDecode.addWidget(lb_KD_kek,0,0,1,1)
        layout_KeyDecode.addWidget(lb_KD_auskey1,1,0,1,1)
        layout_KeyDecode.addWidget(lb_KD_auskey2,2,0,1,1)
        layout_KeyDecode.addWidget(lb_KD_Rootname,3,0,1,1)
        layout_KeyDecode.addWidget(lb_KD_Rootpass,4,0,1,1)

        #KEK hex string line
        self.qle_KD_kek_str = QLineEdit()
        self.qle_KD_kek_str.setText("")
        layout_KeyDecode.addWidget(self.qle_KD_kek_str, 0, 1, 1, 4)

        #Encoded aus-key as hex string line 1
        self.qle_KD_auskey_str1 = QLineEdit()
        self.qle_KD_auskey_str1.setText("")
        layout_KeyDecode.addWidget(self.qle_KD_auskey_str1, 1, 1, 1, 4)

        #Encoded aus-key as hex string line 2
        self.qle_KD_auskey_str2 = QLineEdit()
        self.qle_KD_auskey_str2.setText("")
        layout_KeyDecode.addWidget(self.qle_KD_auskey_str2, 2, 1, 1, 4)

        #Display Auskey
        self.qle_KD_auskey = QLineEdit()
        self.qle_KD_auskey.setText("")
        layout_KeyDecode.addWidget(self.qle_KD_auskey, 3, 1, 1, 4)

        #Display Root password
        self.qle_KD_rootpass = QLineEdit()
        self.qle_KD_rootpass.setText("")
        layout_KeyDecode.addWidget(self.qle_KD_rootpass, 4, 1, 1, 4)

        bt_KD_decode = QPushButton("decode")
        bt_KD_decode.clicked.connect(Decode)
        layout_KeyDecode.addWidget(bt_KD_decode, 0, 5, 1, 1)

        bt_KD_del = QPushButton("delete")
        bt_KD_del.clicked.connect(DispClear())
        layout_KeyDecode.addWidget(bt_KD_del, 1, 5, 1, 1)

        #layout_KeyDecode.setColumnStretch(0, 10)
        #layout_KeyDecode.setColumnStretch(1, 10)
        #layout_KeyDecode.setColumnStretch(2, 10)
        #layout_KeyDecode.setColumnStretch(3, 2000)
        #layout_KeyDecode.setColumnStretch(4, 10)
        self._gpbox_KeyDecode.setLayout(layout_KeyDecode)


class SerialCom():

    def __init__(self):
        self.rx_data = b''
        self.ser = None
        self.lock = threading.Lock()

    def status(self):
        return self.ser

    def getopen(self):
        if not self.port.isOpen() :
            self.port.open()

    def getclose(self):
        self.port.close()

    def connect(self, port = "", baudrate = 0, bytesize = 0,
                 parity = '', stopbit = 0, xonxoff = False, rtscts = False,
                 dsrdtr = False, timeout = 0):
        i = 0
        if self.lock.acquire(blocking = True , timeout = 1): 
            try :
                print("Connexion to " + port + "... =>",end="\t")
                with serial.Serial() as self.ser:
                    self.ser.port = port
                    self.ser.baudrate = baudrate
                    self.ser.bytesize = bytesize
                    self.ser.parity = parity
                    self.ser.stopbit = stopbit
                    self.ser.xonxoff = xonxoff
                    self.ser.setRTS = rtscts
                    self.ser.setDTR = dsrdtr
                    self.ser.timeout = timeout
                #time.sleep(0.05)
                self.ser.close()
                self.ser.open()
                print("connected")
                i = 1
            except :
                i = -1
                print("error : serial port is busy")
            self.lock.release()
        else :
            i = 0
            print("error : threadCom is locked")
        #if(i == 1) : 
        #        self.thread_rxData = Thread_GET(self.listen_rxData,0.0001)#Thread_timer(0.000001,self.listen_rxData)#,['Repeating'])
        #        self.thread_rxData.start()
        return i

    def disconnect(self):
        i = 0
        if self.lock.acquire(blocking = True , timeout = 1):
            try : 
                print("Disconnect from " + self.ser.port + "... =>",end="\t")
                if self.ser !=None :
                    i = 1
                    if self.ser.isOpen() :
                        self.ser.close()
                        while self.ser.isOpen() :
                            time.sleep(0.001)
                        print("disconnected")
                        #self.thread_rxData.thr_stop()
                    else : 
                        i = 2
                        print("aldready disconnected")
                else :
                    i = -2
                    print("error : no existing connection")
            except :
                i = -1
                print("error during disconnection")
            self.lock.release()
        else : 
            i = 0
            print("error : threadCom is locked")
        return i

    def listen_rxData(self):
        if self.lock.acquire(blocking = True, timeout = 1) :
            try :
                if self.ser.isOpen and self.ser.inWaiting()>0 :
                    rx_data = self.ser.read(1)
                    self.rx_data += rx_data
                    #print(self.rx_data)
            except: pass
            self.lock.release()

    def get_data(self):
        if self.lock.acquire(blocking = True, timeout = 1):
            data = self.rx_data
            self.rx_data = b""
            self.lock.release()
        return data

    def send_data(self, *data):
        r =self.port.write(data)
        return r

class Thread_timer(threading.Timer):
 
    #def __init__(self):
    #    super().__init__(self)
    #    print("ThreadCom initialized")
    
    def run(self):
        print("ThreadTimer Started %s :" % self.getName)
        while not self.finished.wait(self.interval):
             self.function()
 
    def stop(self):
        self.cancel()  # pour terminer une eventuelle attente en cours de Timer
        print("ThreadTimer Stopped")

class Thread_GET(threading.Thread):

    def __init__(self,function1,function2,function3,interval):
        super(Thread_GET,self).__init__()
        self.function1 = function1
        self.function2 = function2
        self.function3 = function3
        self.interval = interval
        self.stop = False
        print("ThreadCom initialized")

    def run(self):
        print("ThreadGET Started")
        while not self.stop :#not Dialog.ser_auto_status:
            self.function1()
            #if self.function2():
            #    self.function3()
            time.sleep(self.interval)
        print("ThreadGET Stopped")

    def thr_stop(self):
        self.stop = True # pour termine
        

class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()
        self.showMessage("toto")

class SerialInterface(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.width=600
        self.height=800
       
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

        #add Status bar
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar)

       
        #add connect group / DiagBox
        self.dialog=Dialog()
        centralLayout.addWidget(self.dialog)

        print("MainFrame Interface initialized")


if __name__ == "__main__":

    print("Lidl Gateway Flash soft Started")
    app = QApplication(sys.argv)
    frame = SerialInterface()
    frame.show()
    sys.exit(app.exec())