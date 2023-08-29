data "databricks_current_user" "me" {
}

resource "databricks_git_credential" "global" {
  git_provider          = "gitHub"
  git_username          = var.repo_user_name
  personal_access_token = var.repo_pat
  force                 = true
}

resource "databricks_repo" "dlt_files_in_repos_in_user_home" {
  depends_on = [databricks_git_credential.global]
  url        = "https://github.com/dustinvannoy-db/databricks_with_poetry.git"
  path       = "${data.databricks_current_user.me.repos}/dlt-files-tf-dev"
  branch     = "dev"

  lifecycle {
    ignore_changes = [
      branch,
    ]
  }
}

# resource "databricks_repo" "dlt_files_in_repos_in_staging" {
#   depends_on = [databricks_git_credential.global]
#   url        = azuredevops_git_repository.repository.remote_url
#   path       = "${data.databricks_current_user.me.repos}/dlt-files-tf-staging"
#   branch     = "main"
#
#   lifecycle {
#     ignore_changes = [
#       branch,
#     ]
#   }
# }

# resource "databricks_repo" "dlt_files_in_repos_in_prod" {
#   depends_on = [databricks_git_credential.global]
#   url        = azuredevops_git_repository.repository.remote_url
#   path       = "${data.databricks_current_user.me.repos}/dlt-files-tf-prod"
#   branch     = "releases"
# }
