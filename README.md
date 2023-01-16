# Michote - Starehe Yako

Michote is an online bus ticket booking service whose main goal is to provide convenience of booking a bus ticket without having to physically travel to the booking offices.

## About this repo

This repository contains all the dev work for the backend of this service. To view the frontend code, visit this link: [michote frontend](https://github.com/mkoner/michote_frontend).

## Installation

Clone this repository.

```bash
git clone https://github.com/RonCollins-MM/michote_backend.git
```

## Launch the server

Run the app with the following environment variables:

```bash
MICHOTE_MYSQL_PWD=@Michote_dev_123 MICHOTE_MYSQL_HOST=localhost MICHOTE_MYSQL_DB=michote_dev_db MICHOTE_TYPE_STORAGE=db MICHOTE_API_HOST=0.0.0.0 MICHOTE_API_PORT=5000 python3 -m api.v1.app
```

Then open another terminal instance and curl to the different routes. Example:

```bash
curl -X GET http://0.0.0.0:5000/api/v1/stats
```

__Note:__ Ensure you run the `setup_mysql_dev.sql` script to setup your database locally. See [here](./scripts/) for more details.
