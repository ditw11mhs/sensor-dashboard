import streamlit as st
import serial.tools.list_ports
import time
from backend import SerialHandler

class WebApp:
    def main(self):
        st.sidebar.title("Project Sismik")
        st.sidebar.text("Aditya Wardianto\nMuhammad Daffa Gunawan")
        self.initialization()
        self.start_connection()
    
    def initialization(self):
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port, _, _ in sorted(ports):
            port_list.append(port)
        c1,c2=st.sidebar.columns(2)
        self.port = c1.selectbox("Select Port", port_list,index=1)
        self.baudrate = c2.selectbox(
            "Select Baudrate", [9600, 19200, 38400, 57600, 115200], index=4
        )
        self.timeout = c1.selectbox(
            "Select Timeout", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        )
        self.n_buffer = c2.number_input("Data Buffer", min_value=1, value=10)
        self.plot_map = c1.checkbox("Plot Map",True)
        self.plot_metrics = c2.checkbox("Plot Metrics",True)
        
    def start_connection(self):
        if st.sidebar.button("Start Plot"):
            stop_connection = st.sidebar.button("Stop")
            master = SerialHandler(self.port, self.baudrate, self.timeout,["Potentio 1","Potentio 2","Potentio 3"],self.n_buffer)
            plot_placeholder = st.empty()
            c1_c,c2_c,c3_c,c4_c = st.columns(4)
            metrics_placeholder = [c1_c.empty(),c2_c.empty(),c3_c.empty()]
            hz_placeholder = c4_c.empty()
            
            if self.plot_map and not self.plot_metrics:
                while True:
                    start = time.time()
                    master.preprocessed_routine()
                    master.buffer_routine()
                    master.plot_map(plot_placeholder)
                    end = time.time()
                    
                    hz_placeholder.metric("Hz",1/(end-start))
                    
                    if stop_connection:
                        print("stop")
                        break
            
            if not self.plot_map and self.plot_metrics:
                while True:
                    start = time.time()
                    master.preprocessed_routine()
                    master.plot_metrics(metrics_placeholder)
                    end = time.time()
                    hz_placeholder.metric("Hz",1/(end-start))
                    
                    if stop_connection:
                        print("stop")
                        break
                
            if self.plot_map and self.plot_metrics:
                while True:
                    start = time.time()
                    master.preprocessed_routine()
                    master.buffer_routine()
                    master.plot_metrics(metrics_placeholder)
                    master.plot_map(plot_placeholder)
                    end = time.time()
                    
                    hz_placeholder.metric("Hz",1/(end-start))
                    
                    if stop_connection:
                        print("stop")
                        break
                
        
        
if __name__ == "__main__":
    app = WebApp()
    app.main()