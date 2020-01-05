# bt-stat
Polybar bluetooth module. 

## Installation/usage
1. Make sure bluetoothctl and Python >= 3.3 is installed
2. Download python script and modify the (list of) MAC addresses for bluetooth devices to fit your own stuff. 
3. Create polybar config
```
[module/bluetooth]
type = custom/script
label = %output%
format-prefix = " "
format-underline = #5f6cd7
format-prefix-foreground = ${colors.foreground-alt}
exec = python3 ~/.config/polybar/bt-stat.py
```