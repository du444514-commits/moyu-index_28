"""命令行入口：交互问答 + 参数模式。"""

import argparse
import sys

from .core import compute_score, level_of, advice_of
from .quotes import quote_of
from .render import bar


def _ask_number(prompt, default):
    """读取一个非负数字，回车则使用默认值。"""
    try:
        raw = input(prompt).strip()
    except EOFError:
        print()
        print("   -> 检测到输入流结束（Ctrl+D），改用默认值 %s" % default)
        return default
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        print("   -> 输入不是数字，已使用默认值 %s" % default)
        return default
    if value < 0:
        print("   -> 不能填负数，已使用默认值 %s" % default)
        return default
    return value


def run_interactive():
    print("========== 摸鱼指数计算器 v0.2 ==========")
    print("直接回车即采用括号内的默认值\n")
    switch = _ask_number("1. 今天窗口切换次数 (60): ", 60)
    idle = _ask_number("2. 单次最长连续摸鱼分钟 (30): ", 30)
    escape = _ask_number("3. 茶水间/厕所遁走次数 (3): ", 3)
    ratio = _ask_number("4. 真实工作占比 0~1 (0.6): ", 0.6)
    ratio = min(ratio, 1.0)
    return switch, idle, escape, ratio


def render_report(score):
    level = level_of(score)
    print()
    print("  摸鱼指数 : %d / 100  %s" % (score, bar(score)))
    print("  当前等级 : %s" % level)
    print("  一句点评 : %s" % quote_of(level, score))
    print("  助手建议 : %s" % advice_of(score))
    print()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="moyu",
        description="摸鱼指数计算器：给今天的摸鱼程度打个分。",
    )
    parser.add_argument("--switch", type=float, default=60, help="窗口切换次数")
    parser.add_argument("--idle", type=float, default=30, help="单次最长摸鱼分钟")
    parser.add_argument("--escape", type=float, default=3, help="遁走次数")
    parser.add_argument("--work", type=float, default=0.6, help="真实工作占比 0~1")
    parser.add_argument("--no-input", action="store_true", help="跳过交互，直接用参数")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.no_input or not sys.stdin.isatty():
        switch, idle, escape, ratio = args.switch, args.idle, args.escape, args.work
    else:
        switch, idle, escape, ratio = run_interactive()

    try:
        score = compute_score(switch, idle, escape, ratio)
    except ValueError as exc:
        print("参数有误：%s" % exc, file=sys.stderr)
        return 2

    render_report(score)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
