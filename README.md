*Note: In its current state, this project is more of an MWE or proof-of-concept than a finished product.*

# Conduct

Conduct is a simple secrets management tool. Define all your secrets in an external configuration file, reference them in your codebase, and have them dynamically parsed into a temporary execution environment, removed upon completion of your command.

## Usage

- Store your secrets in a `secrets.yml` file in a location of your choice:

    ```yml
    MY_PASSWORD: "0penS3same"
    ```

- Throughout your codebase, place your secrets in string literals using `SECRET_` flags:

    ```python
    password = "SECRET_MY_PASSWORD"
    ```

- To execute your command, use `conduct`:

    ```bash
    $ conduct /path/to/secrets.yml "your command"
    ```

    e.g.,

     ```bash
    $ conduct ../secrets.yml "docker compose up --build --force-recreate -d"
    ```
