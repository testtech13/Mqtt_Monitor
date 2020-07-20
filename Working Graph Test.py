# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random

RoomT1 = [] #Data is what is recevied from the
RoomT2 = []

import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.1.48"
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker



def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))
    
def on_message_from_temp1(client, userdata, message):
    RoomT1.insert(0,round(float(message.payload.decode()),2))
    print(RoomT1)
    window.update_graph()
    
def on_message_from_temp2(client, userdata, message):
    RoomT2.insert(0,round(float(message.payload.decode()),2))
    print(RoomT2)
    window.update_graph()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
client.subscribe("temp1")
client.message_callback_add("temp1", on_message_from_temp1)
client.subscribe("temp2")
client.message_callback_add("temp2", on_message_from_temp2)
print("subscribe")    

client.loop_start()

class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
		
        QMainWindow.__init__(self)

        loadUi("MplMain.ui",self)

        self.setWindowTitle("House Monitor")

        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)
        self.pushButton_generate_random_signal_2.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
		


    def update_graph(self):
        self.QLabel.LabelT1.text(RoomT2[0])

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(RoomT1)
        self.MplWidget.canvas.axes.plot(RoomT2)
        #self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('Temp1', 'Temp2'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Room Temperature')
        self.MplWidget.canvas.draw()
		

     
        

app = QApplication([])
app.setStyle('bb10dark')
window = MatplotlibWidget()
window.show()
app.exec_()
