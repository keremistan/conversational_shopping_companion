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
  key = each.value

  source_hash = filemd5("${local.data_contracts_folder_path}${each.value}")

  content_type = "application/json"
}
