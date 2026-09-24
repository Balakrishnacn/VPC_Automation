module "vpc" {
  source = "../../modules/vpc"

  name = "generated-vpc"
  cidr = "10.42.0.0/16"
}
