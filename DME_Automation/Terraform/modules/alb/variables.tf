variable "subnet_ids" {
  type = list(string)
}
variable "vpc_id" {}
variable "security_group_id" {}
variable "instance_id" {}
variable "env" {
  type        = string
  description = "Environment name"
}
