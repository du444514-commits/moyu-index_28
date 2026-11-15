"""moyu-index_28: 命令行摸鱼指数计算器。"""

__version__ = "0.1.0"

from .core import compute_score, level_of, advice_of
from .quotes import quote_of

__all__ = ["compute_score", "level_of", "advice_of", "quote_of"]
