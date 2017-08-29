"""Configuration settings for the pain api."""
# -*- coding: utf-8 -*-
from logging import basicConfig, DEBUG
from os import path
from invoke import run

LOG_FILE_PATH = '/tmp/pain_data.log'
LOG_LEVEL = DEBUG
MAIN_NAME = '__main__'
basicConfig(filename=LOG_FILE_PATH, level=LOG_LEVEL)
WEATHER_ID = '3d0b141357a6842ab0f3a42a9192a836'
DEFAULT_ZIP = '78681'
PA_ZIP_CODE = '17404'
PAIN_LEVEL_QUESTION = 'Enter your current pain level[0-10]: '
PAIN_INVALID_MESSAGE = 'Please enter a valid pain level value.'
INVALID_PAIN_INPUT_MESSAGE = 'Invalid pain level. Pain level must be 0-10.'
INVALID_PAIN_INPUT_EXCEPTION = ValueError(INVALID_PAIN_INPUT_MESSAGE)
ERROR_SAVING_DATA_MESSAGE = 'Unable to save the pain data. Check the logs.'
SAVING_MESSAGE = 'Saving the pain and weather data...'
SAVING_COMPLETE_MESSAGE = 'Save complete!'
# Options are: imperial and metric. Standard for kelvin.
DEFAULT_UNITS = 'imperial'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?' \
          'zip={zip_code},' \
          'us&appid={app_id}&units={units}'
HOME_PATH = path.expanduser('~')
DATA_DIRECTORY = path.join(HOME_PATH, 'data')
run('mkdir -p {directory}'.format(directory=DATA_DIRECTORY))
DB_FILE_NAME = 'pain.db'
DB_FILE_PATH = path.join(DATA_DIRECTORY, DB_FILE_NAME)
CREATE_TABLE_QUERY = "CREATE TABLE IF NOT EXISTS pain(" \
                     "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                     "date TEXT, pain_level TEXT, city TEXT, " \
                     "temperature TEXT, " \
                     "pressure TEXT, humidity TEXT, min_temp TEXT, " \
                     "max_temp TEXT, conditions TEXT);"
INSERT_PAIN_QUERY = "INSERT INTO pain(date, pain_level, city, temperature, " \
                    "pressure, humidity, min_temp, max_temp, conditions) " \
                    "VALUES (date('now'),'{pain_level}','{city}','{temp}'," \
                    "'{pressure}','{humidity}','{min_temp}'," \
                    "'{max_temp}','{conditions}');"
SELECT_PAIN_ITEMS_QUERY = "SELECT * FROM pain;"
SELECT_PAIN_ITEM_COUNT_QUERY = "SELECT count(*) FROM pain;"
TEST_DB_PATH = 'test.db'
TEST_CITY_TX_NAME = 'Round Rock'
TEST_CITY_PA_NAME = 'York'
TEST_STRING_CONTAINS = 'Temp:'
