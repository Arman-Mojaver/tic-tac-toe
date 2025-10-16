## Introduction
This project is a Tic Tac Toe API built with FastAPI and powered by PostgreSQL for persistent game data storage.

It leverages SQLAlchemy as the ORM for clean database interaction and is fully containerized using Docker and Docker Compose for seamless setup and deployment.

## Dependencies
In order to run the web application the following dependencies are required:

* Docker
* docker-compose

## Services
The services are listed in the `docker-compose.yaml` file. The project has the following services:
- webapp (including a CLI)
- db-development (PostgreSQL)
- db-production (PostgreSQL)
- db-testing (PostgreSQL)
- pgAdmin

## How to get started
In order to get started the following lines of code clone the repository and set up the project in one go (docker-compose required).
```
git clone https://github.com/Arman-Mojaver/tic-tac-toe.git
cd tic-tac-toe
make setup
```

Each step of the setup can also be done manually as follows (the following steps are not necessary if `make setup` is run):

1. Clone the repository:
```
git clone https://github.com/Arman-Mojaver/tic-tac-toe.git
```
2. Create an `.env` file:

Make a copy of `.env.example` and name it `.env`, or run:
```
make env-file
```

3. Build the image:
```
docker image build .
```
or
```
make build
```

4. Start the container using docker compose:
```
docker compose -f docker-compose.yaml up -d
```
or
```
make up
```
5. Run the database migrations
```
make alembic-upgrade
```
6. Open the API /docs page by going to `http://localhost:8000/docs`, or executing the following command:
```
make docs
```


## CLI
The CLI is accessed by opening up a bash shell inside the container, and typing `cli`.
1. Open a bash shell inside the container:
```
docker compose -f docker-compose.yaml exec -it webapp bash
```
or
```
make in
```
2. Execute the CLI:
```
cli
```

Example command:
```
cli utils info
```


## Environments
This project supports three runtime environments: `production`, `development` and `testing`. The active environment is selected by setting the `ENVIRONMENT` variable inside a `.env` file at the repository root. Docker Compose reads that `.env` file automatically and the variable is passed into containers so application code and entrypoints can branch behavior accordingly. The default environment is `development`.

In order to change between environments:
- change the `ENVIRONMENT` variable in .env
- Recreate the containers:
```
make down && make up
```


## Tests
In order to run the tests, run the following command:
```
make pytest
```

## Test coverage report
In order to run the tests and generate an HTML coverage report, run the following command:
```
make cov
```

## pgAdmin
pgAdmin is a Web UI to manage Postgres databases. In order to access it, go to http://localhost:8082/.
When accessing it for the first time, there will be no servers nor databases available. The information to access the servers is available in `config/` folder.


## Code Quality and Linting
This project maintains clean, consistent code using Ruff and pre-commit hooks.

Ruff is used for linting and formatting according to strict, performant Python standards.
The configuration rules for Ruff are defined in `pyproject.toml`.

Pre-commit hooks automatically run checks before each commit to ensure code style, formatting, and quality are enforced.
The hooks are configured in the `.pre-commit-config.yaml` file.

## Database Seeding
To populate the database with initial test data (such as default users), you can execute the following CLI command:
```
docker compose -f docker-compose.yaml run --rm -it webapp /bin/bash -c "cli seed"
```
or
```
make seed
```
