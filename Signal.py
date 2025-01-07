from PyQt5 import QtCore
import Main_Program_UI
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog ,QApplication , QMainWindow,QColorDialog
import sys
import pandas as pd 
import math
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Spacer
from Second_Window_Program  import MainWindow as secondwindow
from scipy.interpolate import interp1d
from Main_Program_UI import Ui_MainWindow

class Signal():

    top_signals=[]
    middle_signals=[]
    def __init__(self,id,filename,name,amplitude,time,timer,widget,plot,legend,position,hide=False,rectangle=None,color=None):
        super().__init__()
        self.id=id
        self.filename=filename
        self.name=name
        self.label=name
        self.amplitude=amplitude
        self.time=time
        self.timer=timer
        self.widget=widget
        self.plot=plot
        self.legend=legend
        self.hide=hide
        self.position=position
        self.rectangle=rectangle
        self.color=color
        if self.position=="Top":
            Signal.top_signals.append(self)
        elif self.position=="Middle":
            Signal.middle_signals.append(self)
    @classmethod
    def signal_list(self,position):
        if position=="Top":
            return Signal.top_signals
        elif position=="Middle":
            return  Signal.middle_signals
    @classmethod
    def Delete_Signal_List(self , position):
        if position=="Top":
            Signal.top_signals=[]
        elif position=="Middle":
            Signal.middle_signals=[]
        
    


        