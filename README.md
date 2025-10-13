## CLI
The CLI is accessed by opening up a bash shell inside the container, and typing `cli`.
1. Open a bash shell inside the container:
```
docker compose -f docker-compose.yaml exec -it cli bash
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


## Tests
In order to run the tests, run the following command:
```
make pytest
```
