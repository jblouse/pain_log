# -*- coding: utf-8 -*-
from unittest import TestCase
from settings import TEST_STRING_CONTAINS
from weather_retriever import WeatherRetriever


class WeatherRetrieverTests(TestCase):
    """Tests for the weather api class."""
    def test_simple_case(self):
        """Test simple weather api case."""
        weather_api = WeatherRetriever()
        weather = weather_api.get_weather()
        self.assertIsNotNone(weather)
        self.assertIsNotNone(weather.temperature)
        self.assertIsNotNone(weather.pressure)
        self.assertTrue(TEST_STRING_CONTAINS in weather.__repr__())
