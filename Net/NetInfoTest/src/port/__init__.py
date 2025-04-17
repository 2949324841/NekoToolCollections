#   poetry run port
#   ---PORT 测试用---
#   本地网络信息观察窗口工具
#   可以查看本地暴露的socket申请的运行软件（服务）的地址：端口数据等信息
#   部分功能没有完善（包括列排序，目前是QTableView的默认排序方式，这些。。。等）

from port.MainWindow import *;


def main():
    app = QApplication(sys.argv)
    window = MainWindow(None)
    window.show()
    return app.exec()