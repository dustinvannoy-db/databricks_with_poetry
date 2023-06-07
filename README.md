# databricks_with_poetry

This is a sample project for Databricks, generated via cookiecutter.

While using this project, you need Python 3.X and `pip` or `conda` for package management.

## How this repository was created
1. Use dbx to initialize project.
    ```
    dbx init \                                   
        -p "cicd_tool=GitHub Actions" \
        -p "cloud=AWS" \
    -p "project_name=databricks_with_poetry" \
    -p "profile=databricks_with_poetry" \
    --no-input
    ```
1. Move code around a little so that everything is under databricks_with_poetry directory.
1. Install poetry (ran from virtualenv)
    ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```
1. Add to `conf/deployment.yml`:
    ```
    build:
    no_build: true
    # python: "poetry"
    ``` 

1. Update pyproject.toml
    ```
    [tool.poetry]
    name = "databricks_with_poetry"
    version = "0.1.0"
    description = ""
    authors = ["dustinvannoy-db <dustin.vannoy@databricks.com>"]
    readme = "README.md"
    packages = [{include = "databricks_with_poetry"}]

    [tool.poetry.dependencies]
    python = "^3.9.0"
    urllib3 = "1.26.6"
    pandas = "1.4.4"
    scikit-learn = "1.1.1"


    [tool.poetry.group.dev.dependencies]
    databricks-connect = "13.0.0"
    chispa = "^0.9.2"
    pytest = "^7.0.0"
    dbx = "^0.8.0"

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    ```

1. Customized unit and integration tests.

1. Run `poetry install`
1. Run `poetry build`
1. Run `dbx deploy`
1. Run `dbx launch --trace databricks_with_poetry-sample-tests`


## Local environment setup

1. Instantiate a local Python environment via a tool of your choice. This example is based on `conda`, but you can use any environment management tool:
```bash
conda create -n databricks_with_poetry python=3.9
conda activate databricks_with_poetry
```

2. If you don't have JDK installed on your local machine, install it (in this example we use `conda`-based installation):
```bash
conda install -c conda-forge openjdk=11.0.15
```

3. Install project locally (this will also install dev requirements):
```bash
pip install -e ".[local,test]"
```

## Running unit tests

For unit testing, please use `pytest`:
```
pytest tests/unit --cov
```

Please check the directory `tests/unit` for more details on how to use unit tests.
In the `tests/unit/conftest.py` you'll also find useful testing primitives, such as local Spark instance with Delta support, local MLflow and DBUtils fixture.

## Running integration tests

There are two options for running integration tests:

- On an all-purpose cluster via `dbx execute`
- On a job cluster via `dbx launch`

For quicker startup of the job clusters we recommend using instance pools ([AWS](https://docs.databricks.com/clusters/instance-pools/index.html), [Azure](https://docs.microsoft.com/en-us/azure/databricks/clusters/instance-pools/), [GCP](https://docs.gcp.databricks.com/clusters/instance-pools/index.html)).

For an integration test on all-purpose cluster, use the following command:
```
dbx execute <workflow-name> --cluster-name=<name of all-purpose cluster>
```

To execute a task inside multitask job, use the following command:
```
dbx execute <workflow-name> \
    --cluster-name=<name of all-purpose cluster> \
    --job=<name of the job to test> \
    --task=<task-key-from-job-definition>
```

For a test on a job cluster, deploy the job assets and then launch a run from them:
```
dbx deploy <workflow-name> --assets-only
dbx launch <workflow-name>  --from-assets --trace
```


## Interactive execution and development on Databricks clusters

1. `dbx` expects that cluster for interactive execution supports `%pip` and `%conda` magic [commands](https://docs.databricks.com/libraries/notebooks-python-libraries.html).
2. Please configure your workflow (and tasks inside it) in `conf/deployment.yml` file.
3. To execute the code interactively, provide either `--cluster-id` or `--cluster-name`.
```bash
dbx execute <workflow-name> \
    --cluster-name="<some-cluster-name>"
```

Multiple users also can use the same cluster for development. Libraries will be isolated per each user execution context.

## Working with notebooks and Repos

To start working with your notebooks from a Repos, do the following steps:

1. Add your git provider token to your user settings in Databricks
2. Add your repository to Repos. This could be done via UI, or via CLI command below:
```bash
databricks repos create --url <your repo URL> --provider <your-provider>
```
This command will create your personal repository under `/Repos/<username>/databricks_with_poetry`.
3. Use `git_source` in your job definition as described [here](https://dbx.readthedocs.io/en/latest/guides/python/devops/notebook/?h=git_source#using-git_source-to-specify-the-remote-source)

## CI/CD pipeline settings

Please set the following secrets or environment variables for your CI provider:
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

## Testing and releasing via CI pipeline

- To trigger the CI pipeline, simply push your code to the repository. If CI provider is correctly set, it shall trigger the general testing pipeline
- To trigger the release pipeline, get the current version from the `databricks_with_poetry/__init__.py` file and tag the current code version:
```
git tag -a v<your-project-version> -m "Release tag for version <your-project-version>"
git push origin --tags
```
