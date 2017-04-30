# -*- coding: utf-8 -*-
from os import path, remove
from unittest import TestCase
from logging import getLogger
from weather_api import WeatherAPI
from settings import PA_ZIP_CODE, TEST_CITY_TX_NAME, TEST_CITY_PA_NAME, \
    TEST_STRING_CONTAINS, TEST_DB_PATH, INVALID_PAIN_INPUT_EXCEPTION


class WeatherAPITests(TestCase):
    """Tests for the weather api class."""
    def setUp(self):
        """Setup test database file."""
        self.db_path = TEST_DB_PATH
        self._delete_test_database()

    def tearDown(self):
        """Teardown test database file."""
        self._delete_test_database()

    def _delete_test_database(self):
        """Delete the test database file."""
        if path.isfile(self.db_path):
            remove(self.db_path)

    def test_simple_case(self):
        """Test simple weather api case."""
        weather_api = WeatherAPI()
        pain_data = weather_api.get_weather_data()
        self.assertIsNotNone(pain_data)
        self.assertIsNotNone(pain_data.temperature)
        self.assertIsNotNone(pain_data.pressure)
        self.assertTrue(TEST_STRING_CONTAINS in pain_data.__repr__())
        self.assertIsNone(pain_data.save(10, self.db_path))
        self.assertIsNone(pain_data.save(0, self.db_path))
        self.assertIsNone(pain_data.save(5, self.db_path))
        self.assertEquals(pain_data.get_pain_item_count(self.db_path), 3)
        with self.assertRaises(type(INVALID_PAIN_INPUT_EXCEPTION)):
            pain_data.save(100)
        with self.assertRaises(type(INVALID_PAIN_INPUT_EXCEPTION)):
            pain_data.save(-100)
        with self.assertRaises(ValueError):
            pain_data.save('test')
        self.assertEquals(len(pain_data.get_pain_items(self.db_path)), 3)

    def test_zip_case(self):
        """Test simple weather api case."""
        weather_api = WeatherAPI()
        weather_tx = weather_api.get_weather_data()
        self.assertIsNotNone(weather_tx)
        self.assertEquals(weather_tx.city, TEST_CITY_TX_NAME)
        getLogger(__name__).debug(weather_tx)
        weather_pa = weather_api.get_weather_data(PA_ZIP_CODE)
        self.assertIsNotNone(weather_pa)
        getLogger(__name__).debug(weather_pa)
        self.assertEquals(weather_pa.city, TEST_CITY_PA_NAME)
        self.assertIsNotNone(weather_tx.temperature)
        self.assertIsNotNone(weather_tx.pressure)
        self.assertTrue(TEST_STRING_CONTAINS in weather_tx.__repr__())
        self.assertNotEquals(weather_tx.city, weather_pa.city)
