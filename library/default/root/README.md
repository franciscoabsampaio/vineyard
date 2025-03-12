## asasd

There are two tiers of Databricks workspaces:
- Standard. Requires a public IP.
- Premium. Allows for both public and private network implementations. In this project, premium workspaces will always generate private networking resources, such as private endpoints and private links. Regardless, users can still decide if they want to enable private frontends or not.

### root VS env

The repository and workflow are split into `root` and ``env`` for a few reasons:
- Users may want to deploy critical infrastructure (which, when destroyed, represents permanent business damage and loss of information) and non-critical environment-specific infrastructure from different environments. An example would be CI/CD pipelines in different environments, for each environment.
- Certain resources are unlikely to be redeployed/altered at a frequent rate. Others, such as cluster size, are more likely to be reconfigured.
- Sequential generation of the databricks resources per-environment would have required some very rough workarounds if dynamic `provider` blocks were not used. Using `for_each` arguments in `provider` blocks is only possible in OpenTofu 1.9.0 onwards. The Terraform version with which this repository was tested does not support dynamic `provider` blocks - and most likely no future version will.