provider "aws" {
  region = var.aws_region
}

resource "aws_iot_thing" "raspberry_pi" {
  name = "raspberry-pi"
}

resource "aws_iot_certificate" "raspberry_pi_cert" {
  active = true
}

resource "aws_iot_thing_principal_attachment" "att" {
  principal = aws_iot_certificate.raspberry_pi_cert.arn
  thing     = aws_iot_thing.raspberry_pi.name
}

resource "aws_iot_policy_attachment" "policy_att" {
  policy = aws_iot_policy.pub_raspberry_pi_topic.name
  target = aws_iot_certificate.raspberry_pi_cert.arn
}

resource "local_file" "raspberry_pi_cert_private_key" {
    content  = aws_iot_certificate.raspberry_pi_cert.private_key
    filename = "raspberry_pi_private_key.pem"
}

resource "aws_iot_policy" "pub_raspberry_pi_topic" {
  name = "PubToRaspberryPiTopic"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "iot:Publish",
        ],
        "Resource" : [
          "arn:aws:iot:${var.aws_region}:${var.aws_account_id}:topic/RaspberryPi"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "iot:Connect"
        ],
        "Resource" : [
          "arn:aws:iot:${var.aws_region}:${var.aws_account_id}:client/${aws_iot_thing.raspberry_pi.name}"
        ]
      }
    ]
  })
}

variable "aws_region" {
  type        = string
  description = "AWS Region where the resources shall be deployed"
  default     = "eu-central-1"
}

variable "aws_account_id" {
  type        = string
  description = "Account ID of your AWS account"
}
