resource "aws_key_pair" "terraform_key" {
  key_name   = "terraform-key"
  public_key = file("/home/daniyal/Downloads/Terraform-project/id_rsa.pub")
}
