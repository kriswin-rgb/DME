variable "env" {
  description = "Environment name"
  type        = string
}

resource "aws_key_pair" "terraform_key" {
  key_name   = "terraform-key-${var.env}"
  public_key = file("/home/daniyal/Downloads/Terraform-project/id_rsa.pub")
}
