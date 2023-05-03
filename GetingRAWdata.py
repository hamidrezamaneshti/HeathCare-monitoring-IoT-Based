import serial
import csv

def open_serial_port(port, baudrate, timeout):
    """Open the serial port with the specified parameters."""
    return serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

def read_data(arduino, num_samples):
    """Read data from the serial port and store it in a list."""
    data = []
    for _ in range(num_samples):
        data.append(str(arduino.readline()))
    return data

def clean_data(data):
    """Clean the data by removing unnecessary characters."""
    cleaned_data = []
    for item in data:
        cleaned_data.append(item[2:-5])
    return cleaned_data

def write_data_to_csv(data, file_path):
    """Write the cleaned data to a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['hart'])
        for item in data:
            writer.writerow([item])

if __name__ == "__main__":
    arduino = open_serial_port(port="COM3", baudrate=9600, timeout=1)
    raw_data = read_data(arduino, num_samples=10)
    print(raw_data)
    cleaned_data = clean_data(raw_data)
    print(cleaned_data)
    write_data_to_csv(cleaned_data, file_path="Sample_Dataset.csv")