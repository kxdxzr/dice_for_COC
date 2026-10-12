# dice_for_COC 🎲

COC 跑团骰子 / Dice for Call of Cthulhu TRPG，带 GUI。

> **v2.0 更新**：`dice_CN.py` + `dice_EN.py` 已合并为单个 **`dice.py`**，
> 右下角 `语言/Language` 可实时切换中文 / English，无需重启。
> 旧的 `dice_CN.py` / `dice_EN.py` 保留作历史备份，新用户请用 `dice.py` 或直接下载 exe。
>
> **v2.0 update**: `dice_CN.py` + `dice_EN.py` merged into single **`dice.py`**
> with live 中文/EN switch (bottom-right, no restart needed).
> Old files are kept for history; new users please use `dice.py` or the exe in Releases.

---

## 下载即用 / Download & Play

- **Windows 用户**：去右侧 [Releases](../../releases) 下载 `dice_for_COC.exe`，双击即用，无需装 Python。
- **Windows users**: download `dice_for_COC.exe` from [Releases](../../releases), double-click to run. No Python needed.

## 源码运行 / Run from source

```bash
pip install -r requirements.txt
python dice.py
```

依赖只有 `FreeSimpleGUI`（PySimpleGUI 免费分支，API 完全兼容；如果你还有旧版 `PySimpleGUI` 也能直接跑）。
`numpy` 已不再需要（v2.0 起存档改用纯 Python 读写）。

Requires only `FreeSimpleGUI` (free fork of PySimpleGUI, same API; old `PySimpleGUI` also works).
`numpy` is no longer needed since v2.0.

## 外观 / Screenshots

![image](https://user-images.githubusercontent.com/74366156/205477370-23b44c54-612e-4bdf-9239-9869158d939f.png)

![image](https://user-images.githubusercontent.com/74366156/205477372-685b03a1-385b-4ffb-a9e6-a97864192eea.png)

## 功能 / Features

| 中文 | English |
|---|---|
| 常用骰按钮：1d3 / 1d4 / 1d6 / 1d8 / 1d10 / 1d100 | Quick buttons: 1d3 / 1d4 / 1d6 / 1d8 / 1d10 / 1d100 |
| 自定义骰子，格式如 `1d3 + 2d6 + 2`（空格可有可无）| Custom formula like `1d3 + 2d6 + 2` (spaces optional) |
| 双窗口：`Front_end` 大字展示，适合双屏投屏；`Hide` 可隐藏暗投结果 | Second window `Front_end` for big display on a second screen; `Hide` conceals secret rolls |
| 大成功 / 大失败变色（默认 ≤5 金色、≥96 红色，阈值可改）| Critical / Fumble highlight (default ≤5 gold, ≥96 red, adjustable) |
| 日志窗口记录每次投掷，退出时自动存 `log.log`，可加载、可删上一条 | Log panel records every roll, auto-saved to `log.log` on exit; load & undo supported |
| 语言实时切换：右下角 `中文 / EN` | Live language switch: bottom-right `中文 / EN` |
| 设置（语言 + 阈值）自动存 `settings.set` | Settings (language + thresholds) auto-saved to `settings.set` |

## 文件说明 / Files

| 文件 File | 说明 Description |
|---|---|
| `dice.py` | ✅ 主程序（中英合并版），用这个 / Main program (merged bilingual), use this |
| `dice_for_COC.exe` | Windows 打包版（见 Releases）/ Packaged Windows build (see Releases) |
| `dice_CN.py` / `dice_EN.py` | 旧版备份 / Legacy backups |
| `log.log` / `settings.set` | 运行时自动生成 / Auto-generated at runtime |

## 自己打包 exe / Build the exe yourself

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name dice_for_COC dice.py
# 产物在 dist/dice_for_COC.exe
```

## 反馈 / Feedback

欢迎提 Issue 报 bug、提建议。Still in development, issues and suggestions welcome.
