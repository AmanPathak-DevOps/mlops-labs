aws_region = "us-east-1"

project_name = "intent-classifier"

vpc_cidr = "10.0.0.0/16"

public_subnet_1_cidr = "10.0.1.0/24"
public_subnet_2_cidr = "10.0.2.0/24"

private_subnet_1_cidr = "10.0.11.0/24"
private_subnet_2_cidr = "10.0.12.0/24"

instance_type = "t3.micro"

key_name = "Aman-Pathak"

desired_capacity = 2
min_size = 1
max_size = 3