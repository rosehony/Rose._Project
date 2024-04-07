import time
from collections import deque
import matplotlib.pyplot as plt
from scapy.all import sniff
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Global variables
packet_sizes = []
arrival_times = deque(maxlen=100)  # Sliding time window of 100 packets
THRESHOLD = 10  # Example threshold for packet arrival rate (packets per second)
ALERT_THRESHOLD = 0.1  # Threshold for anomaly score

# Initialize Isolation Forest model
model = IsolationForest(contamination=ALERT_THRESHOLD)
anomaly_indices = []  # Initialize anomaly indices list

def calculate_arrival_rate():
    if len(arrival_times) < 2:
        return 0  # Not enough data points for calculation
    
    # Calculate time difference between first and last packet in the sliding window
    time_diff = arrival_times[-1] - arrival_times[0]
    return len(arrival_times) / time_diff if time_diff > 0 else 0

def plot_anomalies(packet_sizes, anomaly_indices):
    plt.figure(figsize=(10, 5))
    plt.hist(packet_sizes, bins=20, color='blue', alpha=0.7, label='Packet Sizes')
    plt.scatter(anomaly_indices, [packet_sizes[i] for i in anomaly_indices], color='red', label='Anomalies')
    plt.xlabel('Packet Size (bytes)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Packet Sizes with Anomalies')
    plt.legend()

    # Add text annotations for packet details
    for i in anomaly_indices:
        plt.annotate(f"Packet Size: {packet_sizes[i]} bytes", xy=(i, packet_sizes[i]), xytext=(i, packet_sizes[i] + 100),
                     arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.show()

def packet_callback(packet):
    arrival_times.append(time.time())  # Record arrival time of packet
    
    if packet.haslayer('IP'):
        src_ip = packet['IP'].src
        packet_size = len(packet)
        packet_sizes.append(packet_size)

        # Real-time anomaly detection based on packet arrival rate
        arrival_rate = calculate_arrival_rate()
        print(f"Packet arrival rate: {arrival_rate} packets/second")  # Print packet arrival rate
        if arrival_rate > THRESHOLD:
            print(f"Source IP: {src_ip}")
            print("High packet arrival rate detected! Potential anomaly.")
            # Print packet details
            print("Packet Details:")
            print(packet.summary())  # Print summary of packet details

            # Perform anomaly detection based on packet sizes
            if len(packet_sizes) >= 100:
                X = StandardScaler().fit_transform(packet_sizes[-100:])  # Scale features
                y_pred = model.fit_predict(X.reshape(-1, 1))  # Perform anomaly detection
                global anomaly_indices  # Declare anomaly_indices as global
                anomaly_indices = [i for i, pred in enumerate(y_pred) if pred == -1]
                if anomaly_indices:
                    print("Anomalies detected!")
                    print("Anomaly details:")
                    for idx in anomaly_indices:
                        print(f"Anomaly at index {idx}: Packet Size = {packet_sizes[idx]} bytes")

# Packet capture
sniff(prn=packet_callback, count=20)

# Plot anomalies
plot_anomalies(packet_sizes, anomaly_indices)
