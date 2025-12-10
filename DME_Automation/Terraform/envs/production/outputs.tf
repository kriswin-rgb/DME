output "ec2_ip" {
  value = module.ec2.public_ip
}

output "alb_dns" {
  value = module.alb.alb_dns_name
}
