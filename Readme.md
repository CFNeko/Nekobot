# What it is
This repository contains a bot created by Neko. 

## requirements
Have pip and python3 installed  
Have postgresQL installed on your computer.

## setup
- setup a venv (as per [this link](https://docs.python.org/3/library/venv.html#creating-virtual-environments)) and activate it
- `pip install -r requirements.txt`  
- Setup a postgresQL database, and import into it the data from `expanded_data.sql`
- rename the `.env.example` to `.env` and fill it with data needed to connect to your db.  
( Concerning the DISCORD_TOKEN key, fill it using your bot admin interface.)

## run
- activate your [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
- In the same shell, `python Neko.py`

## gotcha and other things that should be cleaned

ensure your cogs are ALL uppercase (or do what's recommanded by the TODO in Commands cog, help method)
