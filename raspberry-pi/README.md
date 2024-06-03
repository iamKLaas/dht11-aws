# Raspberry Pi 

The Raspberry Pi is reading data from the DHT11 sensor and publishing it via MQTT to AWS IoT (Core). The connection between the Raspberry Pi and AWS IoT is secured with MTLS.

### Prerequisites
* Raspberry Pi is connected to the internet
* Packages are installed as given in [requirements.txt](./requirements.txt)
* DHT11 humidity and temperature sensor is connected to the Raspberry Pi
* Certificates created by the [Terraform Configuration](../terraform/main.tf) are present in the same directory as the DHT11.py script

### Instruction
The DHT11.py script can be ran by using the command "python3 DHT11.py $AWS_ENDPOINT" in the directory of the Python script. 
The $AWS_ENDPOINT argument needs to be replaced with the actual AWS endpoint the Raspberry Pi should connect to.

