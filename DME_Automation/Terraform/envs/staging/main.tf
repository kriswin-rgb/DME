terraform {
  backend "s3" {
    bucket       = "terraform-state-daniyal"
    key          = "staging/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "terraform"
}


module "sg" {
  source = "../../modules/security_group"
  vpc_id = data.aws_vpc.default.id
  env    = "staging"
}


module "ec2" {
  source            = "../../modules/ec2"
  ami_id            = data.aws_ami.latest_amazon_linux.id
  instance_type     = "t3.micro"
  subnet_id         = data.aws_subnets.public.ids[0]
  security_group_id = module.sg.web_sg_id   
  key_name          = aws_key_pair.terraform_key.key_name
  env               = "staging"
}


module "alb" {
  source            = "../../modules/alb"
  subnet_ids        = data.aws_subnets.public.ids
  vpc_id            = data.aws_vpc.default.id
  security_group_id = module.sg.web_sg_id   
  instance_id       = module.ec2.instance_id
  env               = "staging"
}


