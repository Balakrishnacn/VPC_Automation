output "id" {
  description = "The VPC ID."
  value       = aws_vpc.this.id
}

output "arn" {
  description = "The VPC ARN."
  value       = aws_vpc.this.arn
}

output "cidr_block" {
  description = "The configured VPC CIDR block."
  value       = aws_vpc.this.cidr_block
}
