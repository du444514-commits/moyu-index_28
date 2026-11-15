# 发布到 GitHub

本地仓库已经完整，含 `main` 分支、4 个功能/修复分支、一次真实的冲突解决与 `v1.0.0` 标签。
剩下只需要把它推到你的 GitHub 账号下。

## 1. 前置准备

仓库名必须是 `项目名_学号后两位` 的格式，本项目已经叫 `moyu-index_28`，无需改名。

```bash
cd moyu-index_28
git log --oneline --graph --all      # 确认历史完整
git status                           # 应为 working tree clean
```

## 2. 在 GitHub 上建空仓库

打开 https://github.com/new ：

- Repository name：`moyu-index_28`
- 可见性：**Public**（作业要求开源，私有仓库不算）
- **不要**勾选 Add a README / .gitignore / license

## 3. 关联远程并推送

```bash
git remote add origin https://github.com/du444514-commits/moyu-index_28.git
git push -u origin main
git push origin --tags
```

推送时提示输入用户名和密码：用户名填 GitHub 用户名，**密码位置粘贴 Personal Access Token**。

## 4. 推送所有分支

```bash
git push origin feature/cli feature/unicode-bar feature/fancy-bar hotfix/eof-input
```

## 5. 推送后要检查的四件事

1. 仓库首页能正常渲染 README，徽章不是裂图；
2. 仓库右侧出现 "MIT license" 标识；
3. Actions 工作流在三个 Python 版本上全绿；
4. Insights → Network 能看到分支与合并图形。

## 6. 常见报错

| 报错 | 原因 | 处理 |
| --- | --- | --- |
| `remote origin already exists` | remote 已存在 | `git remote set-url origin <新地址>` |
| `Updates were rejected` | 远端仓库非空 | `git pull --rebase origin main` 后再推 |
| `Authentication failed` | 用了账号密码而非 token | 改用 token |
| `src refspec main does not match any` | 本地还没有 main 分支 | 确认 `git branch` 里有 main |
