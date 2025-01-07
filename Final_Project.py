from PyQt5 import QtCore
from PyQt5.QtCore import Qt
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
from Signal import Signal
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time





chrome_options = Options()
# Uncomment the next line to run Chrome in headless mode (without a GUI)
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-web-security')




class MainWindow(QMainWindow,Main_Program_UI.Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.index_signal=-1
        self.Index_T_tracking=0
        self.Index_M_tracking=0
        try :
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.url = 'https://www.binance.com/en/trade/BTC_USDT?_from=markets&type=spot'
            self.driver.get(self.url)
        except:
            pass
        self.API_Time=[]
        self.BTC_USDT=[]
        self.Time_Creator_Api=-1
       

        self.islinked=False
    

        self.timer_T=QtCore.QTimer()
        self.timer_M=QtCore.QTimer()
        self.timer_T.setInterval(10)
        self.timer_M.setInterval(10)

        self.islinked=False
        self.Top_isrunning=False
        self.Middle_isrunning=False
        
        self.my_pen=pg.mkPen(width=2)
        self.Snapshots_Array=[]
        self.concatenate_Data=[]
        self.time_Sampling=0
        self.statistics_Array=[]
        self.Isconnected=False

        
        
        self.ToolButton_Top_Browse.clicked.connect(lambda:self.get_data_Browser(self.Widget_Top))
        self.ToolButton_Middle_Browse.clicked.connect(lambda:self.get_data_Browser(self.Widget_Middle))

        self.timer_T.timeout.connect(lambda : self.update_graph(self.Widget_Top))
        self.timer_M.timeout.connect(lambda : self.update_graph(self.Widget_Middle))

        self.ToolButton_Top_PlayPause.clicked.connect(lambda:self.plot_data_playpause(self.Widget_Top))
        self.ToolButton_Middle_PlayPause.clicked.connect(lambda:self.plot_data_playpause(self.Widget_Middle))
        self.ToolButton_Top_Replay.clicked.connect(lambda:self.rewind(self.Widget_Top))
        self.ToolButton_Middle_Replay.clicked.connect(lambda:self.rewind(self.Widget_Middle))
        self.ToolButton_Top_SelectColor.clicked.connect( lambda : self.Get_Color(self.Widget_Top))
        self.ToolButton_Middle_SelectColor.clicked.connect( lambda : self.Get_Color(self.Widget_Middle))
        self.ComboBox_Top_Signals.currentIndexChanged.connect(lambda:self.show_hide_checkbox(self.Widget_Top))
        self.ComboBox_Middle_Signals.currentIndexChanged.connect(lambda:self.show_hide_checkbox(self.Widget_Middle))
        self.checkBox_Top_ShowHide.stateChanged.connect(lambda:self.Show_Hide(self.Widget_Top))
        self.checkBox_Middle_ShowHide.stateChanged.connect(lambda:self.Show_Hide(self.Widget_Middle))
        self.LineEdit_Top_EditLabel.textChanged.connect(lambda : self.Track_Label(self.Widget_Top))
        self.LineEdit_Middle_EditLabel.textChanged.connect(lambda : self.Track_Label(self.Widget_Middle))
        self.ToolButton_Top_SubmitSpeed.clicked.connect(lambda:self.set_frequncy(self.Widget_Top))
        self.ToolButton_Middle_SubmitSpeed.clicked.connect(lambda:self.set_frequncy(self.Widget_Middle))

        self.ToolButton_Top_ZoomIn.clicked.connect(lambda : self.zoom_in(self.Widget_Top))
        self.ToolButton_Top_ZoomOut.clicked.connect(lambda : self.zoom_out(self.Widget_Top))

        self.ToolButton_Middle_ZoomIn.clicked.connect(lambda : self.zoom_in(self.Widget_Middle))
        self.ToolButton_Middle_ZoomOut.clicked.connect(lambda : self.zoom_out(self.Widget_Middle))
        self.ToolButton_Top_Delete.clicked.connect(lambda:self.Remove_Selected_Signal(self.Widget_Top))
        self.ToolButton_Middle_Delete.clicked.connect(lambda:self.Remove_Selected_Signal(self.Widget_Middle))
        self.CheckBox_API.stateChanged.connect(lambda:self.StateChanged_CheckBox_API())
        # link 
        self.CheckBox_LinkGraphs.stateChanged.connect(self.Link_Graphs)

        

        self.ToolButton_Top_SelectPart.clicked.connect(lambda : self.Select_Part_Graph(self.Widget_Top))
        self.ToolButton_Middle_SelectPart.clicked.connect(lambda : self.Select_Part_Graph(self.Widget_Middle))
        self.ComboBox_InterpolationOrder.currentIndexChanged.connect(self.Update_GlueGraphs_Interpolation)
        self.ToolButton_ConcatnateGraphs.clicked.connect(self.Glue_Graphs)
        self.ToolButton_SecondWindow.clicked.connect(self.show_Second_Window)
        self.ToolButton_Top_TakeSnapShot.clicked.connect(lambda : self.collect_SnapShots(self.Widget_Top))
        self.ToolButton_Middle_TakeSnapShot.clicked.connect(lambda : self.collect_SnapShots(self.Widget_Middle))
        self.ToolButton_CreatePdf.clicked.connect(self.create_pdf_with_images)

        self.ToolButton_MoveDown.clicked.connect(lambda:self.Move_Signal(self.Widget_Top))
        self.ToolButton_MoveUp.clicked.connect(lambda:self.Move_Signal(self.Widget_Middle))

        # disableee buttons 
        self.ToolButton_Top_TakeSnapShot.setEnabled(False)
        self.ToolButton_Middle_TakeSnapShot.setEnabled(False)
   
        self.HorizontalSlider_Top_connectGraphs.setEnabled(False)
        self.HorizontalSlider_Middle_connectGraphs.setEnabled(False)

        self.horizontalScrollBar_Top.valueChanged.connect(lambda:self.update_scrollbar_view(self.Widget_Top))
        self.horizontalScrollBar_Middle.valueChanged.connect(lambda:self.update_scrollbar_view(self.Widget_Middle))

           
        self.Widget_Top.sigRangeChanged.connect(lambda:self.change_limit(self.Widget_Top))
        self.Widget_Middle.sigRangeChanged.connect(lambda:self.change_limit(self.Widget_Middle))
            

        
        self.plot_api=self.Widget_Top.plot()

    def change_limit(self,widget):
    
        if self.islinked and not (self.Top_isrunning):
            x,y=widget.viewRange()
            if widget==self.Widget_Middle:
                self.Widget_Top.blockSignals(True)
                self.Widget_Top.setXRange(x[0],x[1])
                self.Widget_Top.setYRange(y[0],y[1])
                self.Widget_Top.blockSignals(False)

            else:
                self.Widget_Middle.blockSignals(True)
                self.Widget_Middle.setXRange(x[0],x[1])
                self.Widget_Middle.setYRange(y[0],y[1])
                self.Widget_Middle.blockSignals(False)


    def get_data_Browser(self , Widget):
        fileName=self.browse_file()
        print(fileName)
        if fileName is not None:
            self.add_signal(Widget,fileName)
            
    def add_signal(self,Widget,fileName,color=None):
        
        #id for the signal 
        self.index_signal+=1
        # index tracking>> =0 >> choose anther signal 
        self.Index_currentSignal=self.index_signal   

        name=fileName.split('/')[-1].split('.')[0]          
        pen=pg.mkPen(width=2)
        plot=Widget.plot(pen=pen)
        legend=Widget.addLegend()
        legend.addItem(plot,name)
        time , amplitude =  self.read_file(fileName)          
        timer=self.timer(Widget)
        position=self.specify_widget(Widget)
        signal=Signal(self.index_signal,fileName,name,amplitude,time,timer,Widget,plot,legend,position,color=color)
        comboBox=self.comboBox(Widget)
        comboBox.addItem(signal.name)
        
        comboBox.setItemData(comboBox.count()-1,signal,Qt.UserRole)
        comboBox.setCurrentText(signal.name)
        position=self.specify_widget(Widget)
        #print(Signal.signal_list(position) ,len(Signal.signal_list(position)) )
        
        self.rewind(Widget)
        
    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;CSV Files (*.csv);;DAT Files (*.dat);;XLSX Files (*.xlsx);;TXT Files (*.txt)", options=options)
        
        if fileName:
            print(f"Selected file: {fileName}")
            try:
                return fileName
            except Exception as e:
                print(f"Error opening file: {e}")
                return None
        else:
            print("No file selected")
            return None
        
    def read_file(self, fileName):
        if fileName.endswith('.csv'):
            df = pd.read_csv(fileName)
        elif fileName.endswith('.xlsx'):
            df = pd.read_excel(fileName)
        elif fileName.endswith('.dat') or fileName.endswith('.txt'):
            df = pd.read_csv(fileName, sep='\t')
        time = df.iloc[:, 0].to_numpy()
        amplitude =df.iloc[:, 1].to_numpy()
        return time, amplitude
    
    def plot_data_playpause(self ,widget):
        
        timer=self.timer(widget)
        position=self.specify_widget(widget)
        
        if self.islinked:
           if self.Top_isrunning :
                    self.ToolButton_Top_PlayPause.setText("Play")
                    self.ToolButton_Middle_PlayPause.setText("Play")
                    self.Top_isrunning ,self.Middle_isrunning =False , False
                    self.timer_T.stop()
                    self.timer_M.stop()
            
           else:
                    self.ToolButton_Top_PlayPause.setText("Pause")
                    self.ToolButton_Middle_PlayPause.setText("Pause")
                    self.Top_isrunning ,self.Middle_isrunning=True , True
                    self.timer_T.start()
                    self.timer_M.start()

        else:

            if len(Signal.signal_list(position))>0 or self.CheckBox_API.isChecked():
                if widget==self.Widget_Top:
                    if self.Top_isrunning:
                        self.ToolButton_Top_PlayPause.setText("Play")
                        timer.stop()
                        self.Top_isrunning=False
                    else:
                        self.ToolButton_Top_PlayPause.setText("Pause")
                        timer.start()
                        self.Top_isrunning=True
                else :
                    if  self.Middle_isrunning:
                        self.ToolButton_Middle_PlayPause.setText("Play")
                        timer.stop()
                        self.Middle_isrunning=False
                    else:
                        self.ToolButton_Middle_PlayPause.setText("Pause")
                        timer.start()
                        self.Middle_isrunning=True

    def rewind(self,widget):

        if self.CheckBox_API.isChecked():
            self.Time_Creator_Api=-1
            self.API_Time.clear()
            self.BTC_USDT.clear()

        if self.islinked:
            self.Index_T_tracking=0
            self.Index_M_tracking=0
            self.Top_isrunning=False
            self.Middle_isrunning=False
            self.plot_data_playpause(widget) 


        else :
            if widget==self.Widget_Top:
                self.Index_T_tracking=0
                self.Top_isrunning=False
                self.plot_data_playpause(widget)
                
            
            else:
                self.Index_M_tracking=0
                self.Middle_isrunning=False
                self.plot_data_playpause(widget)

    def update_graph(self,widget):

        if self.CheckBox_API.isChecked():
            timer=self.timer(self.Widget_Top)
            timer.start()
            self.Top_isrunning=True
            self.API()
            self.plot_api.setData(self.API_Time[0:-1],self.BTC_USDT[0:-1])
            
        self.Index_tracking=self.index_tracking(widget)
        position=self.specify_widget(widget)
        time_points,y,Deltas=[],[],[]
   
        for signal in Signal.signal_list(position):

            amplitude=signal.amplitude
            time=signal.time
            if self.Index_tracking<len(amplitude):
              
                plot=signal.plot
                Delta=time[1]-time[0]
                Deltas.append(Delta)
                plot.setData(time[:self.Index_tracking] , amplitude[:self.Index_tracking])
                time_points.append(time[self.Index_tracking])
                y.append(max(amplitude))
                y.append(min(amplitude))
            

        
        #print(self.CheckBox_API.isChecked())


        if not (self.CheckBox_API.isChecked() and widget==self.Widget_Top):
            if len(y)>0:
                max_y=max(y)
                min_y=min(y)
                min_x,max_x=self.get_x_lim(Deltas,time_points)
                Delta=max(Deltas)
                widget.setXRange(min_x,max_x+(10*Delta))
                widget.setYRange(min_y,max_y)
                widget.setLimits(xMin=0, xMax=max_x+(10*Delta), yMin=min_y, yMax=max_y)
               
                self.HScrollBar_limits(widget,100,int((max_x+(10*Delta))*1000),int(Delta*1000))
                
    def get_x_lim(self,Deltas,time_points):
    
        Delta=max(Deltas)
        max_x=max(time_points)
        
        if   max_x-(600*Delta)<0:
            x_min=0
        else:
            x_min=max_x-(Delta*600)
        
        return x_min,max_x
    
    
    def index_tracking(self,Widget):
        if Widget==self.Widget_Top:
            self.Index_T_tracking+=1
            return self.Index_T_tracking
        else:
            self.Index_M_tracking+=1
            return self.Index_M_tracking
        
    def Get_Color(self , widget,color=None):
        signal=self.current_selected_signal(widget)
        if color is  None:
            color=QColorDialog.getColor()
            signal.color=color
        else:
            color=signal.color
        pen=pg.mkPen(color=color , width=3)
    
        signal.plot.setPen(pen)

    def Track_Label(self, widget):

        signal=self.current_selected_signal(widget)
        label=self.LineEdit_Top_EditLabel.text() 
        set_label = lambda label: signal.name if label == "" else label           
        signal.legend.removeItem(signal.label)
        signal.label=set_label(label)
        signal.legend.addItem(signal.plot , set_label(label))
    
    def set_frequncy(self,widget):   
        if widget==self.Widget_Top:
            timer=self.timer_T
            if self.LineEdit_Top_Speed.text():
                speed=self.LineEdit_Top_Speed.text()
                self.LineEdit_Top_Speed.clear()
                timer_timeout=(10**(3))/(float(speed))
            else:
                timer_timeout=10
        
        else:
            timer=self.timer_M
            if self.LineEdit_Middle_Speed.text():
                speed=self.LineEdit_Middle_Speed.text()
                self.LineEdit_Middle_Speed.clear()
                timer_timeout=(10**(3))/(float(speed))
            else:
                timer_timeout=10
           
        print(f" timer_timeout : {timer_timeout}")
        if self.islinked:
            self.timer_T.setInterval(int(timer_timeout)) 
            self.timer_M.setInterval(int(timer_timeout))
        else :
            timer.setInterval(int(timer_timeout))  


    def Link_Graphs (self):
        self.islinked=self.CheckBox_LinkGraphs.isChecked() and self.current_selected_signal(self.Widget_Top) and self.current_selected_signal(self.Widget_Middle)
        if self.islinked :
            # set the timer to the minumum value of freq 
            self.timer_T.setInterval(max(self.timer_T.interval() , self.timer_M.interval()))
            self.timer_M.setInterval(max(self.timer_T.interval() , self.timer_M.interval()))

            self.rewind(self.Widget_Top)
            self.rewind(self.Widget_Middle)

        else :
            print(f" is checked : {self.CheckBox_LinkGraphs.isChecked()}")

    def Select_Part_Graph(self, widget): 
                
        signal=self.current_selected_signal(widget) 
        if signal:  
            if widget == self.Widget_Top:
                button=self.ToolButton_Top_SelectPart
            else:
                button=self.ToolButton_Middle_SelectPart



            start_x , start_y=self.get_startpoint_ROI(widget)
            time_sampling=signal.time[1] - signal.time[0]
            width , height=100 * time_sampling , 2000*time_sampling      
            Rec=pg.RectROI([start_x , start_y] , [width,height] ,pen='r', movable=True, resizable=True )       
            if signal.rectangle :
                rec=signal.rectangle
                signal.rectangle=None
                widget.removeItem(rec) 
                button.setText("select Part")

            else:
              widget.addItem(Rec)       
              signal.rectangle=Rec
              button.setText("Delete Rec")        

    def get_startpoint_ROI(self, widget):
        # get the bounders of my graph [[xmin , xmax],[ymin , ymax]]
        x_range=widget.viewRange()[0]
        y_range=widget.viewRange()[1]
        
        center_x=(x_range[1] + x_range[0])/2
        center_y=(y_range[1] + y_range[0])/2

        Signal=self.current_selected_signal(widget)
        time_sampling=Signal.time[1] - Signal.time[0]
        width , height=100 * time_sampling , 2000*time_sampling
  
        start_x=center_x - width/2
        start_y=center_y - height/2
        


        return start_x ,start_y

    def Get_Data_GlueGraphs(self):
        # get the 2 rectangles 
        if self.current_selected_signal(self.Widget_Top)and self.current_selected_signal(self.Widget_Middle):
            Signal_top=self.current_selected_signal(self.Widget_Top)
            Signal_middle=self.current_selected_signal(self.Widget_Middle)
            
            Rec_T=Signal_top.rectangle
            Rec_M=Signal_middle.rectangle
            if Rec_T and Rec_M:
                self.Widget_Top.removeItem(Rec_T)
                self.Widget_Middle.removeItem(Rec_M)

                self.ToolButton_Middle_SelectPart.setText("select part")
                self.ToolButton_Top_SelectPart.setText("select Part")
                


                # pos=[x , y] 
                rect_T_pos = Rec_T.pos()  
                rect_M_pos = Rec_M.pos()  
                # size =[width , height]
                rect_T_size = Rec_T.size()  
                rect_M_size = Rec_M.size()  

                
                x_min_T=rect_T_pos.x()
                x_max_T = x_min_T + rect_T_size[0]
            

                x_min_M =rect_M_pos.x()    
                x_max_M = x_min_M + rect_M_size[0]       

            
                Xaxis_Top=Signal_top.time
                Xaxis_Middle=Signal_middle.time
            
                # get the nearest  intersect _ region
                for i in range (len(Xaxis_Top)-1):
                    if x_min_T>Xaxis_Top[i] and x_min_T < Xaxis_Top[i+1]:
                        Intersect_Xmin_Top=Xaxis_Top[i]
                        break
            
                for i in range (len(Xaxis_Top)-1):
                    if x_max_T>Xaxis_Top[i] and x_max_T < Xaxis_Top[i+1]:
                        Intersect_Xmax_Top=Xaxis_Top[i+1]
                        break
            
                for i in range (len(Xaxis_Middle)-1):
                    if x_min_M>Xaxis_Middle[i] and x_min_M < Xaxis_Middle[i+1]:
                        Intersect_Xmin_Middle=Xaxis_Middle[i]
                        break
            
                for i in range (len(Xaxis_Middle)-1):
                    if x_max_M>Xaxis_Middle[i] and x_max_M < Xaxis_Middle[i+1]:
                        Intersect_Xmax_Middle=Xaxis_Middle[i+1]
                        break
            
                # # get the regions of rectangles fot top , middle
                # data={"top":{"X_rang" : [Intersect_Xmin_Top , Intersect_Xmax_Top]
                #               }
                #               ,
                #        "middle": {"X_rang" : [Intersect_Xmin_Middle , Intersect_Xmax_Middle]}      
                #       }
                
                # print(data)


                Index_Xmin_T=np.where(Signal_top.time==Intersect_Xmin_Top)[0]
                Index_Xmax_T=np.where(Signal_top.time==Intersect_Xmax_Top)[0]

                Index_Xmin_M=np.where(Signal_middle.time==Intersect_Xmin_Middle)[0]
                Index_Xmax_M=np.where(Signal_middle.time==Intersect_Xmax_Middle)[0]

                Time_Intersect_T_Range=Signal_top.time[Index_Xmin_T[0] :Index_Xmax_T[0]+1]
                Data_intersect_T_Range=Signal_top.amplitude[Index_Xmin_T[0] :Index_Xmax_T[0]+1]


                Time_Intersect_M_Range=Signal_middle.time[Index_Xmin_M[0] :Index_Xmax_M[0]+1]
                Data_intersect_M_Range=Signal_middle.amplitude[Index_Xmin_M[0] :Index_Xmax_M[0]+1]
            
            

            
                
                Data_Middle={"Data":Data_intersect_M_Range , 
                            "time":Time_Intersect_M_Range,
                            "Xmin":Intersect_Xmin_Middle,
                            "Xmax":Intersect_Xmax_Middle}
                
                Data_Top={"Data":Data_intersect_T_Range , 
                            "time":Time_Intersect_T_Range,
                            "Xmin":Intersect_Xmin_Top,
                            "Xmax":Intersect_Xmax_Top}
                
                if Intersect_Xmin_Top < Intersect_Xmin_Middle:
                    return Data_Top , Data_Middle
                else :
                    return Data_Middle , Data_Top
            
        return None , None

    def Glue_Graphs(self):
        
        if  self.current_selected_signal(self.Widget_Top).rectangle and self.current_selected_signal(self.Widget_Middle).rectangle :
            widget_index=self.ComboBox_ConcatenateGraph.currentIndex()       
            widget= self.Widget_Top if widget_index==0 else self.Widget_Middle
           
            if not self.Isconnected:
                self.Isconnected=True
                self.ToolButton_ConcatnateGraphs.setText(" DisConcatnoate ")

                first_signal , second_signal=self.Get_Data_GlueGraphs()
                if first_signal and second_signal :


                    if widget == self.Widget_Top:
                        widget.removeItem( self.current_selected_signal(self.Widget_Top).plot)
                        slider = self.HorizontalSlider_Top_connectGraphs
                        slider.setEnabled(True)
                        self.ToolButton_Top_TakeSnapShot.setEnabled(True)
                        self.ToolButton_Top_PlayPause.setEnabled(False)
                        self.ToolButton_Top_Replay.setEnabled(False)
                        self.ToolButton_Top_Browse.setEnabled(False)
                        self.ToolButton_Top_Delete.setEnabled(False)
                        self.ToolButton_Top_SelectPart.setEnabled(False)
                        self.ToolButton_Middle_SelectPart.setEnabled(False)
                        self.ToolButton_Top_SelectColor.setEnabled(False)
                        self.ToolButton_MoveDown.setEnabled(False)
                        self.ToolButton_MoveUp.setEnabled(False)
                        
                        

                    else:
                        widget.removeItem( self.current_selected_signal(self.Widget_Middle).plot)
                        slider = self.HorizontalSlider_Middle_connectGraphs
                        slider.setEnabled(True)
                        self.ToolButton_Middle_TakeSnapShot.setEnabled(True)                       
                        self.ToolButton_Middle_PlayPause.setEnabled(False)
                        self.ToolButton_Middle_Delete.setEnabled(False)
                        self.ToolButton_Middle_Browse.setEnabled(False)
                        self.ToolButton_Middle_Replay.setEnabled(False)
                        self.ToolButton_Middle_SelectPart.setEnabled(False)
                        self.ToolButton_Top_SelectPart.setEnabled(False)
                        self.ToolButton_Middle_SelectColor.setEnabled(False)
                        self.ToolButton_MoveDown.setEnabled(False)
                        self.ToolButton_MoveUp.setEnabled(False)


                    slider.valueChanged.connect(self.Update_GlueGraphs_Interpolation)


                  


                    # get the interval of second signal to replot it 
                    Sampling_Xaxis_SecondSignal= second_signal["time"][3] - second_signal["time"][2]
                    bias =Sampling_Xaxis_SecondSignal * 3

                    # strat draw second signal far away first using bias 
                    StartTime_secondSignal=first_signal["Xmax"] +bias 
                    
                    EndTime=StartTime_secondSignal + len(second_signal["Data"]) *Sampling_Xaxis_SecondSignal
                    # create a new interval time for the second graph
                    
                    Xaxis_Range=np.arange(StartTime_secondSignal, EndTime, Sampling_Xaxis_SecondSignal)
                    if len(Xaxis_Range) <len(second_signal["Data"]):
                        differ=len(second_signal["Data"]) - len(Xaxis_Range)
                        for i in range (differ) :
                            Xaxis_Range = np.append(Xaxis_Range, Xaxis_Range[-1]+Sampling_Xaxis_SecondSignal)
    
                    elif  len(Xaxis_Range) >len(second_signal["Data"]):
                        print("here minus")
                        differ=len(Xaxis_Range) - len(second_signal["Data"])
                        Xaxis_Range = Xaxis_Range[:-differ]

                    print(len(Xaxis_Range) ,len(second_signal["Data"]) )
                   
                  
                    x_min=first_signal["time"][0] - Sampling_Xaxis_SecondSignal*7
                    x_max=EndTime +Sampling_Xaxis_SecondSignal*7
                    print( x_min ,x_max )
                    widget.setLimits(xMin=x_min, xMax=x_max)
                    widget.setXRange(x_min,x_max)
                  
                  
                    # plot second signal with new interval
                    print(len(Xaxis_Range) ,len(second_signal["Data"]) )
                    widget.plot(first_signal["time"] , first_signal["Data"]  ,pen=self.my_pen)
                    widget.plot(Xaxis_Range,second_signal["Data"]  ,pen=self.my_pen)

                                        


                    
                    # for statisticssss
                    #print(f"data first : {first_signal["Data"] } , second : {second_signal["Data"]}")
                    self.concatenate_Data=np.concatenate((np.array(first_signal["Data"]) , np.array(second_signal["Data"])))
                    self.time_Sampling=Sampling_Xaxis_SecondSignal

                    slider_range=StartTime_secondSignal-first_signal["Xmin"]
                    step_slider=Sampling_Xaxis_SecondSignal

                    max=int(slider_range/step_slider)
                    print (f" steps in bar is {max}")
                    slider.setMaximum(max)
            
            elif self.Isconnected:
                self.ToolButton_ConcatnateGraphs.setText("Concatnoate Graphs")
                self.Isconnected=False
                

                self.current_selected_signal(self.Widget_Top).rectangle=None
                self.current_selected_signal(self.Widget_Middle).rectangle=None
            
                # print("hereee")
                if widget_index == 0:
                        self.Widget_Top.clear()
                        Signal.Delete_Signal_List("Top")
                        self.ComboBox_Top_Signals.clear()

                        self.HorizontalSlider_Top_connectGraphs.setValue(0)
                        self.HorizontalSlider_Top_connectGraphs.setEnabled(False)
                        self.ToolButton_Top_TakeSnapShot.setEnabled(False)
                        self.ToolButton_Top_PlayPause.setEnabled(True)
                        self.ToolButton_Top_Replay.setEnabled(True)
                        self.ToolButton_Top_Delete.setEnabled(True)
                        self.ToolButton_Top_Browse.setEnabled(True)
                        self.ToolButton_Top_SelectPart.setEnabled(True)
                        self.ToolButton_Middle_SelectPart.setEnabled(True)
                        self.ToolButton_Top_SelectColor.setEnabled(True)
                        self.ToolButton_MoveDown.setEnabled(True)
                        self.ToolButton_MoveUp.setEnabled(True)
                        
                        

                else:   
                    self.Widget_Middle.clear()
                    Signal.Delete_Signal_List("Middle")
                    self.ComboBox_Middle_Signals.clear()
                    self.HorizontalSlider_Middle_connectGraphs.setValue(0)
                    self.HorizontalSlider_Middle_connectGraphs.setEnabled(False)
                    self.ToolButton_Middle_TakeSnapShot.setEnabled(False)
                    self.ToolButton_Middle_PlayPause.setEnabled(True)
                    self.ToolButton_Middle_Replay.setEnabled(True)
                    self.ToolButton_Top_SelectPart.setEnabled(True)
                    self.ToolButton_Middle_SelectPart.setEnabled(True)
                    self.ToolButton_Middle_Delete.setEnabled(True)
                    self.ToolButton_Middle_Browse.setEnabled(True)
                    self.ToolButton_Middle_SelectColor.setEnabled(True)
                    self.ToolButton_MoveDown.setEnabled(True)
                    self.ToolButton_MoveUp.setEnabled(True)

    def Update_GlueGraphs_Interpolation(self):
        # 0>> top , 1 >> midlle 

        
        widget_index=self.ComboBox_ConcatenateGraph.currentIndex()
        if widget_index == 0:
            widget= self.Widget_Top
            Bar = self.HorizontalSlider_Top_connectGraphs
        else:
            widget= self.Widget_Middle
            Bar = self.HorizontalSlider_Middle_connectGraphs
        

        widget.clear()         
        slider_value=Bar.value()
        order=self.get_Order_from_Index(self.ComboBox_InterpolationOrder.currentIndex())

        first_data , second_data=self.Get_Data_GlueGraphs()

        if first_data and second_data:
            Sampling_Xaxis_firstSignal=first_data["time"][1]-first_data["time"][0]
            Sampling_Xaxis_SecondSignal=second_data["time"][1]-second_data["time"][0]
            
            bias =Sampling_Xaxis_SecondSignal * 5

            StartTime=first_data["Xmax"] + bias - (slider_value * Sampling_Xaxis_SecondSignal)
            
            print(slider_value)

            EndTime=StartTime + len(second_data["Data"]) *Sampling_Xaxis_SecondSignal
            Xaxis_Range=np.arange(StartTime, EndTime +Sampling_Xaxis_SecondSignal , Sampling_Xaxis_SecondSignal)
            
            
            print(  len(Xaxis_Range) , len(second_data["Data"]))
            
            if len(Xaxis_Range) < len(second_data["Data"]):
                differ=len(second_data["Data"]) - len(Xaxis_Range)
                for i in range (differ) :
                  Xaxis_Range = np.append(Xaxis_Range, Xaxis_Range[-1]+Sampling_Xaxis_SecondSignal)
            elif  len(Xaxis_Range) > len(second_data["Data"]):
                print("minus")
                differ=len(Xaxis_Range) - len(second_data["Data"])
                Xaxis_Range = Xaxis_Range[:-differ]
            


            start_overlap, end_overlap =self.get_overlap_interval(first_data["time"] ,Xaxis_Range )
        
            if start_overlap:
                    # sampling the time based on small sampling time for 2 signals 
                    sampling_time = min(Sampling_Xaxis_SecondSignal, Sampling_Xaxis_firstSignal)

                    num_samples = int((end_overlap - start_overlap) / sampling_time) + 1
                    # Generate values using np.linspace()
                    time_common = np.linspace(start_overlap, end_overlap, num_samples)
                    # print(f"time comnmmon : {time_common}")
                    #  linear functions for interpolationnn
                    
                    # get the data in the common time 
                    Fsignal_Interp_region= interp1d(first_data["time"], first_data["Data"], kind=order, fill_value='extrapolate')(time_common) 
                    Ssignal_Inter_region=interp1d(Xaxis_Range, second_data["Data"], kind=order, fill_value='extrapolate')(time_common) 
                    

                    combined_signal = np.where(time_common <= end_overlap, (Fsignal_Interp_region + Ssignal_Inter_region) / 2, Ssignal_Inter_region)


                    #print(f"real data plot1 {first_data["Data"]} \n real data plot2 : 3{second_data["Data"]} ")
                    # print(f"interpolated datatop: {Fsignal_Interp_region} \n interpolated dtaa midd : {Ssignal_Inter_region} ")
                    # print(f"combined signal : {combined_signal}")


                    combined_signal_full = np.concatenate((
                    first_data["Data"][:first_data["time"].searchsorted(start_overlap)],  # Non-overlapping part of signal 1
                    combined_signal,  # Combined part of signals in the overlapping region
                    second_data["Data"][Xaxis_Range.searchsorted(end_overlap):]  # Non-overlapping part of signal 2
                        ))

                # Create full time vector
                    t_full = np.concatenate((
                        first_data["time"][:first_data["time"].searchsorted(start_overlap)],  # Non-overlapping time of signal 1
                        time_common,  # Common time for overlap
                        Xaxis_Range[Xaxis_Range.searchsorted(end_overlap):]  # Non-overlapping time of signal 2
                    ))

                    widget.plot(t_full , combined_signal_full ,pen=self.my_pen)
                    self.concatenate_Data=combined_signal_full
                    self.time_Sampling=min(Sampling_Xaxis_SecondSignal , Sampling_Xaxis_firstSignal)

            else :
                    widget.plot(first_data["time"] , first_data["Data"]  ,pen=self.my_pen)
                    widget.plot(Xaxis_Range,second_data["Data"]  ,pen=self.my_pen)
                    #print(f"data first : {first_data["Data"] } , second : {second_data["Data"]}")
                    self.concatenate_Data=np.concatenate((np.array(first_data["Data"]) ,np.array( second_data["Data"])))
                    self.time_Sampling=Sampling_Xaxis_SecondSignal

    def Remove_Selected_Signal(self,Widget):
        removed_signal=self.current_selected_signal(Widget)
        if removed_signal:
            comboBox=self.comboBox(Widget)
            index=comboBox.currentIndex()
            Widget.removeItem(removed_signal.plot)
            comboBox.removeItem(index)
            
            if Widget==self.Widget_Top:
                Signal.top_signals.remove(removed_signal)
            else:
                Signal.middle_signals.remove(removed_signal)

            position=self.specify_widget(Widget)
            timer=self.timer(Widget)
            if len(Signal.signal_list(position))==0:
                timer.stop()
                
                if Widget==self.Widget_Top:
                    self.ToolButton_Top_PlayPause.setText("Play")
                    self.Top_isrunning=False
                    self.Index_T_tracking=0
                else:
                    self.ToolButton_Middle_PlayPause.setText("Play")
                    self.Middle_isrunning=False
                    self.Index_M_tracking=0

    def get_overlap_interval(self,Time_1 ,Time_2 ):
        Time_1 = np.asarray(Time_1)
        Time_2 = np.asarray(Time_2)

        # Calculate overlap start and end correctly using np.maximum and np.minimum
        start = np.max([Time_1[0], Time_2[0]])  # Use a list to get the max
        end = np.min([Time_1[-1], Time_2[-1]])  # Use a list to get the min
         
        # Check if there is an actual overlap
        if start <= end:
            print(f"start : {start} , end : {end}")
            return start, end
        return None , None

    def get_Order_from_Index(self , index_order):
        if index_order ==0: return "nearest"
        elif index_order==1: return "linear"
        elif index_order==2:return "quadratic"
        elif index_order==3:return "cubic"

    def timer(self,Widget):
        if Widget==self.Widget_Top:
            return self.timer_T
        else:
            return self.timer_M
            
    def comboBox(self,widget):
        if widget==self.Widget_Top:
            return self.ComboBox_Top_Signals
        else:
           return self.ComboBox_Middle_Signals

    def specify_widget(self,widget):
        if widget==self.Widget_Top:
            return "Top"
        elif widget==self.Widget_Middle:
            return "Middle"

    def Show_Hide(self,widget):
        current_selected_signal=self.current_selected_signal(widget)
        if widget==self.Widget_Top:
            if self.checkBox_Top_ShowHide.isChecked():   
                current_selected_signal.hide=True
                current_selected_signal.plot.hide()
            else:
                current_selected_signal.hide=False
                current_selected_signal.plot.show()
        elif widget==self.Widget_Middle:
            if self.checkBox_Middle_ShowHide.isChecked():   
                current_selected_signal.hide=True
                current_selected_signal.plot.hide()
            else:
                current_selected_signal.hide=False
                current_selected_signal.plot.show()

    def show_hide_checkbox(self,widget):
        current_selected_signal=self.current_selected_signal(widget)
        if current_selected_signal:
            if widget==self.Widget_Top:
                self.checkBox_Top_ShowHide.setChecked(current_selected_signal.hide)  
            else :
                self.checkBox_Middle_ShowHide.setChecked(current_selected_signal.hide)

    def show_Second_Window(self):
            print("second_window here")
            self.second_window = secondwindow()
            self.second_window.show() 

    def current_selected_signal(self,widget):
        comboBox=self.comboBox(widget)
        index=comboBox.currentIndex()
        signal=comboBox.itemData(index,Qt.UserRole)    
        return signal

    def collect_SnapShots(self, widget):
        snapshot = widget.grab()
        snapshot_file = f"img_{len(self.Snapshots_Array) + 1}.png"  # e.g., img_1.png
        snapshot.save(snapshot_file, "PNG")
    
        self.Snapshots_Array.append(snapshot_file)
        
        self.statistics_Array.append(self.calculate_statistics(self.concatenate_Data , self.time_Sampling))

    def create_pdf_with_images(self):
        if len(self.Snapshots_Array)>0:
            pdf = SimpleDocTemplate("test.pdf", pagesize=letter)
            story = []
            
            # Get maximum width and height from the letter page size
            max_width, max_height = letter


            # Loop through images and statistics
            for index, (img_path, stats) in enumerate(zip(self.Snapshots_Array, self.statistics_Array)):
                # Add the image name above the image
                # image_name = img_path.split('/')[-1]  # Extract the image name from the file path
                # name_paragraph = Paragraph(f"<b>{image_name}</b>", styles['Title'])  # Add bold text for the image name
                # story.append(name_paragraph)  # Add the image name to the PDF
                # story.append(Spacer(1, 6))  # Add space between the name and the image

                # Create an Image object from the saved image file
                img = Image(img_path)

                # Original image dimensions
                img_width, img_height = img.drawWidth, img.drawHeight

                # Scale the image to fit within the page size, maintaining aspect ratio
                aspect_ratio = img_width / img_height
                if img_width > max_width or img_height > max_height:
                    if img_width > max_width:
                        img_width = max_width
                        img_height = img_width / aspect_ratio
                    
                    if img_height > max_height:
                        img_height = max_height
                        img_width = img_height * aspect_ratio

                # Set the scaled dimensions to the image object
                img.drawWidth = img_width
                img.drawHeight = img_height

                # Add the image and a spacer to the story
                story.append(img)
                story.append(Spacer(1, 12))  # Add space between image and table

                # Create a structured table from the statistics
                table_data = [
                    ['Statistic', 'Value'],
                    ['Mean', f"{stats['mean']:.2f}"],
                    ['Standard Deviation', f"{stats['std']:.2f}"],
                    ['Minimum', f"{stats['min']:.2f}"],
                    ['Maximum', f"{stats['max']:.2f}"],
                    ['Duration', f"{stats['duration']:.2f}"]
                ]

                # Create a table and set its style
                table = Table(table_data, colWidths=[max_width * 0.4, max_width * 0.3])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Header row color
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BODYPADDING', (0, 0), (-1, -1), 8)
                ]))

                # Check if there is enough space for the table on the current page
                if len(story) + 2 + len(table_data) > max_height / 20:  # 2 for image and spacer
                    story.append(PageBreak())  # Add a page break if not enough space

                # Add the table to the story
                story.append(table)
                story.append(Spacer(1, 12))  # Add space after the table

                # Check if two images have been added, and if so, add a page break
                if (index + 1) % 2 == 0:
                    story.append(PageBreak())  # Add a page break after two sets of images and tables

            # Build the PDF with the story
            pdf.build(story)
            print("PDF created successfully: test.pdf")
            print(len(self.Snapshots_Array))
            self.Snapshots_Array.clear()
            self.statistics_Array.clear()

    def calculate_statistics(self,data , time_sampling):
        # print(f" in stst  , data :{data} , time : {time_sampling}")
        stats = {}
        stats['mean'] = np.mean(data)
        stats['std'] = np.std(data)
        stats['min'] = np.min(data)
        stats['max'] = np.max(data)
        stats['duration'] = time_sampling
        return stats

    def zoom_in(self , widget) :
       if self.islinked:
           viewboxT=self.Widget_Top.getViewBox()
           viewboxM=self.Widget_Middle.getViewBox()
           viewboxT.scaleBy((.8,.8))
           viewboxM.scaleBy((.8,.8))
       else:
         viewbox= widget.getViewBox()
         viewbox.scaleBy((0.8, 0.8))

    def zoom_out(self,widget):
        if self.islinked:
           viewboxT=self.Widget_Top.getViewBox()
           viewboxM=self.Widget_Middle.getViewBox()
           viewboxT.scaleBy((1/0.8, 1/0.8))
           viewboxM.scaleBy((1/0.8, 1/0.8))
        else:
        
            viewbox= widget.getViewBox()
            viewbox.scaleBy((1/0.8, 1/0.8))

    def API (self):
        pass
    #     try:
    #     # Extract the page source
    #         html = self.driver.page_source

    #         # Parse the HTML with BeautifulSoup
    #         soup = BeautifulSoup(html, 'html.parser')

    #         # Find the price element (update this selector as needed)
    #         price_element = soup.find('div', class_='showPrice')
    #         if price_element:
    #             price = price_element.text.strip()  # Get the text and remove extra spaces
    #             price=self.convert_to_float(price)
    #             self.BTC_USDT.append(price)
    #             self.Time_Creator_Api+=1
    #             self.API_Time.append(self.Time_Creator_Api)

    #             print("BTC/USDT Price:", price)
    #         else:
    #            pass
    #     except KeyboardInterrupt:
    #         print(f"y :{self.BTC_USDT}")
    #         print(f"x : {self.API_Time}")
    #         print("Stopping price updates...")

    def convert_to_float(self,number_str):
    # Remove commas from the string
        cleaned_number = number_str.replace(",", "")
        # Convert the cleaned string to a float
        return float(cleaned_number)

    def StateChanged_CheckBox_API(self):
        
        if  self.CheckBox_API.isChecked():
            self.Widget_Top.addItem(self.plot_api)
            self.ToolButton_Top_Browse.setEnabled(False)
            self.ToolButton_Top_SubmitSpeed.setEnabled(False)
            self.ToolButton_Top_Replay.setText("clear")
            for _ in range(len(Signal.top_signals)):
                self.Remove_Selected_Signal(self.Widget_Top)
        else:
            self.Top_isrunning=False
            self.ToolButton_Top_PlayPause.setText("Play")
            self.ToolButton_Top_Replay.setText("replay")
            self.ToolButton_Top_Browse.setEnabled(True)
            self.ToolButton_Top_SubmitSpeed.setEnabled(True)
            self.ToolButton_Top_Replay.setEnabled(True)
            self.Widget_Top.removeItem(self.plot_api)            

    def Move_Signal(self,widget):
        moved_signal=self.current_selected_signal(widget)
        if moved_signal:
            if moved_signal.color is None:
                moved_signal.color="white"
            if widget==self.Widget_Top:
                self.add_signal(self.Widget_Middle,moved_signal.filename,color=moved_signal.color)
                self.Get_Color(self.Widget_Middle,moved_signal.color)
                self.Remove_Selected_Signal(widget)
                
            else:
            
                self.add_signal(self.Widget_Top,moved_signal.filename,color=moved_signal.color)
                self.Get_Color(self.Widget_Top,moved_signal.color)
                self.Remove_Selected_Signal(widget)

    def HScrollBar_limits(self,widget,min,max,delta):
        if widget==self.Widget_Top:
            self.horizontalScrollBar_Top.blockSignals(True)
            self.horizontalScrollBar_Top.setMinimum(min)
            self.horizontalScrollBar_Top.setMaximum(max)
            self.horizontalScrollBar_Top.setSingleStep(delta)
            self.horizontalScrollBar_Top.setPageStep(10*delta)
            self.horizontalScrollBar_Top.setValue(max)
            self.horizontalScrollBar_Top.blockSignals(False)
        else:
            self.horizontalScrollBar_Middle.blockSignals(True)
            
            self.horizontalScrollBar_Middle.setMinimum(min)
            self.horizontalScrollBar_Middle.setMaximum(max)
            self.horizontalScrollBar_Middle.setSingleStep(delta)
            self.horizontalScrollBar_Middle.setPageStep(10*delta)
            self.horizontalScrollBar_Middle.setValue(max)
            self.horizontalScrollBar_Middle.blockSignals(False)

    
    def update_scrollbar_view(self,widget):
        if widget==self.Widget_Top:
            x=self.horizontalScrollBar_Top.value()/1000
            widget.setXRange(x-.1,x)
        else:
            x=self.horizontalScrollBar_Middle.value()/1000
            widget.setXRange(x-.1,x)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    MainWindow_ = MainWindow()
    MainWindow_.show()
    sys.exit(app.exec_())