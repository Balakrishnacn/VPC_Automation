variable "name" {
  description = "Name prefix applied to the VPC and its default resources."
  type        = string

  validation {
    condition     = can(regex("^[A-Za-z0-9][A-Za-z0-9-]{0,62}$", var.name))
    error_message = "name must be 1-63 characters, start with a letter or digit, and contain only letters, digits, and hyphens."
  }
}

variable "cidr" {
  description = "Manually supplied IPv4 CIDR block for the VPC."
  type        = string

  validation {
    condition     = can(cidrnetmask(var.cidr)) && tonumber(split("/", var.cidr)[1]) >= 16 && tonumber(split("/", var.cidr)[1]) <= 28
    error_message = "cidr must be a valid IPv4 network between /16 and /28."
  }
}

variable "enable_dns_support" {
  description = "Whether DNS resolution is supported in the VPC."
  type        = bool
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Whether DNS hostnames are assigned to instances in the VPC."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags to apply to the VPC."
  type        = map(string)
  default     = {}
}
