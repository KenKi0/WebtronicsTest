# Webtronics Test

# Getting Started

## Run docker compose.
### Prerequisites
* Docker **20.10.21**

1. Clone the repo.
   ```sh
   $ git clone git@github.com:KenKi2002/WebtronicsTest.git
   ```
2. Define environment variables.  
    Create .env file in the root of project and fill it in like .env.sample.  
    NOTE: set pg_host as db is reqiered

3. Build and run docker compose by predefined `make` command.
    ```sh
    $ make app
    ```


## Run as python script.
### Prerequisites

* python **3.10.2**
* poetry


### Installation

1. Clone the repo.
   ```sh
   $ git clone git@github.com:KenKi2002/WebtronicsTest.git
   ```
2. Activate virtual environment.
   ```sh
   $ poetry init
   $ poetry shell

3. Install requirements.
    ```sh
   (venv) $ poetry install
   ```

4. Define environment variables.  
    Create .env file in the root of project and fill it in like .env.sample
    
5. Migrate database.
    ```sh
   (venv) $ alembic upgrade head
   ```

6. Run service.
    ```sh
   (venv) $ python -m bin run
   ```
