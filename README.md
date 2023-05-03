# Low-cost medical health-care monitoring system IoT-based using fog computing

This project constitutes a component of the implementation of my thesis. Initially, we provide an overview of the project in the introduction section and proceed to discuss the Python codes utilized therein.

## **Introduction**

Today, providing healthcare services is becoming increasingly challenging due to the growing population and rising costs
of medical treatments and center expenses. In Iran, rural areas are particularly affected by the lack of appropriate
medical services. However, the progress of Internet of Things (IoT) technology has shown promise in improving some of
these issues, especially in reducing treatment costs.
To address these challenges, our research proposes a low-cost medical healthcare monitoring system based on IoT using
fog computing. We implemented an ECG machine based on this architecture that can be used for both ECG and heart
monitoring. Our system can store recorded ECG data of patients in cloud storage for use by expert physicians.
Additionally, our system can monitor heart rate variability (HRV) using fog computing technology. If a patient’s heart
condition becomes abnormal, it can send a notification through three channels: internet, local network, and short
message.
Experimental testing and comparisons have shown that our system has high accuracy and reliability. We tested the
system with a real ECG device on four healthy individuals and achieved an accuracy rate of 98.17.

The figure below illustrates the architecture of this project.

![](https://s8.uupload.ir/files/picture1_uy09.jpg)




## Step 1 (Preparation Patient)

In this step, we prepare the patient to obtain data from their ECG node, as illustrated in the figure below.

![](https://s8.uupload.ir/files/picture2_tr2c.jpg)


## Step 2 (Connecting ECG module to Arduino)

In this step, the ECG module AD 8232 is utilized to obtain ECG data. The data received from this module is in analog format, and thus requires conversion to a digital signal for processing. The figure below demonstrates how to connect the module to Arduino.

![](https://s8.uupload.ir/files/picture3_hm1q.jpg)


## Step 3 (Filtering and Analyze data in FOG node)

Following the acquisition and conversion of data from Arduino, Raspberry Pi serves as a fog node. The processes involved in the operation of the fog node are divided into multiple steps, including:

Step 1 (GetingRAWdata.py):
* Reading data from the Arduino via the serial port.

Step 2 (heartbeat.py):
* Filtering data
* Detecting peaks in heart rate
* Identifying abnormal heart rate patterns

Step 3 (main.py):
* Generating plot
* Preparing data for transmission to the cloud

Step 4 (SenDataToCould.py):
* Transmitting processed data to Firebase for real-time monitoring.


Indeed, these files are the primary and crucial components of the project. Once executed, the figure below displays a sample of the ECG signal.

![](https://s8.uupload.ir/files/picture4_6z15.png)

***
# The operational mechanism of the device

The proposed device functions as both an ECG device and a heart monitoring system. In ECG mode, the device is activated for a specific duration to obtain ECG data. If the device is connected to the internet, the data can be uploaded to the internet and simultaneously saved in local storage. In the event of an internet connection failure, the data is only saved locally. The flow chart for ECG mode is presented below.

![](https://s8.uupload.ir/files/picture5_mbcb.jpg)


Regarding heart monitoring, the device obtains patient data and conducts real-time analysis as shown in the flow chart below. If the abnormality detection system attempts to connect to the internet and successfully establishes a connection, the LED embedded in the device turns red, and a notification is transmitted to the doctor via the cloud and SMS. If the connection is lost, the LED turns red, and an SMS is sent. During this period, the doctor can monitor the patient's heart rate on the local network and online.

![](https://s8.uupload.ir/files/picture6_192o.jpg)


# GUI

The gui.html file provides a basic demonstration of ECG monitoring using FLASK to retrieve data from a real-time database (Firebase) and display it for the purpose of monitoring a patient's heart rate. The picture below displays the graphical user interface (GUI).

![](https://s8.uupload.ir/files/ecg-monitoring_v8k9.gif)




