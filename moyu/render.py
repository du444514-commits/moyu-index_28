"""分数条渲染。"""

DEFAULT_WIDTH = 24


def bar(score, width=DEFAULT_WIDTH):
    """把 0~100 的分数画成一条进度条。

    参数:
        score: 0~100 的整数分数
        width: 进度条总格数

    返回:
        str，例如 "摸鱼 █████░░░░░ 50%"
    """
    if width <= 0:
        raise ValueError("width 必须为正数")
    score = max(0, min(100, int(score)))
    filled = round(width * score / 100)
    return "摸鱼 " + "█" * filled + "░" * (width - filled) + " %d%%" % score
