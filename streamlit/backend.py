from time import time
import serial
import time
import streamlit as st
import plotly.express as px
import pandas as pd

class SerialHandler:
    def __init__(self, port, baudrate, timeout,columns,n_buffer):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.columns=columns
        self.n_buffer=n_buffer
        self.plot_buffer=pd.DataFrame(columns=self.columns)
        
    def readline(self):
        time.sleep(0.01)
        return self.ser.readline()
    
    def bit_to_volt(self,bit):
        return bit/4095*3.3
    
    def preprocess(self,data):
        raw_dat=data.decode()
        data = raw_dat.strip()
        self.preprocessed_data=[float(x) for x in data.split("|")]
        return self.preprocessed_data
    
    def dataframing(self,data):
        return pd.DataFrame([data], columns=self.columns)
    
    def buffer_write(self,data,n_buffer):
        if len(self.plot_buffer.index)==n_buffer:
            self.plot_buffer = self.plot_buffer.iloc[1: , :]
        self.plot_buffer=pd.concat([self.plot_buffer,data], ignore_index=True)
    
    def preprocessed_routine(self):
        data = self.readline()
        self.preprocess(data)
        
    def buffer_routine(self):
        dataframe = self.dataframing(self.preprocessed_data)
        self.buffer_write(dataframe,self.n_buffer)
    
    def plot_map(self,placeholder):
        # fig = px.line(self.plot_buffer, x=self.plot_buffer.index,y=self.plot_buffer.columns,render_mode="webgl")
        # fig.update_layout(title="Live Data",xaxis_title="Time",yaxis_title="Voltage")
        # placeholder.plotly_chart(fig)    
        placeholder.line_chart(self.plot_buffer)  
        
    def plot_metrics(self,placeholders):
        for i,(placeholder,columns) in enumerate(zip(placeholders,self.columns)):
            placeholder.metric(columns,self.preprocessed_data[i])
        
        
        
    