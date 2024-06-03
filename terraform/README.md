# Terraform - AWS IoT Thing (Infrastructure) Setup

The Terraform configuration in this package will setup a AWS IoT thing with the name "raspberry-pi" in the provided AWS account and region.
The AWS IoT thing will be setup with a certificate that has a policy attached that allows to connect to AWS IoT Core and to publish messages on the topic "RaspberryPi".
The Terraform configuration will output the certificate "raspberry_pi_cert.pem" and the private key "raspberry_pi_private_key.pem" which are needed for the mutual TLS connection of the Raspberry Pi.

### Prerequisites 
* Terraform is installed 
* AWS_ACCESS_KEY_ID and AWS_SECRET_ACCES_KEY are exported as environment varibales 

### Instruction

Run the Terraform configuration with the 'terraform apply' command. Input variables can either be provided by creating a .tfvars file or command line/terminal options. 

Needed input variables are
* aws_region (default is "eu-central-1")
* aws_account_id

To destroy the setup infrastructure run the 'terraform destroy' command.