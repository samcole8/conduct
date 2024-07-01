*Note: In its current state, this project is more of an MWE or proof-of-concept than a finished product.*

# Conduct

Conduct is a secrets management tool and wrapper for Docker Compose. Define all your secrets in an external configuration file, reference them in your codebase, and have them dynamically parsed into a temporary build environment.

## Usage

- Store your secrets in a `secrets.yml` file in a location of your choice:

    ```yml
    MY_PASSWORD: "0penS3same"
    ```

- Throughout your codebase, place your secrets in string literals using `SECRET_` flags:

    ```python
    password = "SECRET_MY_PASSWORD"
    ```

- To deploy, use `conduct` instead of `docker-compose up`:

    ```bash
    $ conduct /path/to/secrets.yml <docker-compose arguments>
    ```
    e.g.,
     ```bash
    $ conduct ../secrets.yml --build --force-recreate -d
    ```
