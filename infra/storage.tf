locals {
  data_contracts_folder_path = "${path.module}/../data_contracts/"
}

resource "aws_s3_bucket" "shopping_companion_bucket" {
  bucket = "shopping-companion-contracts-and-data-ingestion"
}

resource "aws_s3_object" "data_contracts" {
  bucket = aws_s3_bucket.shopping_companion_bucket.id

  for_each = fileset(local.data_contracts_folder_path, "**")

  source = "${local.data_contracts_folder_path}${each.value}"
  key    = each.value

  source_hash = filemd5("${local.data_contracts_folder_path}${each.value}")

  content_type = "application/json"
}

data "aws_iam_policy_document" "sns_file_creation_topic" {

  statement {
    effect = "Allow"

    principals {
      identifiers = ["s3.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sns:Publish"]

    resources = ["arn:aws:sns:*:*:s3-event-notification-topic"] # this resource's name must be the same as the "name" of aws_sns_topic resource. Otherwise, it throws error.

    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.shopping_companion_bucket.arn]
    }
  }
}

resource "aws_sns_topic" "file_creation_topic" {
  name   = "s3-event-notification-topic"
  policy = data.aws_iam_policy_document.sns_file_creation_topic.json
}

resource "aws_s3_bucket_notification" "bucket_notifications" {
  bucket = aws_s3_bucket.shopping_companion_bucket.id

  topic {
    topic_arn     = aws_sns_topic.file_creation_topic.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".log"
  }

  depends_on = [aws_sns_topic.file_creation_topic]
}
