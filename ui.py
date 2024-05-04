import sys
import numpy as np
from PySide6.QtCore import QThread, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QImage, QPixmap
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import requests
import json

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=3, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

class GetMethod(QThread):

    plot_update  = Signal(list,list,str,int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.end_point = ""
        self.type = ""
        self.message = ""
        self.ID = ""
        self.Databuffer = 1000
        self.exit_flag = ""

    def start_visuals(self):
        self.exit_flag = False

    def stop_visuals(self):
        print("End visuals")
        self.exit_flag = True

    def run(self):
        print("Starting the thread")
        while True:
            self._get_method(self.type , self.end_point, self.message, self.ID)  # Call  
        print("end of thread")



    def _get_method(self, type, end_point, message, ID):
        print(type , end_point)
        if self.type == "_stream_consumption":
            if (self.exit_flag == True):
                pass
            else:
                response = requests.get(self.end_point, stream=True)
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        self._update_text(decoded_line)
        elif type == "consumption+consumption":
            if (self.exit_flag == True):
                pass
            else:
                response = requests.get(self.end_point)
                J_response = json.loads(response.text)["consumption"][-(self.Databuffer):]
                x = [x['timestamp'] for x in J_response]
                y = [y['value'] for y in J_response]
                type_ = "consumption"
                self.emit_plot_update(x,y,"consumption",0)
        elif type == "grid+to_consumption":
            if (self.exit_flag == True):
                pass
            else:
                response = requests.get(self.end_point)
                J_response = json.loads(response.text)["to_consumption"][-(self.Databuffer):]
                x = [x['timestamp'] for x in J_response]
                y = [y['value'] for y in J_response]
                self.emit_plot_update(x,y,self.type ,0)
        elif type == "grid+to_storage":
            if (self.exit_flag == True):
                pass
            else:
                response = requests.get(end_point)
                J_response = json.loads(response.text)["to_storage"][-(self.Databuffer):]
                x = [x['timestamp'] for x in J_response]
                y = [y['value'] for y in J_response]
                self.emit_plot_update(x,y,self.type ,0)
        elif type == "production+to_consumption":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["to_consumption"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "production+to_grid":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["to_grid"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "production+to_storage":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["to_storage"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "storage+capacity":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["capacity"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "storage+charge":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["charge"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "storage+to_consumption":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["to_consumption"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "storage+to_grid":
            response = requests.get(end_point)
            J_response = json.loads(response.text)["to_grid"][-(self.Databuffer):]
            x = [x['timestamp'] for x in J_response]
            y = [y['value'] for y in J_response]
            self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_conumption+consumption":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                        # response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["consumption"]['timestamp'])
                        y.append(line_as_json["consumption"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
            self.exit_flag == False
        elif type == "stream_grid+to_consumption":
            print(f"Im inside of stream flag is {self.exit_flag}")
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_consumption"]['timestamp'])
                        y.append(line_as_json["to_consumption"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
            
        elif type == "stream_grid+to_storage":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_storage"]['timestamp'])
                        y.append(line_as_json["to_storage"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_grid+to_storage":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_storage"]['timestamp'])
                        y.append(line_as_json["to_storage"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_production+to_consumption":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_consumption"]['timestamp'])
                        y.append(line_as_json["to_consumption"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_production+to_grid":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_grid"]['timestamp'])
                        y.append(line_as_json["to_grid"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_production+to_storage":
                response = requests.get(end_point, stream=True)
                print(end_point,response)
                x = list()
                y = list()
                for line in response.iter_lines():
                    print(f"Im inside of stream flag is {self.exit_flag}")
                    if (self.exit_flag == True):
                        break
                    elif (self.exit_flag == False):
                        if line:
                        #     response = line.decode('utf-8')
                            line_as_json = json.loads(line)
                            print(line_as_json)
                            x.append(line_as_json["to_grid"]['timestamp'])
                            y.append(line_as_json["to_grid"]['value'])

                            if (len(x)>10):
                                x.pop(0)
                                y.pop(0)
                            self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_storage+capacity":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["capacity"])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_storage+charge":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["charge"]['timestamp'])
                        y.append(line_as_json["charge"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_storage+to_consumption":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_consumption"]['timestamp'])
                        y.append(line_as_json["to_consumption"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
        elif type == "stream_storage+to_grid":
            response = requests.get(end_point, stream=True)
            print(end_point,response)
            x = list()
            y = list()
            for line in response.iter_lines():
                print(f"Im inside of stream flag is {self.exit_flag}")
                if (self.exit_flag == True):
                    break
                elif (self.exit_flag == False):
                    if line:
                    #     response = line.decode('utf-8')
                        line_as_json = json.loads(line)
                        print(line_as_json)
                        x.append(line_as_json["to_grid"]['timestamp'])
                        y.append(line_as_json["to_grid"]['value'])

                        if (len(x)>10):
                            x.pop(0)
                            y.pop(0)
                        self.emit_plot_update(x,y,self.type ,0)
            

    def emit_plot_update(self, time,value, type,buffer):
        self.plot_update.emit(time,value, type,buffer)  # Emit the progress value

# ------------------------------------------------------------------------------------------------------

class hackathon(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.window = self.loader.load("Data_Measaure.ui")
        self.ID = "88cf343b-4080-4d30-8de9-dfa905d6eb9b"
        self.stream_consumption = self.window.SC1
        self.consumption = self.window.MC1
        self.stream_conumption = self.window.SC1
        self.grid = self.window.MG1
        self.stream_grid = self.window.SG1
        self.comboBox = self.window.comboBox
        self.production = self.window.MP1
        self.storage = self.window.MS1
        self.status_box = self.window.textEdit
        self.graphicview = self.window.graphicsView
        self.stream_production = self.window.SP1
        self.showdata = self.window.showdata
        self.start_visuals = self.window.start_visuals
        self.end_visuals = self.window.stop_visuals
        self.showdatabutton = self.window.showdatabutton

        self.comboBox.activated.connect(self._on_combo)
        self.stream_consumption.toggled.connect(self._stream_consumption)
        self.consumption.toggled.connect(self._consumption)
        self.production.toggled.connect(self._production)
        self.storage.toggled.connect(self._production)
        self.stream_storage = self.window.SS1
        self.grid.toggled.connect(self._grid)
        self.stream_consumption.toggled.connect(self._stream_consumption)
        self.stream_grid.toggled.connect(self._stream_grid)
        self.stream_production.toggled.connect(self._stream_production)
        self.start_visuals.clicked.connect(self._start_visuals)
        self.end_visuals.clicked.connect(self._end_visuals)
        self.stream_storage.toggled.connect(self._stream_storage)
        # Create a Matplotlib plot canvas
        self.canvas = PlotCanvas()
        self.layout = QtWidgets.QVBoxLayout(self.graphicview)
        self.layout.addWidget(self.canvas)
        # Initiate the threads
        self.Getmethod = GetMethod()
        # Variables
        self.stream_counter = 0

    def _end_visuals(self):
        self.Getmethod.stop_visuals()
        self._update_text("Ending the sesion")
        ax = self.canvas.ax
        ax.clear()

    def _start_visuals(self):
        self.Getmethod.start_visuals()
        if(self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option"):
            self._update_text("Starting the sesion")
        if(self.storage.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/storage"
            self._get_method("storage+"+current_value, end_point, "", self.ID)
        elif(self.production.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/production"
            self._get_method("production+"+current_value, end_point, "", self.ID)
        elif(self.consumption.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/consumption"
            self._get_method("consumption+"+current_value, end_point, "", self.ID)
        elif(self.grid.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/grid"
            self._get_method("grid+"+current_value, end_point, "", self.ID)
        elif(self.stream_consumption.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/consumption"
            self._get_method("stream_conumption+"+current_value, end_point, "", self.ID)
        elif(self.stream_grid.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/grid"
            self._get_method("stream_grid+"+current_value, end_point, "", self.ID)
        elif(self.stream_production.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/production"
            self._get_method("stream_production+"+current_value, end_point, "", self.ID)
        elif(self.stream_storage.isChecked() and (self.comboBox.itemText(self.comboBox.currentIndex()) != "select a option")):
            self._update_text("Loading the Data....")
            current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
            end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/storage"
            self._get_method("stream_storage+"+current_value, end_point, "", self.ID)
        else:
            self._update_text("Select an option")

    def _showdata(self,mssg):
        self.showdata.setText(mssg)

    def plot_graph(self,x,y,title):
        # Generate example data
        ax = self.canvas.ax
        ax.clear()
        ax.plot(x, y)
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Kw')
        ax.tick_params(axis='x', rotation=90)
        self.canvas.draw()
        self._update_text("Loaded Successfully")


    def _on_combo(self):
        pass
        # if(self.storage.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/storage"
        #     self._get_method("storage+"+current_value, end_point, "", self.ID)
        # elif(self.production.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/production"
        #     self._get_method("production+"+current_value, end_point, "", self.ID)
        # elif(self.consumption.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/consumption"
        #     self._get_method("consumption+"+current_value, end_point, "", self.ID)
        # elif(self.grid.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/measurements/grid"
        #     self._get_method("grid+"+current_value, end_point, "", self.ID)
        # elif(self.stream_consumption.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/consumption"
        #     self._get_method("stream_conumption+"+current_value, end_point, "", self.ID)
        # elif(self.stream_grid.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/grid"
        #     self._get_method("stream_grid+"+current_value, end_point, "", self.ID)
        # elif(self.stream_production.isChecked()):
        #     self._update_text("Loading the Data....")
        #     current_value = self.comboBox.itemText(self.comboBox.currentIndex()) 
        #     end_point = f"https://hackathon.kvanttori.fi/buildings/{self.ID}/streams/grid"
        #     self._get_method("stream_production+"+current_value, end_point, "", self.ID)

    def _production(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option" ,"to_consumption" , "to_grid","to_storage"])
        self._update_text("select a option in what to visualize")

    
    def _storage(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option" ,"capacity" ,"charge" , "to_consumption","to_grid"])
        self._update_text("select a option in what to visualize")

    def _consumption(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option","consumption"])
        self._update_text("select a option in what to visualize")

    def _grid(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option" ,"to_consumption" , "to_storage"])
        self._update_text("select a option in what to visualize")
        

    def _stream_consumption(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option","consumption"])
        self._update_text("select a option in what to visualize")

    def _stream_grid(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option","to_consumption","to_storage"])
        self._update_text("select a option in what to visualize")

    def _stream_production(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option","to_consumption","to_grid","to_storage"])
        self._update_text("select a option in what to visualize")
    
    def _stream_storage(self):
        self.comboBox.clear()
        self.comboBox.addItems(["select a option","capacity","charge","to_consumption","to_grid"])
        self._update_text("select a option in what to visualize")

    def _update_text(self, mssg):
        self.status_box.setText(mssg)

    def _get_method(self, type, end_point, message, ID):
        self.Getmethod.ID = ID
        self.Getmethod.type = type
        self.Getmethod.end_point = end_point
        self.Getmethod.message = message
        self.Getmethod.plot_update.connect(self.plot_graph)
        self.Getmethod.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    start_hackathon = hackathon()
    start_hackathon.window.show()
    sys.exit(app.exec())
