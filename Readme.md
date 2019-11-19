# What it is
This repository contains a bot created by Neko. I currently have the data to setup a pgsql
database to run it.

##requirements
Have pipenv and python3 installed
Have postgresQL installed on your computer.

## setup
`pipenv install`
Setup a postgresQL database, and import into it the data from `expanded_data.sql`
rename the `.env.example` to `.env` and fill it with data needed to connect to your db.
Concerning the DISCORD_TOKEN key, fill it using your bot admin interface.
