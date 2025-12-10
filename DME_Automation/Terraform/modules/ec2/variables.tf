variable "ami_id" {}
variable "instance_type" {}
variable "subnet_id" {}
variable "security_group_id" {}
variable "key_name" {
  type        = string
  description = "SSH key name to access the EC2 instance"
}
variable "env" {
  type        = string
  description = "Environment name (staging/production)"
}
