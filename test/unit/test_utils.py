import unittest
from unittest.mock import patch, mock_open

import utils

utils.ENABLE_CACHING = True


@patch("builtins.open", new_callable=mock_open)
@patch("utils.pickle")
@patch("utils.os")
class TestUtils(unittest.TestCase):

    def test_load_cached_result_from_file(self,
                                          os_mock,
                                          pickle_mock,
                                          _open_mock):
        os_mock.path.isfile.return_value = True
        pickle_mock.load.return_value = 42
        ret = self._testing_function()

        self.assertEqual(42, ret)
        pickle_mock.load.assert_called_once()

    def test_save_cached_result_to_file(self,
                                        os_mock,
                                        pickle_mock,
                                        _open_mock):
        os_mock.path.isfile.return_value = False

        ret = self._testing_function()

        self.assertEqual(42, ret)
        pickle_mock.dump.assert_called_once()

    def test_save_cached_result_to_file_and_crate_dir(self,
                                                      os_mock,
                                                      pickle_mock,
                                                      _open_mock):
        os_mock.path.isfile.return_value = False
        os_mock.path.isdir.return_value = False

        ret = self._testing_function()

        self.assertEqual(42, ret)
        os_mock.mkdir.assert_called_once()
        pickle_mock.dump.assert_called_once()

    @utils.cache_result_to_file("dummy_cache_file")
    def _testing_function(self):
        return 42
