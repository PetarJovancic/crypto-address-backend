# crypto-address-backend

Backend server for a generating crypto adresses.
Service covers following coins:
"BTC", "ETH", "QTUM", "LTC", "DOGE"

<img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"
     alt="Markdown Python icon"
     height="30px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://cdn.onlinewebfonts.com/svg/img_437027.png"
     alt="Markdown Flask icon"
     height="30px"
/>&nbsp;&nbsp;
<img src="https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg"
     alt="Markdown Postgres icon"
     height="30px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://www.docker.com/sites/default/files/d8/2019-07/horizontal-logo-monochromatic-white.png"
     alt="Markdown Docker icon"
     height="30px"
/>

## Usage

The app requires an `.env`. file with the following variables:

```
DATABASE_URL=postgresql://<username>:<password>@<database_url>:<port>/<database_name>
SECRET_KEY=<flask-secret-key>
JWT_SECRET_KEY=<jwt-secret-key>
JWT_ALGORITHM=<jwt-algorithm>
WALLET_LANGUAGE=<language>
WALLET_STRENGTH=<integer>
PASSPHRASE_LENGHT=<integer>
KEYS_CONFIG_FILE=<config-file-dir>
```

Examples are given in .env.example file in the repository

### Without Docker

Before starting make sure you created postgres database and created .env.
It is advised to work in a virtual environment. Create one using the following command:

```
python3 -m venv venv
```

Activating **venv**:

- Windows OS: `./venv/Scripts/activate`
- Unix/Mac OS: `source venv/bin/activate`

Install the required packages into the newly created venv:

```
pip install -r requirements.txt
```

Run the following commands to setup the tables in your database:

```
flask db init
flask db migrate
flask db upgrade
```

To start the server run:

```
flask run
```

### Using Docker

There are two separate Docker containers, one for hosting the Postgres database and the other one for Flask service.
At the moment there is issue connecting flask service to the postgres service

To build and run containers execute:

```
docker-compose up --build --remove-orphans
```

## Test

Tests are not yet implemented:

## Manual Testing

To test endpoints import 'Crypto API.postman_collection.json' file into Postman.

System works the following way:

```
Step1: User needs to be registered
Step2: Login user and retrieve access token
Step3: Use access token to get Auth and create new account for the user
Step4: Generate crypto address of your chosing for that account
Step5(Optional): Retrieve all the addresses
Step5(Optional): Retrieve address by address ID
```
