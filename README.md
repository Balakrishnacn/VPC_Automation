# VPC Automation with AWS Bedrock

This repository generates reviewed Terraform changes for an AWS VPC. It does
not apply infrastructure automatically: a workflow creates a branch and pull
request, and a human must approve and merge that pull request before a
separate, explicitly configured deployment process may apply it.

## Layout

- `modules/vpc` - reusable AWS VPC Terraform module.
- `generated/vpc` - generated root configuration that consumes the module.
- `scripts/generate_vpc_pr.py` - validates inputs, asks Amazon Bedrock for
  configuration values, renders Terraform, and opens a pull request.
- `.github/workflows/generate-vpc.yml` - manually triggered generation workflow.
- `.github/workflows/terraform-validate.yml` - formatting and validation only.
- `.github/workflows/terraform-apply.yml` - manually dispatched apply behind an
  environment reviewer gate.

## Generate a VPC pull request

Run the **Generate VPC Terraform PR** workflow with a manually supplied IPv4
CIDR such as `10.42.0.0/16`. You may also provide a natural-language request
such as “a small development VPC in us-east-1 with three availability zones”.
The CIDR is always validated locally and is passed explicitly to the reusable
module. The Bedrock model may choose only supported module settings; it cannot
write arbitrary workflow files or Terraform resources.

The workflow uses GitHub's OIDC token to assume the AWS role configured in
`AWS_ROLE_TO_ASSUME`. No long-lived AWS keys are stored in the repository.
The role needs permission to invoke the selected Bedrock model. The workflow
also needs the repository's `GITHUB_TOKEN` to create a branch and pull request.

## Approval and deployment safety

Configure branch protection on `main` to require pull-request review and the
Terraform validation check. The generation workflow intentionally has no
`terraform apply` command and no AWS provisioning permissions. The apply
workflow can only be manually dispatched from `main`, uses the separate
`terraform-apply` environment, and pauses for its required reviewers before
running. Configure that environment with the people who may approve
deployment, and set `AWS_APPLY_ROLE_TO_ASSUME` to a narrowly scoped role.

For local checks:

```bash
terraform -chdir=modules/vpc fmt -check -recursive
terraform -chdir=modules/vpc init -backend=false
terraform -chdir=modules/vpc validate
python -m unittest discover -s tests -v
```