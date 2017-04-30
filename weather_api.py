"""Class for getting weather using a web api."""
# -*- coding: utf-8 -*-
from logging import getLogger
from sqlite3 import connect
from requests import get
from settings import API_URL, DEFAULT_ZIP, WEATHER_ID, DEFAULT_UNITS, \
    DB_FILE_PATH, INSERT_PAIN_QUERY, CREATE_TABLE_QUERY, \
    INVALID_PAIN_INPUT_EXCEPTION, SELECT_PAIN_ITEMS_QUERY, \
    SELECT_PAIN_ITEM_COUNT_QUERY


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class PainData(object):
    """Type to represent weather data."""
    WEATHER_STRING = \
        '{city} - Temp: {temperature}, Pressure: {pressure}, ' \
        'Humidity: {humidity}, Min_Temp: {min_temp}, Max_Temp: {max_temp}, ' \
        'Conditions: {conditions}'
    WEATHER_KEY = 'weather'
    CONDITION_KEY = 'description'
    MAIN_KEY = 'main'
    CITY_KEY = 'name'
    TEMP_KEY = 'temp'
    PRESSURE_KEY = 'pressure'
    HUMIDITY_KEY = 'humidity'
    TEMP_MIN_KEY = 'temp_min'
    TEMP_MAX_KEY = 'temp_max'

    @property
    def conditions(self):
        """Returns a string for concatenated conditions."""
        return ', '.join(self._conditions)

    def __init__(self, weather_json=None):
        """Initializer for weather data."""
        self.city = None
        # Temperature.Unit Default: Kelvin, Metric: Celsius,
        # Imperial: Fahrenheit.
        self.temperature = None
        # Atmospheric pressure (on the sea level,
        # if there is no sea_level or grnd_level data), hPa
        self.pressure = None
        # Humidity, %
        self.humidity = None
        self.min_temperature = None
        self.max_temperature = None
        self._conditions = list()
        if weather_json:
            self.city = weather_json[self.CITY_KEY]
            self.temperature = weather_json[self.MAIN_KEY][self.TEMP_KEY]
            self.pressure = weather_json[self.MAIN_KEY][self.PRESSURE_KEY]
            self.humidity = weather_json[self.MAIN_KEY][self.HUMIDITY_KEY]
            self.min_temperature = weather_json[
                self.MAIN_KEY][self.TEMP_MIN_KEY]
            self.max_temperature = weather_json[
                self.MAIN_KEY][self.TEMP_MAX_KEY]
            for condition in weather_json[self.WEATHER_KEY]:
                self._conditions.append(condition[self.CONDITION_KEY])

    def __str__(self):
        """Override for printing weather data."""
        return self.WEATHER_STRING.format(
            city=self.city, temperature=self.temperature,
            pressure=self.pressure, humidity=self.humidity,
            min_temp=self.min_temperature, max_temp=self.max_temperature,
            conditions=self.conditions)

    def __repr__(self):
        """Override for repr."""
        return self.__str__()

    @staticmethod
    def _execute_simple_query(query, pain_database=DB_FILE_PATH):
        """Execute no parameter queries and return results."""
        getLogger(__name__).debug(query)
        getLogger(__name__).debug(pain_database)
        connection = connect(pain_database)
        with connection:
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE_QUERY)
            cursor.execute(query)
            results = cursor.fetchall()
            getLogger(__name__).debug(results)
            return results

    def get_pain_item_count(self, pain_database=DB_FILE_PATH):
        """Get the count of pain level items."""
        count_query = SELECT_PAIN_ITEM_COUNT_QUERY
        return self._execute_simple_query(count_query, pain_database)[0][0]

    def get_pain_items(self, pain_database=DB_FILE_PATH):
        """Get all the pain data items."""
        item_query = SELECT_PAIN_ITEMS_QUERY
        return self._execute_simple_query(item_query, pain_database)

    def save(self, pain_level, pain_database=DB_FILE_PATH):
        """Save the data for heuristics"""
        getLogger(__name__).debug(pain_level)
        getLogger(__name__).debug(pain_database)
        if not 0 <= int(pain_level) <= 10:
            raise INVALID_PAIN_INPUT_EXCEPTION
        insert_query = INSERT_PAIN_QUERY.format(
            pain_level=pain_level, city=self.city,
            temp=self.temperature, pressure=self.pressure,
            humidity=self.humidity, min_temp=self.min_temperature,
            max_temp=self.max_temperature, conditions=self.conditions)
        getLogger(__name__).debug(insert_query)
        connection = connect(pain_database)
        with connection:
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE_QUERY)
            cursor.execute(insert_query)


class WeatherAPI(object):  # pylint: disable=too-few-public-methods
    """Class for calling the weather api."""
    def __init__(self, api_key=WEATHER_ID, get_weather=get):
        """Initializer that requires an optional api_key."""
        self.logger = getLogger(__name__)
        self.logger.debug(api_key)
        self.api_key = api_key
        self.get = get_weather

    def get_weather_data(self, zip_code=DEFAULT_ZIP):
        """Method for calling the weather api to get weather data."""
        self.logger.debug(zip_code)
        api_url = API_URL.format(zip_code=zip_code, app_id=self.api_key,
                                 units=DEFAULT_UNITS)
        self.logger.debug(api_url)
        response = self.get(api_url)
        response.raise_for_status()
        result = response.json()
        weather_data = PainData(result)
        return weather_data
