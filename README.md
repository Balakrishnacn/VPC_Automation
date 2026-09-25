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

The workflow authenticates with credentials supplied through GitHub Actions
secrets. Configure these repository or environment secrets:

- `AWS_ACCESS_KEY_ID` - required IAM access key ID.
- `AWS_SECRET_ACCESS_KEY` - required IAM secret access key.
- `AWS_SESSION_TOKEN` - optional session token for temporary credentials.

Set the optional `AWS_REGION` and `BEDROCK_MODEL_ID` as repository variables.
The credentials are passed only to the workflow's AWS configuration action and
are not written to files, Terraform configuration, generated branches, or pull
requests. For local use, export the same AWS environment variables before
running the generator; boto3 and the Terraform AWS provider read them without
requiring credentials in source code. Use a narrowly scoped IAM principal
with permission to invoke the selected Bedrock model, rotate keys regularly,
and never print or commit credential values. The workflow also needs the
repository's `GITHUB_TOKEN` to create a branch and pull request.

## Approval and deployment safety

Configure branch protection on `main` to require pull-request review and the
Terraform validation check. The generation workflow intentionally has no
`terraform apply` command and no AWS provisioning permissions. The apply
workflow can only be manually dispatched from `main`, uses the separate
`terraform-apply` environment, and pauses for its required reviewers before
running. Configure that environment with the people who may approve
deployment, and provide the same AWS credential secrets to that environment
or repository. The apply workflow uses them only after the environment's
required reviewers approve the manually dispatched run.

For local checks:

```bash
terraform -chdir=modules/vpc fmt -check -recursive
terraform -chdir=modules/vpc init -backend=false
terraform -chdir=modules/vpc validate
python -m unittest discover -s tests -v
```