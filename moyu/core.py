"""摸鱼指数计分核心。

本模块只做纯计算，不涉及任何输入输出，方便单元测试与复用。
"""

MAX_SCORE = 100

# 各项指标的权重，四者之和必须为 1.0
WEIGHTS = {
    "switch": 0.30,   # 屏幕切换频率
    "idle": 0.25,     # 单次最长连续摸鱼时长
    "escape": 0.20,   # 遁走次数
    "work": 0.25,     # 真实工作占比（反向计分）
}

# 归一化上限：达到该值即视为该项满分
CAPS = {
    "switch": 120,
    "idle": 180,
    "escape": 10,
}

LEVELS = (
    (75, "赛博隐士"),
    (50, "摸鱼带师"),
    (25, "正常打工"),
    (0, "卷王本王"),
)


def _clamp(value, low, high):
    """把 value 限制在 [low, high] 区间内。"""
    if value < low:
        return low
    if value > high:
        return high
    return value


def _normalize(value, cap):
    """把 0~cap 的数值归一化到 0~1。"""
    if cap <= 0:
        raise ValueError("cap 必须为正数")
    return _clamp(value / cap, 0.0, 1.0)


def compute_score(switch_count, longest_idle_min, escape_count, real_work_ratio):
    """计算摸鱼指数。

    参数:
        switch_count: 今日窗口切换次数，>=0
        longest_idle_min: 单次最长连续摸鱼分钟，>=0
        escape_count: 茶水间 / 厕所遁走次数，>=0
        real_work_ratio: 真实工作占比，取值 0~1

    返回:
        int，0~100 之间的整数分数
    """
    if switch_count < 0 or longest_idle_min < 0 or escape_count < 0:
        raise ValueError("计数类指标不能为负数")
    if not 0.0 <= real_work_ratio <= 1.0:
        raise ValueError("real_work_ratio 必须落在 0~1 之间")

    score = 100.0 * (
        WEIGHTS["switch"] * _normalize(switch_count, CAPS["switch"])
        + WEIGHTS["idle"] * _normalize(longest_idle_min, CAPS["idle"])
        + WEIGHTS["escape"] * _normalize(escape_count, CAPS["escape"])
        + WEIGHTS["work"] * (1.0 - real_work_ratio)
    )
    return int(round(_clamp(score, 0, MAX_SCORE)))


def level_of(score):
    """根据分数返回摸鱼等级名称。"""
    score = _clamp(score, 0, MAX_SCORE)
    for threshold, name in LEVELS:
        if score >= threshold:
            return name
    return LEVELS[-1][1]


def advice_of(score):
    """根据分数给一句（不太正经的）建议。"""
    if score >= 75:
        return "建议立刻把窗口切回去，你的摸鱼已经能被隔壁工位听见了。"
    if score >= 50:
        return "还行，属于带薪思考人生，记得给自己留一条后路。"
    if score >= 25:
        return "基本正常，偶尔神游，属于健康打工人的合理波动。"
    return "今天的你过于努力，建议摸五分钟，保护一下颈椎。"
