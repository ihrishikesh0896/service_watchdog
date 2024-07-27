# Local Service Monitor

`local_service_monitor.py` is a Python script designed to monitor and log any new services that start listening on `localhost` (127.0.0.1) on any port. The script is cross-platform compatible, running seamlessly on Windows, Linux, and macOS.

## Features

- **Local IP Detection**: Identifies the local IP address of the machine.
- **Service Monitoring**: Continuously monitors for new services that are listening on `localhost`.
- **Background Process**: Runs as a background process to ensure continuous monitoring without interrupting other tasks.
- **Cross-Platform Compatibility**: Compatible with major operating systems including Windows, Linux, and macOS.
- **Logging**: Logs the details of new services, including the port, process ID (PID), and process name, to a log file (`service_monitor.log`).

## Use Case: Integration with EDR Systems
This script can be used as part of a custom EDR (Endpoint Detection and Response) solution to enhance security monitoring capabilities. It helps in detecting temporary ports that are opened and used to send/receive data from other devices or hosts, which can be indicative of suspicious activity or potential security threats.

By integrating this script with your EDR system, you can:

- Monitor for Temporary Services: Detect new services that open ports temporarily, which might be used for unauthorized data transfer.
- Log Suspicious Activity: Keep a detailed log of all new services, making it easier to investigate suspicious activities.
- Automate Responses: Combine this script with other security tools to automate responses to potential threats, such as alerting administrators or shutting down suspicious services.

## Requirements

- Python 3.x
- `psutil` library

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ihrishikesh0896/service_watchdog.git
   cd local_service_monitor
   ```

2. **Install Dependencies**:
   Ensure `psutil` is installed:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Script**:
   Execute the script with Python:
   ```bash
   python local_service_monitor.py
   ```

## How It Works

1. **Initialization**: The script configures logging to store logs in `service_monitor.log`.
2. **IP Address Retrieval**: Uses the `socket` library to determine the local IP address.
3. **Service Detection**: Utilizes the `psutil` library to fetch current services listening on `localhost`.
4. **Monitoring Process**: Runs `monitor_services` as a background process using the `multiprocessing` module, checking for new services at specified intervals (default is every 60 seconds).
5. **Logging**: Logs any new services detected with their port, PID, and process name.

## Example Log Entry

```
2024-07-26 12:34:56 - New service detected on port 8080 with PID 12345, Name: python
```

## OS Detection

The script detects the operating system and handles OS-specific operations if necessary. If an unsupported OS is detected, it logs a warning and terminates.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or new features to add.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact [ihrishikeshnate@gmail.com] or open an issue on GitHub.

---
