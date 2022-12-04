# dice_for_COC
dice_EN 英文

dice_CN 中文

## 需要的包
datetime, numpy, PySimpleGUI

## 外观
![image](https://user-images.githubusercontent.com/74366156/205445017-14b82654-eef1-4514-aba9-149843b40fbf.png)

![image](https://user-images.githubusercontent.com/74366156/205445037-6f407b36-bc0e-4d66-aeab-a7a5dbfacf56.png)

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
