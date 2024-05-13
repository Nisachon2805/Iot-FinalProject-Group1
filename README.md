# IoT Final Project Description 
This is a guideline for students who enroll in 2102541 IoT Fundamental Course (academic year 2023)

Class Instructors:

- Assoc. Prof. Chaodit Aswakul (https://ee.eng.chula.ac.th/chaodit-aswakul/)
- Assoc. Prof. Wanchalerm Pora (https://ee.eng.chula.ac.th/wanchalerm-pora/)

Department of Electrical Engineering, Faculty of Engineering, Chulalongkorn University, Thailand

This repository was created by Patchapong Kulthumrongkul 6670165121@student.chula.ac.th
Wireless Network and Future Internet Research Unit, Department of Electrical
Engineering, Faculty of Engineering, Chulalongkorn University, Bangkok Thailand

---

## System Architecture
![Alt text](/Diagram.svg)
![Alt text](/Dataflow.svg)
The primary objectives of this project include designing and implementing a full-stack IoT system and deploying all services to run in a real operating environment. Therefore, collaboration with teammates is essential to develop a comprehensive system, utilizing GitHub as our workspace for development.

### System components
#### - ESP32
  - ESP32 collects the data from attached sensors and publish the data to a sensor gateway via MQTT.
  - ESP32 receives the command by subscribing the topic that is used to send command from other services and send the command to the actuators.

#### - Raspberry Pi (Sensor Gateway)
  - **MQTT Broker**
    - The broker facilitates communication among IoT devices within the local area network (Wi-Fi) 
  **Note:** ESP32 boards and Raspberry Pi must connect to the same Wi-Fi network to be within the same local area network (LAN).
    - For the EMQX MQTT broker (ref: [EMQX](https://www.emqx.io/)), you can configure the broker through port 18083, while the common MQTT port is 1883.
  - **Consumer**
    - Python script listens to messages published to the broker and writes that data into an InfluxDB database.
    - If you wish to provide real-time streaming data to the analytics component, you can accomplish this directly here as well.
  - **Command Center**
    - If your analytics service controls actuators, you can utilize the Command Center to poll action data from the database and publish commands to the MQTT broker.
  - **Docker Container**
    - All services operating on the Raspberry Pi must run as Docker images, necessitating the containerization of all applications within the Raspberry Pi.
#### - IoTCloudServe@TEIN ([GitHub](https://github.com/IoTcloudServe))
  - **InfluxDB**
    - InfluxDB is a time-series database designed for collecting streaming data from IoT sensors.
    - InfluxDB is running on port 8086.
    - You can read and write data using InfluxDB client library. (ref: [InfluxDB client library](https://docs.influxdata.com/influxdb/v1/tools/api_client_libraries/))
  - **Data Analytics**
    - After you have collected data from IoT devices, you can leverage that data to derive more meaningful insights.
    - You can develop regression or classification models to predict outputs by learning from the collected data.
    - Once your model is prepared for prediction, utilize real-time data fed from the Consumer to perform real-time predictions.
  - **Website UI** (optional)
    - You can utilize the InfluxDB UI for visualization without needing to implement anything
    - Additionally, you can employ other visualization services such as Grafana.
    - Alternatively, you have the option to design your own simple web application using both backend and frontend technologies.
  - **Docker Container & Rancher**
    - All services operating on the cloud must run as Docker images, necessitating the containerization of all applications within the laptop.
    - Once you have obtained the images, you will need to deploy them on Rancher, a management platform for Kubernetes clusters.
    - Additionally, you'll need to map the services to the outside world using Domain Name System (DNS).
  
**Noted that all of your source code must be pushed to your group's public GitHub repository.**

All members should be able to utilize commands such as git add, commit, push, and pull to communicate between your local repository and the public GitHub repository. [Git Tutorial by w3schools](https://www.w3schools.com/git/)


## Member Responsibilities

This project requires four members to collaborate on system development, each assigned to main specific roles: 
### 1. Hardware Programming(6430406721 Satchukan Sinsuwanrak)
Develop software embedded in ESP32 to interface with sensors and actuators on the board and communicate with an MQTT broker.

#### Recommended Skills
Arduino Programming, Hardware Communication and Networking, MQTT, FreeRTOS

#### Milestones
- **Design Workflow:** Outline the structure and flow of programs running on the ESP32, considering sensor data acquisition, actuator control, and MQTT communication. Ensure that tasks are designed to run concurrently using FreeRTOS to optimize performance.

- **Sensor Integration:** Successfully read data from sensors connected to the ESP32 board, ensuring accurate and reliable sensor readings.

- **Actuator Control:** Implement control mechanisms to manipulate actuators based on input from the ESP32 software, demonstrating effective actuator operation.

- **MQTT Communication:** Establish communication with an MQTT broker, enabling the ESP32 to publish sensor data and subscribe to commands from the broker.

- **Bidirectional Communication:** Develop functionality to send sensor data to the MQTT broker and receive commands from the broker, ensuring bidirectional communication capability.

- **Concurrency Implementation:** Implement multitasking using FreeRTOS to execute sensor reading, actuator control, MQTT communication, and other tasks concurrently, optimizing performance and responsiveness.

- **Version Control:** Upload all code to a common git repository, ensuring proper version control and collaboration among team members, facilitating code sharing and review.
  
#### Useful Resources
- The projects you had completed for the assignment.
  
### 2. Database & Visualization(6432091021 Nisachon Sillapawongsa)
- Handle reading from and writing to the database, as well as managing data for visualization.

#### Recommended Skills 
MQTT, Python Programming, Data Queurying, REST API, User Interface

#### Milestones
- **Design and MQTT Integration:** Develop schemes for data collection from MQTT messages, connect to the MQTT broker, subscribe to relevant topics, ensure proper authentication, and manage topic subscriptions from the database management software.

- **Data Acquisition and Testing (Consumer):** Listen to designed MQTT topics, process incoming data, store it in the database by using InfluxDB client library, and conduct functionality testing to ensure correct data handling.

- **Data Querying:** Use InfluxDB client library to query data for other services in your systems (i.e. Data Analytics)

- **Command Center:** Develop a component to periodically poll commands from the database and publish them to the MQTT broker to control the actuators or trigger specific actions based on real-time data analysis results. 

- **Visualization Development (Website UI):** Develop visualization methods to represent collected data effectively. Available methods are shown in "Website UI" section.

- **Version Control:** Upload all code to a common git repository, ensuring proper version control and collaboration among team members, facilitating code sharing and review.

#### Useful Resources
- Example of consumer file: [Python MQTT Tutorial: Store IoT Metrics with InfluxDB](https://thenewstack.io/python-mqtt-tutorial-store-iot-metrics-with-influxdb/?utm_content=buffer401c3&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer)
- InfluxDB client library for readind and writing data: [InfluxDB client libraries](https://docs.influxdata.com/influxdb/v1/tools/api_client_libraries/)
- Develop Grafana dashboard using data from InfluxDB [Get started with Grafana and InfluxDB](https://grafana.com/docs/grafana/latest/getting-started/get-started-grafana-influxdb/) 
  
### 3. Data Analytics(6430117321 Natwara Wongrujirawanich)
Utilize the collected data from the system to construct a machine learning model, such as classification or regression.

#### Recommended Skills
Python Programming, Data Preprocessing, Data Analysis, Machine Learning, Model Evaluation and Optimization

#### Milestones
- **Data Analysis:** Conduct an in-depth analysis of the collected data to understand its characteristics and distributions.

- **Data Retrieval:** Utilize database integration to fetch data, leveraging the resources provided by the Database team member.

- **Data Cleaning:** Preprocess the data to handle missing values, outliers, and inconsistencies.

- **Feature Description & Analysis:** Describe and analyze features within the dataset to identify patterns and correlations.

- **Objective Definition:** Define clear objectives for the analysis, specifying the intended outcomes and metrics for evaluation.

- **Model Selection:** Choose appropriate machine learning models (e.g., regression, classification, or unsupervised learning) based on the defined objectives.

- **Model Training, Validation, and Testing:** Train, validate, and test the selected model to ensure robust performance and generalization capabilities.

- **Real-time Prediction Application:** Implement the trained model to make real-time predictions, aligning with the defined objectives of the analysis.

- **Version Control:** Upload all code to a common git repository, ensuring proper version control and collaboration among team members, facilitating code sharing and review.

#### Useful Resources
- Lecture slides in MCV
- Example of performimg real-time prediction using python [Performing Real-Time Predictions Using Machine Learning, GridDB and Python](https://griddb.net/en/blog/performing-real-time-predictions-using-machine-learning-griddb-and-python/)

### 4. Edge & Cloud Operator(6670125021 Nonthaphan Limpongsanurak)
   Containerize applications including MQTT broker, database, and analytics for deployment on both edge and cloud nodes.
#### Recommended Skills
Linux Command, Docker Containerization, Service Deployment on Rancher, Networking and Security, Domain Name System 

#### Milestones
- **Gateway Setup (Raspberry Pi):** Configure the Raspberry Pi as the gateway device, enabling SSH access and setting up the hostname for identification.

- **Docker Installation:** Install Docker on the gateway device to facilitate containerization of applications.

- **MQTT Broker Setup:** Pull the EMQX image from Docker Hub and run it as an MQTT broker, mapping ports 1883 and 18083 for communication and management.

- **MQTT Service Testing:** Verify the functionality of the MQTT service using client programs such as MQTTBox, Postman, or MQTT Explorer.

- **Program Containerization:** Containerize all the applications as Docker images to ensure portability and ease of deployment.

- **Image Deployment on Gateway:** Deploy the containerized images, including the MQTT broker, Command Center, Consumer, etc., on the gateway device for local data processing. Verify container deployment and monitor resource utilization.

- **Image Deployment on Cloud:** Deploy the containerized images, including InfluxDB, Data Analytics, etc., on the IoTCloudServe@TEIN for centralized data processing and analytics. Configure cloud server settings and monitor container health.

- **Version Control:** Upload all code to a common git repository, ensuring proper version control and collaboration among team members, facilitating code sharing and review.

#### Useful Resources
- Setting up SSH and hostname in Raspberry Pi [Connecting to your Raspberry Pi via SSH](https://raspberrypi-guide.github.io/networking/connecting-via-ssh#connecting-via-ssh) - Docker Installation on Raspberry Pi [Here's How to Install Docker on Raspberry Pi?](https://www.simplilearn.com/tutorials/docker-tutorial/raspberry-pi-docker)
- [Install EMQX MQTT broker using Docker](https://www.emqx.io/docs/en/latest/deploy/install-docker.html)
- [Containerize application](https://docs.docker.com/get-started/02_our_app/)
- [Deploying Workloads on Rancher](https://ranchermanager.docs.rancher.com/v2.0-v2.4/how-to-guides/new-user-guides/kubernetes-resources-setup/workloads-and-pods/deploy-workloads)
