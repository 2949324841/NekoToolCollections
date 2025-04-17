from port.PortScanner import *;
from port.MainWindow import *;

def display_example1():
    ports = PortScanner.get_all_ports()
    for port in ports[:5]:  # 打印前5条记录
        print(port)

def main():
    app = QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    return app.exec()