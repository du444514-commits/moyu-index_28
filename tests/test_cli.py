"""cli 模块的输入健壮性测试。"""

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moyu.cli import _ask_number, main


class TestAskNumber(unittest.TestCase):
    def test_回车使用默认值(self):
        with mock.patch("builtins.input", return_value=""):
            self.assertEqual(_ask_number("?", 60), 60)

    def test_正常数字被解析(self):
        with mock.patch("builtins.input", return_value="42"):
            self.assertEqual(_ask_number("?", 60), 42)

    def test_非数字回退默认值(self):
        with mock.patch("builtins.input", return_value="abc"):
            self.assertEqual(_ask_number("?", 60), 60)

    def test_负数回退默认值(self):
        with mock.patch("builtins.input", return_value="-5"):
            self.assertEqual(_ask_number("?", 60), 60)

    def test_输入流结束不崩(self):
        with mock.patch("builtins.input", side_effect=EOFError):
            self.assertEqual(_ask_number("?", 60), 60)


class TestMain(unittest.TestCase):
    def test_参数模式正常返回零(self):
        self.assertEqual(main(["--no-input", "--switch", "30", "--idle", "20"]), 0)

    def test_非法工作占比返回错误码(self):
        self.assertEqual(main(["--no-input", "--work", "2"]), 2)


if __name__ == "__main__":
    unittest.main()
