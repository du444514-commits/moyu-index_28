"""core 与 render 的单元测试，直接运行：python -m unittest discover tests"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moyu.core import compute_score, level_of, advice_of, MAX_SCORE
from moyu.render import bar


class TestComputeScore(unittest.TestCase):
    def test_全卷王拿到接近零分(self):
        score = compute_score(0, 0, 0, 1.0)
        self.assertEqual(score, 0)

    def test_全摸鱼拿到满分(self):
        score = compute_score(120, 180, 10, 0.0)
        self.assertEqual(score, MAX_SCORE)

    def test_超额数据会被截断在区间内(self):
        score = compute_score(999, 9999, 99, -0.0 + 0.0)
        self.assertEqual(score, MAX_SCORE)

    def test_分数始终落在合法区间(self):
        for switch in (0, 30, 200):
            for idle in (0, 60, 400):
                for escape in (0, 3, 20):
                    for ratio in (0.0, 0.5, 1.0):
                        score = compute_score(switch, idle, escape, ratio)
                        self.assertGreaterEqual(score, 0)
                        self.assertLessEqual(score, MAX_SCORE)

    def test_负数输入会报错(self):
        with self.assertRaises(ValueError):
            compute_score(-1, 0, 0, 0.5)
        with self.assertRaises(ValueError):
            compute_score(0, -1, 0, 0.5)
        with self.assertRaises(ValueError):
            compute_score(0, 0, -1, 0.5)

    def test_非法工作占比会报错(self):
        with self.assertRaises(ValueError):
            compute_score(10, 10, 1, 1.5)
        with self.assertRaises(ValueError):
            compute_score(10, 10, 1, -0.1)

    def test_指标越高分数越高(self):
        low = compute_score(10, 10, 1, 0.9)
        high = compute_score(80, 120, 8, 0.2)
        self.assertGreater(high, low)


class TestLevel(unittest.TestCase):
    def test_等级边界(self):
        self.assertEqual(level_of(0), "卷王本王")
        self.assertEqual(level_of(24), "卷王本王")
        self.assertEqual(level_of(25), "正常打工")
        self.assertEqual(level_of(50), "摸鱼带师")
        self.assertEqual(level_of(75), "赛博隐士")
        self.assertEqual(level_of(100), "赛博隐士")

    def test_越界分数被截断(self):
        self.assertEqual(level_of(-10), "卷王本王")
        self.assertEqual(level_of(200), "赛博隐士")

    def test_每个等级都有建议(self):
        for score in (0, 30, 60, 90):
            self.assertTrue(advice_of(score))


class TestBar(unittest.TestCase):
    def test_零分全部为空(self):
        self.assertEqual(bar(0, width=10), "摸鱼 ░░░░░░░░░░ 0%")

    def test_满分全部填满(self):
        self.assertEqual(bar(100, width=10), "摸鱼 ██████████ 100%")

    def test_半格宽度正确(self):
        result = bar(50, width=10)
        self.assertEqual(result, "摸鱼 █████░░░░░ 50%")

    def test_非法宽度报错(self):
        with self.assertRaises(ValueError):
            bar(50, width=0)


if __name__ == "__main__":
    unittest.main()
