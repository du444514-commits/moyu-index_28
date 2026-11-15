# moyu-index_28

> 一个零依赖的命令行「摸鱼指数计算器」——把今天到底摸了几成鱼，量化成一个 0~100 的分数。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Deps](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#)

```
  摸鱼指数 : 70 / 100  摸鱼 █████████████████░░░░░░░ 70%
  当前等级 : 摸鱼带师
  一句点评 : 你已经掌握了「看起来很忙」的核心技术栈。
  助手建议 : 还行，属于带薪思考人生，记得给自己留一条后路。
```

## 为什么做这个东西

市面上的「效率工具」都在催你干活，几乎没有工具关心你今天累不累。
`moyu-index_28` 反着来：它不打鸡血，只负责把你那些「说不清但确实存在」的摸鱼行为，
折算成一个能发给同事看的分数。

它只有 4 个指标、1 个分数条、1 句点评，装完就能用，不需要账号、不联网、不收集任何数据。

## 特性

- 零第三方依赖，只用 Python 标准库
- 交互问答与命令行参数两种模式
- 四项指标加权计分，输出 0~100 分、等级、语录与进度条
- 全部逻辑可单元测试，21 条用例覆盖边界与非法输入

## 快速开始

需要 Python 3.8 及以上版本。

```bash
git clone https://github.com/du444514-commits/moyu-index_28.git
cd moyu-index_28
python3 main.py
```

交互模式会依次问你四个问题，直接回车即采用默认值：

| 序号 | 问题 | 默认值 |
| --- | --- | --- |
| 1 | 今天窗口切换次数 | 60 |
| 2 | 单次最长连续摸鱼分钟 | 30 |
| 3 | 茶水间 / 厕所遁走次数 | 3 |
| 4 | 真实工作占比（0~1） | 0.6 |

也可以一次性传参，适合写进脚本或 crontab：

```bash
python3 main.py --no-input --switch 100 --idle 90 --escape 6 --work 0.2
```

单独当模块用：

```python
from moyu import compute_score, level_of

score = compute_score(switch_count=80, longest_idle_min=45, escape_count=4, real_work_ratio=0.3)
print(score, level_of(score))   # 打印分数与等级
```

## 计分规则

四项指标各自归一化到 0~1，再按权重加权，最后乘以 100 并取整：

| 指标 | 权重 | 归一化上限 | 说明 |
| --- | --- | --- | --- |
| 窗口切换次数 | 0.30 | 120 次 | 切得越勤，越像在假装忙碌 |
| 单次最长摸鱼 | 0.25 | 180 分钟 | 一次连摸三小时即视为满分 |
| 遁走次数 | 0.20 | 10 次 | 茶水间、厕所、楼下买咖啡皆算 |
| 真实工作占比 | 0.25 | — | 反向计分，占比越低分越高 |

等级划分：

| 分数区间 | 等级 |
| --- | --- |
| 75 ~ 100 | 赛博隐士 |
| 50 ~ 74 | 摸鱼带师 |
| 25 ~ 49 | 正常打工 |
| 0 ~ 24 | 卷王本王 |

完整推导见 [docs/DESIGN.md](docs/DESIGN.md)。

## 目录结构

```
moyu-index_28/
├── main.py              # 直接运行的入口
├── moyu/
│   ├── __init__.py      # 对外导出的 API
│   ├── core.py          # 计分核心（纯计算，无 IO）
│   ├── quotes.py        # 摸鱼语录
│   ├── render.py        # 进度条渲染
│   └── cli.py           # 命令行入口
├── tests/               # 单元测试
├── docs/
│   ├── DESIGN.md        # 设计说明
│   └── GIT_WORKFLOW.md  # 分支、合并与冲突解决记录
├── LICENSE
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## 运行测试

```bash
python3 -m unittest discover tests -v
```

## 参与贡献

欢迎提 Issue 和 PR，流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。
提 PR 前请确保 `python3 -m unittest discover tests` 全绿。

## 许可证

本项目采用 [MIT License](LICENSE) 开源，可自由用于商业项目，保留版权声明即可。

## 变更记录

见 [CHANGELOG.md](CHANGELOG.md)。
