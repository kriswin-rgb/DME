output "web_sg_id" {
  value = aws_security_group.this.id
}

output "rds_sg_id" {
  value = aws_security_group.rds_sg.id
}
