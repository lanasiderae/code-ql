# This file is intentionally written to test Semgrep rules that block tflint-ignore usage on MSK rules.

# ❌ Should trigger: enforce-msk-topic-name
# rule-id: enforce-msk-topic-name
# reason: Testing that ignoring `msk_topic_name` is caught.
# expect-error: "The MSK topic name rule must always be followed. You can define additional team aliases"
# tflint-ignore: terraform_msk_topic_name
resource "aws_msk_topic" "bad_example_1" {
  name = "invalid-topic-name"
}

# ❌ Should trigger: enforce-msk-app-topics
# rule-id: enforce-msk-app-topics
# reason: Testing that ignoring `msk_app_topics` is caught.
# expect-error: "TLS apps in the MSK configuration must be defined the module they produce/consume on"
# tflint-ignore: terraform_msk_app_topics
resource "aws_msk_topic" "bad_example_2" {
  name = "app-topic"
}

# ❌ Should trigger: enforce-msk-app-consume-groups
# rule-id: enforce-msk-app-consume-groups
# reason: Testing that ignoring `msk_app_consume_groups` is caught.
# expect-error: "TLS apps in the MSK configuration must prefix all consume_groups with the team name"
# tflint-ignore: terraform_msk_app_consume_groups
resource "aws_msk_configuration" "bad_example_3" {
  name           = "bad-config"
  kafka_versions = ["2.8.1"]
}
