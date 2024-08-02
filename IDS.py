from scapy.all import sniff, TCP, IP
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)

# Initialize a list to store captured packets
packets = []

# Define a callback function to process each captured packet
def packet_callback(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        packet_data = {
            'frame.number': packet[IP].id,
            'ip.src': packet[IP].src,
            'ip.dst': packet[IP].dst,
            'tcp.srcport': packet[TCP].sport,
            'tcp.dstport': packet[TCP].dport,
            'frame.len': len(packet),
            'ip.proto': packet[IP].proto,
            'tcp.flags.syn': int(packet[TCP].flags & 0x02 != 0),
            'tcp.flags.ack': int(packet[TCP].flags & 0x10 != 0),
            'tcp.flags.fin': int(packet[TCP].flags & 0x01 != 0),
            'ip.len': packet[IP].len,
            'tcp.window_size_value': packet[TCP].window,
            'tcp.analysis.bytes_in_flight': len(packet[TCP].payload),
            'tcp.analysis.push_bytes_sent': int(packet[TCP].flags & 0x08 != 0),
            'frame.time_epoch': datetime.fromtimestamp(packet.time)
        }
        packets.append(packet_data)

# Capture real-time traffic
sniff(filter="tcp", prn=packet_callback, store=0, count=100)

# Convert the list of packets to a pandas DataFrame
data = pd.DataFrame(packets)

# Drop unnecessary columns
columnsdrop = ["ip.src", "ip.dst", 'frame.number', 'frame.time_epoch']
df = data.drop(columns=columnsdrop, axis=1)

# Ensure the columns are in the same order as the training data
expected_columns = ['tcp.srcport', 'tcp.dstport', 'frame.len', 'ip.proto', 'tcp.flags.syn',
                    'tcp.flags.ack', 'tcp.flags.fin', 'ip.len', 'tcp.window_size_value',
                    'tcp.analysis.bytes_in_flight', 'tcp.analysis.push_bytes_sent']

df = df[expected_columns]

# Load the scaler and models
with open('allow2.pkl', 'rb') as f:
    scaler = pickle.load(f)

allow_model = tf.keras.models.load_model("autoencodeur2.h5")

with open('random_forest.pkl', 'rb') as f:
    RF = pickle.load(f)

with open('standardscalerclass.pkl', 'rb') as f:
    scalerclass = pickle.load(f)

# Initialize the traffic nature column
data['traficnature'] = 'unknown'
threshold = 0.033866014518787194  # Consider parameterizing this

try:
    # Preprocess data for GAN model
    dfgan = scaler.transform(df)
    dfgan = pd.DataFrame(dfgan, columns=df.columns)
    dfsansNan = dfgan[~dfgan.isin([np.nan, np.inf, -np.inf]).any(axis=1)]

    if dfsansNan.empty:
        data['traficnature'] = 'unknown'  
    else:
        allow_probs = allow_model.predict(dfsansNan)
        rmse_i = np.sqrt(np.sum((dfsansNan.values - allow_probs)**2, axis=1) / dfsansNan.shape[1])
        allow_mask_i = rmse_i > threshold

        if not any(allow_mask_i):
            data['traficnature'] = 'normal'
        else:
            df = scalerclass.transform(df)
            prediction = RF.predict(df)
            attack_types = ['httpflood', 'icmpflood', 'land', 'synflood', 'tcpflood', 'udpflood']
            data['traficnature'] = attack_types[prediction[0]]

except Exception as e:
    logging.error(f"Error during packet processing: {e}")

# Output the processed data
print(data.head())
