import psutil
import time
import datetime
import socket

def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_logical_count = psutil.cpu_count(logical=True)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    host_ip = socket.gethostbyname(socket.gethostname())  

    return cpu_percent, cpu_logical_count, memory_info.used, disk_info.used, host_ip

def log_system_info(log_file, monitoring_period, threshold):
    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu_percent, cpu_logical_count, used_memory, used_disk_space, host_ip = get_system_info()

        log_entry = f"{current_time}, {cpu_percent}%, {cpu_logical_count}, {used_memory}B, {used_disk_space}B, {host_ip}"

        with open(log_file, 'a') as file:
            file.write(log_entry + "\n")

        if used_memory / psutil.virtual_memory().total > threshold / 100:
            notify_low_memory(current_time)

        time.sleep(monitoring_period)

def notify_low_memory(current_time):
    notification_file = f"{current_time}-notification.log"
    with open(notification_file, 'w') as file:
        file.write("Low memory: The system is running low on memory.")

def main():
    monitoring_period = int(input("Enter the monitoring period in seconds (default is 5 seconds): ") or 5)
    threshold = float(input("Enter the memory threshold percentage (default is 80%): ") or 80)

    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = f"{current_time_str}-pub.log"

    log_system_info(log_file, monitoring_period, threshold)

if __name__ == "__main__":
    main()
