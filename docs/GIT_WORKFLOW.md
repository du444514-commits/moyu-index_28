# Git 分支管理与协作记录

本文件记录本项目开发过程中的分支创建、功能合并与一次冲突解决过程。

> **关于提交哈希的说明**：文中出现的短哈希为本地开发环境 `git log` 的记录（本地使用 `--no-ff` 合并，主干上保留合并节点）。本仓库在远端发布时，主干上的合并改动以压缩合并（squash）方式落地，提交信息统一标注「（合并自 xxx 分支）」；各功能分支自身仍保留独立提交，可用 `git branch -a` 查看。以远端仓库为准时，请以提交信息定位，不必依赖哈希。

## 1. 分支模型

采用简化版 Git Flow：

| 分支 | 用途 | 生命周期 |
| --- | --- | --- |
| `main` | 随时可运行的主干，只接受合并，不直接提交业务代码 | 长期 |
| `feature/*` | 单个功能的开发分支 | 合并后保留（便于追溯），不删除 |
| `hotfix/*` | 发布前的紧急修复分支 | 合并后保留 |

约定：

- 分支名统一 `类型/简短英文描述`，用小写与连字符；
- 提交信息遵循 Conventional Commits：`feat` / `fix` / `docs` / `chore` / `merge`；
- 合并时保留合并痕迹（本地用 `--no-ff`，远端用压缩合并并在信息中标注来源分支），
  历史图形状清楚，能一眼看出「哪个功能是一批提交」。

## 2. 完整时间线（本地）

```
*   a7d859f merge: 合并 hotfix/eof-input 到 main（v1.0.0 发布前修复）
|\
| * 04d4166 fix(cli): 交互模式遇到 EOF（Ctrl+D）时不再抛出 traceback
|/
*   0d1ea13 fix(merge): 解决 render.py 合并冲突，统一为 Unicode 方块 + 百分比样式
|\
| * 7546b91 feat(render): 进度条加上文字前缀与百分比后缀，信息更直观
* |   c5ab02a merge: 合并 feature/unicode-bar 到 main
|\ \
| |/
|/|
| * 03fb022 feat(render): 进度条改用 Unicode 方块字符，观感更整齐
|/
*   b582806 merge: 合并 feature/cli 到 main
|\
| * daf48a2 feat(cli): 增加交互式问答与参数模式入口
|/
* 3d6c628 feat: 加入摸鱼指数计分核心与单元测试
* a7ef844 chore: 初始化仓库，加入 MIT 许可证与 .gitignore
```

## 3. 分步操作记录

### 3.1 初始化主干

```bash
git init -b main
git add -A
git commit -m "chore: 初始化仓库，加入 MIT 许可证与 .gitignore"
```

### 3.2 计分核心

```bash
git commit -m "feat: 加入摸鱼指数计分核心与单元测试"
```

### 3.3 功能分支一：命令行入口

```bash
git checkout -b feature/cli                                    # 从 main 切出
# 开发 moyu/cli.py 与 main.py
git commit -m "feat(cli): 增加交互式问答与参数模式入口"
git checkout main
git merge --no-ff feature/cli -m "merge: 合并 feature/cli 到 main"
```

### 3.4 制造并解决冲突

为了让「冲突解决」这件事有真实记录，同时从 `main` 切出两个分支，
故意修改 `moyu/render.py` 中 `bar()` 的同一行返回语句：

```bash
git checkout -b feature/unicode-bar     # 方案 A：改用 █ / ░ 方块字符
git commit -am "feat(render): 进度条改用 Unicode 方块字符，观感更整齐"

git checkout main
git checkout -b feature/fancy-bar       # 方案 B：加「摸鱼」前缀与百分比
git commit -am "feat(render): 进度条加上文字前缀与百分比后缀，信息更直观"
```

先合并 A，成功：

```bash
git checkout main
git merge --no-ff feature/unicode-bar -m "merge: 合并 feature/unicode-bar 到 main"
```

再合并 B，触发冲突：

```bash
git merge --no-ff feature/fancy-bar
# Auto-merging moyu/render.py
# CONFLICT (content): Merge conflict in moyu/render.py
# Automatic merge failed; fix conflicts and then commit the result.
```

`git status` 显示：

```
UU moyu/render.py
```

文件内出现冲突标记：

```python
<<<<<<< HEAD
    return "[" + "█" * filled + "░" * (width - filled) + "]"
=======
    return "摸鱼 " + "▓" * filled + "─" * (width - filled) + " %d%%" % score
>>>>>>> feature/fancy-bar
```

### 3.5 冲突解决策略

两个分支的诉求并不矛盾：A 要「方块字符更好看」，B 要「显示百分比更直观」。
因此不是二选一，而是**融合**：

```python
return "摸鱼 " + "█" * filled + "░" * (width - filled) + " %d%%" % score
```

解决步骤：

```bash
# 1. 手动编辑 render.py，删除 <<<<<<< / ======= / >>>>>>> 三组标记
# 2. 同步更新受影响的测试断言（格式变了，3 条断言需要跟着改）
python3 -m unittest discover tests -q     # 21 条用例全绿
git add moyu/render.py tests/test_core.py
git commit -m "fix(merge): 解决 render.py 合并冲突，统一为 Unicode 方块 + 百分比样式"
```

经验总结：

1. 冲突解决后必须重新跑测试，因为格式变更往往会顺带打破测试断言；
2. 优先选「两边都要」的融合方案，而不是随便挑一边丢弃另一半工作；
3. 提交信息里写清冲突来源与决策理由，否则三个月后没人看得懂为什么这样改。

### 3.6 修复分支

测试中发现交互模式按 Ctrl+D 会抛 `EOFError` 导致 traceback，从 `main` 切出修复分支：

```bash
git checkout -b hotfix/eof-input
git commit -am "fix(cli): 交互模式遇到 EOF（Ctrl+D）时不再抛出 traceback"
git checkout main
git merge --no-ff hotfix/eof-input -m "merge: 合并 hotfix/eof-input 到 main（v1.0.0 发布前修复）"
```

同时新增 `tests/test_cli.py`，用 `mock.patch` 模拟 `EOFError`，防止回归。

### 3.7 打标签发布

```bash
git tag -a v1.0.0 -m "v1.0.0: 首个可用版本"
git push origin main --tags
```

## 4. 常用命令速查

| 场景 | 命令 |
| --- | --- |
| 查看带图形的历史 | `git log --oneline --graph --all` |
| 查看某分支独有的提交 | `git log main..feature/cli --oneline` |
| 查看两个分支的差异 | `git diff main...feature/fancy-bar` |
| 合并但不快进 | `git merge --no-ff feature/xxx` |
| 中止一次合并 | `git merge --abort` |
| 解决冲突后继续 | `git add <file>` 然后 `git commit` |
| 查看冲突文件 | `git diff --name-only --diff-filter=U` |
| 删除已合并的本地分支 | `git branch -d feature/xxx` |
