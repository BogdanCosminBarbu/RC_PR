import struct
import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook

IP = '127.0.0.1'
PORT = 502
ID = 0x00


class Client:
    trans_high_id = 0x00
    trans_low_id = 0x00
    proto_high_id = 0x00
    proto_low_id = 0x00
    high_len = 0x00
    low_len = 0x06

    FC_read_coils = 1
    FC_read_holding_registers = 3
    FC_read_input_registers = 4
    FC_write_single_coil = 5
    FC_write_single_register = 6
    FC_write_multiple_coils = 15
    FC_write_multiple_registers = 16

    def __init__(self, idu=ID, ip=IP, port=PORT):
        self.tcp_id = idu
        self.tcp_ip = ip
        self.tcp_port = port
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = False

    # FUNCTION CODE 1
    def read_coils(self, adr_high, adr_low, nr_coils_high, nr_coils_low):
        pachet = struct.pack('12B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, self.high_len, self.low_len, self.tcp_id,
                             int(self.FC_read_coils),
                             adr_high, adr_low, nr_coils_high, nr_coils_low)
        self.tcp_socket.sendall(pachet)


    # FCUNTION CODE 3
    def read_holding_registers(self, adr_high, adr_low, nr_reg_high, nr_reg_low):
        pachet = struct.pack('12B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, self.high_len, self.low_len, self.tcp_id,
                             int(self.FC_read_holding_registers),
                             adr_high, adr_low, nr_reg_high, nr_reg_low)
        self.tcp_socket.sendall(pachet)
        return pachet

    # FUNCTION CODE 4
    def read_input_registers(self, adr_high, adr_low, nr_reg_high, nr_reg_low):
        pachet = struct.pack('12B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, self.high_len, self.low_len, self.tcp_id,
                             int(self.FC_read_input_registers),
                             adr_high, adr_low, nr_reg_high, nr_reg_low)
        self.tcp_socket.sendall(pachet)
        return pachet

    # FCUNTION CODE 5
    def write_single_coil(self, stare=True, adr_high=0x00, adr_low=0x01):
        if stare:
            value = 0xff
        else:
            value = 0x00

        pachet = struct.pack('12B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, self.high_len, self.low_len, self.tcp_id,
                             int(self.FC_write_single_coil),
                             adr_high, adr_low, value, 0x00)
        self.tcp_socket.sendall(pachet)
        return pachet

    # FUNCTION CODE 6
    def write_single_register(self, adr_high, adr_low, data_high, data_low):
        pachet = struct.pack('12B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, self.high_len, self.low_len, self.tcp_id,
                             int(self.FC_write_single_register),
                             adr_high, adr_low, data_high, data_low)
        self.tcp_socket.sendall(pachet)

    # FUNCTION CODE 15
    def write_multiple_coils(self, adr_high, adr_low, nr_coils_high, nr_coils_low, nr_byte, data_high):
        pachet = struct.pack('14B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, 0x00, 0x08, self.tcp_id,
                             int(self.FC_write_multiple_coils),
                             adr_high, adr_low, nr_coils_high, nr_coils_low,
                             nr_byte, data_high)
        self.tcp_socket.sendall(pachet)

    # FUNCTION CODE 16
    def write_multiple_registers(self, adr_high, adr_low, nr_reg_high, nr_reg_low, nr_byte, data_high):
        pachet = struct.pack('14B', self.trans_high_id, self.trans_low_id, self.proto_high_id,
                             self.proto_low_id, 0x00, 0x08, self.tcp_id,
                             int(self.FC_write_multiple_registers),
                             adr_high, adr_low, nr_reg_high, nr_reg_low,
                             nr_byte, data_high)
        self.tcp_socket.sendall(pachet)

    #adr_high, adr_low, nr_reg_high, nr_reg_low
    def memorie_procent(self):
        self.read_input_registers(0x00, 0x01, 0x00, 0x02)
        data = self.tcp_socket.recv(1024)
        primit = struct.unpack('13B', data)
        intreg = primit[9] * 256 + primit[10]
        zecimal = primit[11] * 256 + primit[12]
        return intreg + (zecimal / 100)
    def cpu_procent(self):
        self.read_input_registers(0x00, 0x03, 0x00, 0x02)
        data = self.tcp_socket.recv(1024)
        primit = struct.unpack('13B', data)
        intreg = primit[9] * 256 + primit[10]
        zecimal = primit[11] * 256 + primit[12]
        return intreg + (zecimal / 100)

    def is_internet(self):
        try:
            sock = socket.create_connection(("www.google.com", 80))
            print("Este internet")
        except OSError:
            print("Nu e internet")
        return False
        # self.read_coils(0x00, 0x01, 0x00, 0x01)
        # data = self.tcp_socket.recv(1024)
        # primit = struct.unpack('12B', data)
        # if primit == 0:
        #     print("Nu este internet")
        # else:
        #     print("Este internet")

    def pornire_conexiune(self):
        # Trimitem la coilurile 1 12 123 1234 mesaje

        self.tcp_socket.connect((self.tcp_ip, self.tcp_port))

        print("Avem urmatoarele pachete")
        pachet_trimis = self.write_single_coil(True, 0x00, 0x01)
        pachet_primit = self.tcp_socket.recv(1024)
        if pachet_trimis != pachet_primit:
            print("Pachetul ", pachet_trimis, " e diferit de pachetul primit ", pachet_primit)
        else:
            print("Merge")

        pachet_trimis = self.write_single_coil(True, 0x00, 0x02)
        pachet_primit = self.tcp_socket.recv(1024)
        if pachet_trimis != pachet_primit:
            print("Pachetul ", pachet_trimis, " e diferit de pachetul primit ", pachet_primit)
        else:
            print("Merge")

        pachet_trimis = self.write_single_coil(True, 0x00, 0x03)
        pachet_primit = self.tcp_socket.recv(1024)
        if pachet_trimis != pachet_primit:
            print("Pachetul ", pachet_trimis, " e diferit de pachetul primit ", pachet_primit)
        else:
            print("Merge")

        pachet_trimis = self.write_single_coil(True, 0x00, 0x04)
        pachet_primit = self.tcp_socket.recv(1024)
        if pachet_trimis != pachet_primit:
            print("Pachetul ", pachet_trimis, " e diferit de pachetul primit ", pachet_primit)
        else:
            print("Merge")

        self.connection = True


class Interface(Frame, Client):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Client Modbus TCP")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Informatii")
        lbl.grid(sticky=W, pady=4, padx=5)
        n = Notebook(self)
        f3 = Frame(n)
        f4 = Frame(n)
        f5 = Frame(n)
        f6 = Frame(n)
        f7 = Frame(n)
        f8 = Frame(n)
        n.add(f3, text='Input Registers')
        n.add(f4, text='Hold Registers')
        n.add(f5, text='Internet connection')
        n.add(f6, text='Start connection')
        n.add(f7, text='Memory')
        n.add(f8, text='CPU')
        n.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E + W + S + N)

        client = Client()
        #client.pornire_conexiune()

        button3 = Button(f3, text="Input Register", command=lambda: print("Input register este ", client.read_input_registers(0x00, 0x01, 0x00, 0x02)))
        button4 = Button(f4, text="Hold Register", command=lambda: print("Holding register este ", client.read_holding_registers(0x00, 0x01, 0x00, 0x03)))
        button5 = Button(f5, text="Internet", command=lambda: client.is_internet())
        button6 = Button(f6, text="Pornire Conexiune", command=lambda: client.pornire_conexiune())
        button7 = Button(f7, text="Memorie", command=lambda: print(client.memorie_procent()))
        button8 = Button(f8, text="CPU", command=lambda: print(client.cpu_procent()))
        # Asezarea butoanelor in fiecare frame
        button3.grid(row=4, column=3, padx=5)
        button4.grid(row=4, column=3, padx=5)
        button5.grid(row=4, column=3, padx=5)
        button6.grid(row=4, column=3, padx=5)
        button7.grid(row=4, column=3, padx=5)
        button8.grid(row=4, column=3, padx=5)



def main():
    root = Tk()
    root.geometry("600x300+300+300")
    app = Interface()
    root.mainloop()


if __name__ == '__main__':
    main()
