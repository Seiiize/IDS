# Intrusion Detection System (IDS)

This project implements an Intrusion Detection System (IDS) that analyzes network packets in real-time using machine learning models. The project includes the necessary scripts and models to capture, preprocess, and classify network traffic to detect potential attacks.

## Project Overview

### Files and Their Purposes:

- **`IDS.py`**: The main script that captures network packets in real-time using Scapy, preprocesses them, and classifies them as normal or malicious using pre-trained machine learning models.

- **`GAN_Final.ipynb`**: Jupyter Notebook containing the training process for the Autoencoder model. This notebook includes all the steps required to build and train the Autoencoder model used for anomaly detection.

- **`Class.ipynb`**: Jupyter Notebook detailing the training process for the Random Forest model. This notebook covers the steps to build and train the Random Forest classifier used to identify specific types of attacks.

- **Model Files**:
  - **`autoencodeur.h5`**: The trained Autoencoder model used for anomaly detection.
  - **`random_forest.pkl`**: The trained Random Forest classifier model used for classifying attack types.
  - **`scaler.pkl`**: Scaler used for normalizing data before feeding it into the models.
  - **`scalerclass.pkl`**: Scaler used specifically for the Random Forest model.

## Important Notes

### Large Files

Due to GitHub's file size limits, some files are not included in this repository. Specifically, the dataset files are too large to be hosted on GitHub and should be obtained separately. You will need the following datasets to run the IDS system:

- **`Datasett.csv`**: [Dataset for training the models (261.31 MB)](link-to-download) (replace with actual download link if available)
- **`Data/udpfloodloi.csv`**: [Additional dataset (123.84 MB)](link-to-download) (replace with actual download link if available)

##Contributing
Feel free to contribute to this project by opening issues, submitting pull requests, or suggesting improvements. For any questions or issues, please contact your-email@example.com.

##License
This project is licensed under the MIT License - see the LICENSE file for details.
