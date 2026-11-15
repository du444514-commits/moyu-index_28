# 贡献指南

感谢你愿意花时间。这个项目很小，所以规则也尽量少。

## 开发环境

只需要 Python 3.8+，不需要安装任何第三方依赖。

```bash
git clone https://github.com/du444514-commits/moyu-index_28.git
cd moyu-index_28
python3 -m unittest discover tests -v
```

如果测试全绿，说明环境准备完成。

## 提交 Issue

请说明：

1. 你做了什么操作（完整命令或输入序列）；
2. 期望的结果；
3. 实际的结果，有 traceback 就贴 traceback。

## 提 PR 的流程

```bash
git checkout -b feature/你的功能名
# 改代码
python3 -m unittest discover tests      # 必须全绿
git commit -m "feat: 一句话说明"
git push origin feature/你的功能名
```

然后到 GitHub 上开 Pull Request，说明改动动机与影响范围。

## 代码约定

- 遵循 PEP 8，缩进 4 空格，单行不超过 100 字符；
- `moyu/core.py` 里不允许出现 `print` 与 `input`，保持纯函数；
- 新增或修改行为，必须同步补测试，测试文件放在 `tests/` 下，文件名以 `test_` 开头；
- 提交信息用 Conventional Commits：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`；
- 中文注释与中文文案可以，代码标识符用英文。

## 新增语录

语录在 `moyu/quotes.py` 中按等级分组，新增时：

- 每条不超过 30 个字，避免在终端里折行；
- 不要涉及具体公司、真实人名；
- 保持「反内卷但不冒犯」的调性。

## 许可证

你提交的代码会以项目的 [MIT License](LICENSE) 发布，提交即视为同意。
