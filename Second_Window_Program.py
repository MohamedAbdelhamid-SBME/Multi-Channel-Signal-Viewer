from PyQt5 import QtCore
import Bassant
import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QColorDialog, QVBoxLayout, QWidget
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

class MainWindow(QMainWindow, Bassant.Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.canvas = FigureCanvas(plt.Figure(figsize=(8, 8)))
        self.canvas.setStyleSheet("background: Black;\n"
                                   "border: 2px solid white;\n"
                                   "border-radius:20px;\n"
                                   "")
        self.verticalLayout_2.addWidget(self.canvas)

        self.ToolButton_PlayPause.clicked.connect(self.playPause)
        self.Isplaying = True
        self.ToolButton_PlayPause.setText("Pause")

        self.ToolButton_Rewind.clicked.connect(self.rewind)

    
        data = pd.read_csv("radars.csv")
        data = data.drop(["Rk", "Nation", "Pos", "Squad", "Age", "90s", "Born", "Matches", "FK", "PK", "PKatt"], axis=1)
        data = data.dropna()

        data = data[(data != 0).all(axis=1)]
        data["Player"] = data["Player"].str.split('\\').str[0]
        data = data[(data.select_dtypes(include=['number']) >= 0).all(axis=1)] 
        data = data[20:25]

        df = pd.DataFrame(data)

        
        self.params = list(df.columns[1:]) 
        self.values = df.iloc[:, 1:].values  

        
        self.ranges = []
        for param in self.params:
            min_val = df[param].min() - (df[param].min() * 0.25)
            max_val = df[param].max() + (df[param].max() * 0.25)
            self.ranges.append((min_val, max_val))

        
        self.normalized_values = []
        for value in self.values:
            normalized_value = [(val - self.ranges[i][0]) / (self.ranges[i][1] - self.ranges[i][0]) for i, val in enumerate(value)]
            self.normalized_values.append(normalized_value)

        
        self.normalized_values = np.array(self.normalized_values)

        
        self.num_vars = len(self.params)
        self.angles = np.linspace(0, 2 * np.pi, self.num_vars, endpoint=False).tolist()

        
        self.normalized_values = np.concatenate((self.normalized_values, self.normalized_values[:, [0]]), axis=1)
        self.angles += self.angles[:1]

       
        self.fig = self.canvas.figure
        self.ax = self.fig.add_subplot(111, polar=True)

        
        self.ax.set_ylim(0, 1) 

        num_ticks = 5  
        custom_radius_values = np.linspace(0, 1, num_ticks)  
        self.ax.set_yticks(custom_radius_values)  
        self.ax.set_yticklabels([f"{value:.2f}" for value in custom_radius_values])  
        self.ax.set_xticks(self.angles[:-1])
        self.ax.set_xticklabels(self.params)  

        self.lines = []
        self.fills = []
        colors = [
            (173/255, 216/255, 230/255), 
            (135/255, 206/255, 235/255), 
            (0/255, 191/255, 255/255),    
            (30/255, 144/255, 255/255),  
            (65/255, 105/255, 225/255),  
            (0/255, 0/255, 205/255),      
            (0/255, 0/255, 139/255)       
        ]

        for i, player in enumerate(df['Player']):
            line, = self.ax.plot([], [], color=colors[i], linewidth=2, label=player)
            self.lines.append(line)

        self.ani = FuncAnimation(self.fig, self.update, frames=self.num_vars * len(df['Player']), init_func=self.init, blit=True, repeat=True, interval=500)

       
        self.ax.legend(loc='upper left')  
        self.canvas.draw()

    def init(self):
        for line in self.lines:
            line.set_data([], [])
          
        return self.lines 

    def update(self, frame):
        player_index = frame // self.num_vars
        param_index = frame % self.num_vars
        line = self.lines[player_index]       
        normalized_value = self.normalized_values[player_index]
        line.set_data(self.angles[:param_index + 1], normalized_value[:param_index + 1])
      
        if param_index == self.num_vars - 1:
            line.set_data(self.angles, normalized_value)  

        return self.lines 

    def playPause(self):
        if self.Isplaying:
            self.ToolButton_PlayPause.setText("Play")
            self.ani.event_source.stop()  
            self.Isplaying = False
        else:
            self.ToolButton_PlayPause.setText("Pause")
            self.ani.event_source.start()  
            self.Isplaying = True

    def rewind(self):
        self.ani.event_source.stop()  
        self.Isplaying = True
        self.ToolButton_PlayPause.setText("Pause")  
        self.init()  
        self.canvas.draw()      
        self.ani.frame_seq = self.ani.new_frame_seq()       
        self.ani.event_source.start() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    second_window = MainWindow()
    second_window.show() 
    sys.exit(app.exec_())
