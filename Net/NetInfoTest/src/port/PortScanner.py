import psutil

class PortScanner:
    @staticmethod
    def get_all_ports():
        connections = psutil.net_connections(kind='inet')  # 获取所有网络连接
        port_data = []

        for conn in connections:
            if conn.status == psutil.CONN_LISTEN:
                state = "LISTEN"
            else:
                state = conn.status

            port_data.append({
                "protocol": "TCP" if conn.type == 1 else "UDP",
                "local_ip": conn.laddr.ip if conn.laddr else "",
                "local_port": conn.laddr.port if conn.laddr else 0,
                "remote_ip": conn.raddr.ip if conn.raddr else "",
                "remote_port": conn.raddr.port if conn.raddr else 0,
                "state": state,
                "pid": conn.pid,
                "process_name": psutil.Process(conn.pid).name() if conn.pid else ""
            })

        return port_data

# 示例输出
def display_example():
    ports = PortScanner.get_all_ports()
    for port in ports[:5]:  # 打印前5条记录
        print(port)