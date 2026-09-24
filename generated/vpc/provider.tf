variable "aws_region" {
  description = "AWS region for the generated VPC."
  type        = string
  default     = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}
