
data "aws_bedrock_foundation_model" "gpt_oss_20b" {
  model_id = "openai.gpt-oss-20b-1:0"
}

resource "aws_bedrock_inference_profile" "gpt_profile" {

  name        = "OSS GPT 20b"
  description = "The OSS GPT 20b model"

  model_source {
    copy_from = data.aws_bedrock_foundation_model.gpt_oss_20b.model_arn
  }

  tags = {
    "project" : "Conversational Shopping"
    "environment" : "Development"
  }

}

output "gpt_oss_inference_profile_arn" {
  value = aws_bedrock_inference_profile.gpt_profile.arn
}
