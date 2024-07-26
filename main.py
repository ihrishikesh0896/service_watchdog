import psutil
import time
import logging
import multiprocessing
import platform
import socket

# Configure logging
logging.basicConfig(filename='service_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect() for UDP doesn't send packets
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        logging.info(f"Detected local IP: {local_ip}")
    except Exception as e:
        local_ip = '127.0.0.1'
        logging.error(f"Error obtaining local IP: {e}")
    finally:
        s.close()
    return local_ip


def get_current_services(local_ip):
    connections = psutil.net_connections(kind='inet')
    services = []
    monitor_list = ['127.0.0.1', '0.0.0.0', local_ip, '::']
    for conn in connections:
        if conn.laddr.ip in monitor_list and conn.status == 'LISTEN':
            services.append((conn.laddr.port, conn.pid))
    logging.info(f"Current services: {services}")
    return services


def monitor_services(interval=60):
    local_ip = get_local_ip()
    known_services = set(get_current_services(local_ip))
    logging.info("Starting service monitor...")

    while True:
        try:
            current_services = set(get_current_services(local_ip))
            new_services = current_services - known_services

            for port, pid in new_services:
                try:
                    proc = psutil.Process(pid)
                    logging.info(f"New service detected on IP {local_ip} port {port} with PID {pid}, Name: {proc.name()}")
                except psutil.NoSuchProcess:
                    logging.warning(f"Service detected on IP {local_ip} port {port} but the process {pid} does not exist.")
                except psutil.AccessDenied:
                    logging.warning(f"Access denied when trying to access process with PID {pid} on IP {local_ip} port {port}.")
                except PermissionError:
                    logging.warning(f"Permission error when trying to access process with PID {pid} on IP {local_ip} port {port}.")

            known_services = current_services
        except Exception as e:
            logging.error(f"Error in monitoring services: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    os_name = platform.system()
    logging.info(f"Detected OS: {os_name}")

    if os_name in ["Windows", "Linux", "Darwin"]:
        try:
            # Run the monitor as a background process
            p = multiprocessing.Process(target=monitor_services, args=(60,))
            p.start()
            logging.info("Service monitor started successfully.")
        except Exception as e:
            logging.error(f"Failed to start service monitor: {e}")
    else:
        error_message = f"Unsupported OS: {os_name}"
        print(error_message)
        logging.warning(error_message)
