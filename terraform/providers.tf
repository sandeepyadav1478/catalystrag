terraform {
  required_version = "1.5.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.18.0"
    }
  }
}

provider "aws" {
  profile = "default"
  alias = "dev"
}