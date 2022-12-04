# dice_for_COC
dice_EN for English user
dice_CN for Chinese user

## Package needed
datetime, numpy, PySimpleGUI

## Appearance
This is a dice made for call of cthulhu a table RPG.
![image](https://user-images.githubusercontent.com/74366156/205445017-14b82654-eef1-4514-aba9-149843b40fbf.png)

![image](https://user-images.githubusercontent.com/74366156/205445037-6f407b36-bc0e-4d66-aeab-a7a5dbfacf56.png)

## Function
There are several commonly used dice involved including 1d3, 1d4, 1d6, 1d8, 1d100.

Manully dice calculation is the button entry which takes in a format like 1d3 + 2d6 + 2

If you have two screen, the second window can be used to show the results and hide all the hidden dicing.

The biggest window is used to keep record of all the dice you have done, when the function is closed by the "exit" button, it will be automaticly be saved into a log file.

The color of the result will change when 1d100 > 95 or < 5 for the indication of Fumbles and Criticals. The value can be changed 


## Further
Still in developing and glad to solve bugs anyone raised.

Deal with some bugs.

## Current bugs:
Won't handle error input in customized dice.
