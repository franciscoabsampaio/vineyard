# OpenTofu Or Terraform?

[OpenTofu](https://opentofu.org/) was forked from [HashiCorp Terraform](https://www.terraform.io/) and [officially endorsed by the Linux Foundation](https://www.linuxfoundation.org/press/announcing-opentofu)
in response to [HashiCorp's abrupt licensing changes to Terraform](https://opentofu.org/manifesto/).

Since, it's been growing rapidly and steadily, with both strong community and industry support, and industry giants like [Oracle have already made the switch](https://www.thestack.technology/oracle-dumps-terraform-for-opentofu/)
to Terraform's vegan alternative.

Thanks to the Linux Foundation's methodologies, OpenTofu has already seen the introduction of long-awaited new features.

**Of particular interest to this repository,** the ability to use the [`for_each` argument in `provider` blocks ](https://opentofu.org/docs/language/providers/configuration/#for_each-multiple-instances-of-a-provider-configuration) as of [version 1.9](https://opentofu.org/blog/opentofu-1-9-0/),
a significant milestone over Hashicorp's Terraform,
[which repeatedly refused the feature despite frequent community requests](https://support.hashicorp.com/hc/en-us/articles/6304194229267-Using-count-or-for-each-in-Provider-Configuration). Other examples of highly requested features being ignored or outright denied are [`depends_on` arguments on ``provider`` blocks](https://github.com/hashicorp/terraform/issues/2430), [direct support for single-instance resources](https://github.com/hashicorp/terraform/issues/30221), and [DynamoDB not being required in Terraform S3 backends](https://github.com/hashicorp/terraform/issues/35625) - [two of which are scheduled for the next version of OpenTofu](https://github.com/opentofu/opentofu/milestone/11) at the time of writing.
