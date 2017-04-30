"""This class is for retrieving weather data."""
# -*- coding: utf-8 -*-
from logging import getLogger
from settings import DEFAULT_ZIP
from weather_api import WeatherAPI


class WeatherRetriever(object):  # pylint: disable=too-few-public-methods
    """Class for retrieving weather data using a weather web api."""
    def __init__(self, weather_api=WeatherAPI()):
        """Initializer with option passed in weather api."""
        self._weather_api = weather_api

    def get_weather(self, zip_code=DEFAULT_ZIP):
        """Method to get weather data."""
        weather = self._weather_api.get_weather_data(zip_code)
        getLogger(__name__).debug(weather)
        return weather
