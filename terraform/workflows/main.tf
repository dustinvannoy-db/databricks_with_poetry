terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

provider "databricks" {
  alias = "ws1"
  host  = "https://e2-demo-west.cloud.databricks.com"
  token = var.pat_ws_1
}

provider "databricks" {
  alias = "ws2"
  host  = "https://e2-demo-west-prod.cloud.databricks.com/"
  token = var.pat_ws_2
}
