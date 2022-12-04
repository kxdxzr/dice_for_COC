# dice_for_COC

[简体中文](README.md) | [English](README_EN.md)

dice_EN 英文

dice_CN 中文

## 需要的包
datetime, numpy, PySimpleGUI

## 外观
![image](https://user-images.githubusercontent.com/74366156/205477370-23b44c54-612e-4bdf-9239-9869158d939f.png)

![image](https://user-images.githubusercontent.com/74366156/205477372-685b03a1-385b-4ffb-a9e6-a97864192eea.png)

## 功能
一些常用骰子已经做成按钮包括 1d3, 1d4, 1d6, 1d8, 1d100.

自定义骰子，格式： 1d3 + 2d6 + 2

如果拥有两个屏幕，可以使用“front_end”窗口来展示结果。

The biggest window is used to keep record of all the dice you have done, when the function is closed by the "exit" button, it will be automaticly be saved into a log file.

当1d100随机到大成功与大失败的值时，结果颜色会发生变化，默认大成功大失败值为5 和 96， 该值可改变。


## 未来
仍在开发中，欢迎提供bug与建议

处理bug.

## 当前bug:
无法处理非法自定义骰子输入
