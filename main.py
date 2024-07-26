import psutil
import time
import logging
import multiprocessing
import socket
from datetime import datetime


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect() for UDP doesn't send packets
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Configure logging
logging.basicConfig(filename='service_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Function to get current services
def get_current_services():
    connections = psutil.net_connections(kind='inet')
    services = []
    print('Round Iteration at :' + str(datetime.now().strftime('%H:%M:%S %Y-%m-%d')))
    monitor_list = ['127.0.0.1','0.0.0.0', get_local_ip, '::']
    for conn in connections:
        if conn.laddr.ip in monitor_list:
            services.append((conn.laddr.ip, conn.laddr.port, conn.pid))
    return services

def monitor_services(interval=60):
    known_services = set(get_current_services())
    logging.info("Starting service monitor...")

    while True:
        current_services = set(get_current_services())
        new_services = current_services - known_services

        for ip, port, pid in new_services:
            try:
                proc = psutil.Process(pid)
                logging.info(f"New service detected on port {port} for ip {ip} with PID {pid}, Name: {proc.name()}")
            except psutil.NoSuchProcess:
                logging.warning(f"Service detected on port {port} for ip {ip} but the process {pid} does not exist.")

        known_services = current_services
        time.sleep(interval)

if __name__ == "__main__":
    # Run the monitor as a background process
    p = multiprocessing.Process(target=monitor_services, args=(60,))
    p.start()
    p.join()