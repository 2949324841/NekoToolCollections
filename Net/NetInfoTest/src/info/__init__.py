#poetry run info
#---TCP 测试用---
# 这个代码是一个简单的TCP服务器，用于获取本机的网络接口信息，并在客户端连接时返回这些信息。
# 服务器会监听指定的端口，并在有客户端连接时，返回本机的网络接口信息和客户端的连接信息。
# Windows可以使用telnet命令来连接服务器，Linux可以使用nc命令来连接服务器。
#可以通过下方PORT参数来指定端口号
#此代码是堵塞的，不能同时处理多个连接
#可以通过ctrl+c来停止服务器(建议直接关掉终端)



import socket
import threading
from time import sleep
import netifaces
import ipaddress
from datetime import datetime

PORT = 8084 # 默认端口号



def get_network_info():
    """获取本机的网络接口信息"""
    interfaces = netifaces.interfaces()
    info = {
        'hostname': socket.gethostname(),
        'interfaces': []
    }
    
    for interface in interfaces:
        ifaddrs = netifaces.ifaddresses(interface)
        interface_info = {
            'name': interface,
            'ipv4': [],
            'ipv6': [],
            'mac': None
        }
        
        # 获取MAC地址
        if netifaces.AF_LINK in ifaddrs:
            interface_info['mac'] = ifaddrs[netifaces.AF_LINK][0]['addr']
        
        # 获取IPv4地址
        if netifaces.AF_INET in ifaddrs:
            for addr in ifaddrs[netifaces.AF_INET]:
                ip = addr['addr']
                netmask = addr.get('netmask', '')
                broadcast = addr.get('broadcast', '')
                
                # 计算网络地址
                network = ''
                if ip and netmask:
                    try:
                        network = str(ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False))
                    except:
                        pass
                
                interface_info['ipv4'].append({
                    'address': ip,
                    'netmask': netmask,
                    'broadcast': broadcast,
                    'network': network
                })
        
        # 获取IPv6地址
        if netifaces.AF_INET6 in ifaddrs:
            for addr in ifaddrs[netifaces.AF_INET6]:
                ip = addr['addr']
                # 去掉IPv6的%scope部分
                if '%' in ip:
                    ip = ip.split('%')[0]
                netmask = addr.get('netmask', '')
                
                interface_info['ipv6'].append({
                    'address': ip,
                    'netmask': netmask
                })
        
        info['interfaces'].append(interface_info)
    
    return info

def format_network_info(info):
    """格式化网络信息为可读字符串"""
    lines = []
    lines.append(f"Hostname: {info['hostname']}")
    lines.append("\nNetwork Interfaces:")
    
    for interface in info['interfaces']:
        lines.append(f"\nInterface: {interface['name']}")
        if interface['mac']:
            lines.append(f"  MAC: {interface['mac']}")
        
        if interface['ipv4']:
            lines.append("  IPv4 Addresses:")
            for addr in interface['ipv4']:
                lines.append(f"    Address: {addr['address']}")
                lines.append(f"    Netmask: {addr['netmask']}")
                if addr['broadcast']:
                    lines.append(f"    Broadcast: {addr['broadcast']}")
                if addr['network']:
                    lines.append(f"    Network: {addr['network']}")
        
        if interface['ipv6']:
            lines.append("  IPv6 Addresses:")
            for addr in interface['ipv6']:
                lines.append(f"    Address: {addr['address']}")
                lines.append(f"    Netmask: {addr['netmask']}")
    
    return "\n".join(lines)

server_info = format_network_info(get_network_info())

def handle_client(conn, addr):
    """处理客户端连接"""
    try:
        # 获取客户端信息
        client_info = {
            'address': addr[0],
            'port': addr[1],
            'family': 'IPv4' if ':' not in addr[0] else 'IPv6'
        }
        
        # 获取服务器信息
        #server_info = get_network_info()
        
        # 准备响应数据
        response = []
        response.append("="*40)
        response.append(f"Connection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        response.append("\nServer Network Information:")
        response.append(server_info)
        
        response.append("\n\nClient Network Information:")
        response.append(f"Address: {client_info['address']}")
        response.append(f"Port: {client_info['port']}")
        response.append(f"IP Version: {client_info['family']}")
        response.append("="*40)
        response.append("")  # 空行表示结束
        print(response)
        
        # 发送响应
        conn.sendall("\n".join(response).encode('utf-8'))
        
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection closed with {addr}")

def start_server(port):
    """启动TCP服务器"""
    # 创建IPv4和IPv6套接字
    try:
        server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        print("Server will listen on both IPv4 and IPv6")
    except:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server will listen on IPv4 only (IPv6 not available)")
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('', port))
        server_socket.listen(5)
        print(f"{server_info}")
        print(f"Server started on port {port}. Waiting for connections...")
        
        while True:
            conn, addr = server_socket.accept()
            print(f"\nNew connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            sleep(0.01)
            
    # except KeyboardInterrupt:
    #     print("\nServer is shutting down...")
    #except Exception as e:
    #    print(f"Server error: {e}")
    finally:
        server_socket.close()

def main():
    """主函数入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TCP Server Test Tool')
    parser.add_argument('-p', '--port', type=int, default=PORT, 
                        help=f'Port to listen on (default:  {PORT})')
    
    args = parser.parse_args()
    
    start_server(args.port)