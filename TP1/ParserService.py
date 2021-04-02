import io
import csv
import json
import socket

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
        pass

    def main(self):

        nombrecsv = ReadFile("config.txt").config()
        #reader = {}
        #reader = ReadFile(nombrecsv).csv()

        json_data = Parser(ReadFile(nombrecsv).csv()).DicToJson()
 
        bytesToSend = str.encode(json_data)
        # Create a datagram socket
        port = 10000
        serverAddressPort = ("localhost", port)

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)


Main().main()