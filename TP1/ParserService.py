import io
import csv
import json
import socket
import signal
import time
import traceback
import sys

class ReadFile:
    
    def __init__(self,archivo):
        self.datos = ""
        self.archivo = archivo
        self.dict_reader = {}
    
    def config(self):
        try:
            with open(self.archivo,"r") as f:
                self.datos = f.read()
                return self.datos
        except io.UnsupportedOperation as e:
	        print("No tengo permisos de escritura")
	        print(e)
        except FileNotFoundError as e:
	        print("Archivo no existe")
	        print(e)

    def csv(self):
        try:
            self.dict_reader = csv.DictReader(open(self.archivo))
            return self.dict_reader
        except io.UnsupportedOperation as e:
            print("No tengo permisos de escritura")
            print(e)
        except FileNotFoundError as e:
            print("Archivo no existe")
            print(e)

class Parser:
    def __init__(self, datos_dic):
        self.datos_dic = datos_dic
        self.json_array = []
    
    def DicToJson(self):
        for row in self.datos_dic:
            self.json_array.append(row)
        return json.dumps(self.json_array, indent=4)
       
class Main:

    def __init__(self):
        try:
            self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error:
	        print ('Fallo en la creacion del socket UDP')
	        sys.exit()

    def handler(self,sig, frame):  # define the handler  
        print("Signal Number:", sig, " Frame: ", frame)  
        traceback.print_stack(frame)
        self.UDPClientSocket.close()
        sys.exit()
    
    def main(self):

        # Defino el handler de SIGINT
        signal.signal(signal.SIGINT, self.handler)

        # Leo archivo de configuracion y csv
        csv_dict = {}
        nombrecsv = ReadFile("config.txt").config()
        csv_dict = ReadFile(nombrecsv).csv()

        # Parser de csv a json
        json_data = Parser(csv_dict).DicToJson()
 
        # Encode para enviar por socket UDP
        bytesToSend = str.encode(json_data)

        # Envio datos a servidor UDP
        port = 10000
        serverAddressPort = ("localhost", port)
        self.UDPClientSocket.sendto(bytesToSend, serverAddressPort)  

while True:
    Main().main()
    time.sleep(30)