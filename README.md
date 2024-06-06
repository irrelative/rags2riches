# Rags2Riches

* Data from https://archive.org/details/stackexchange
* https://archive.org/download/stackexchange/history.stackexchange.com.7z


## Getting Started, loading initial data

1. Set up venv, pip install requirements.txt
1. Download data and extract to local `data` directory
1. Create a postgres db named `rags`
1. Run `schema.sql` into that database.
1. Run `init_data.py`
