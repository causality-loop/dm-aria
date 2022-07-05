# dm-aria

## Background
- Use *aria2*, *dmenu*, and Python to download torrents
- Only tested on Arch Linux

## Dependencies
### Mandatory
- dmenu
- [aria2p](https://github.com/pawamoy/aria2p) (and see the Requirements section)

### Optional
- dunst

## Install
```
git clone git@github.com:causality-loop/dm-aria.git
cd dm-aria
chmod +x dm-aria.py
```

## Usage
### Key binding
- First, you'll probably want to assign a key binding to the script (Qtile example):
```
keys = [
    KeyChord([mod], 'space', [
        Key([], 'f', lazy.run_extension(DmenuRun(
            dmenu_command='/home/user/git/dm-aria/dm-aria.py', **dmenu_theme))),
    ]
]
```

### The python script
- Upon running the script, enter a search query
- Type which option you would like to download (you can also use arrow keys or `<C-n>` & `<C-p>`)
- Press `<Esc>` at any time to cancel
- After making a selection, note that `~/.cache/dm-aria/magnet_uris.txt` is now populated
- Repeat the above steps until you have stored all the magnet uris you want to download from

### Configuring aria2
- aria2 looks for a config in `~/.config/aria2/aria2.conf`
- Here is a minimal example config:
```
dir=${HOME}/downloads
input-file=${HOME}/.cache/dm-aria/magnet_uris.txt
save-session=${HOME}/.cache/dm-aria/magnet_uris.txt
```

### More dmenu fun
- Optionally, make a BASH script which will start/stop aria2 from dmenu
- Minimal example:
```
#!/bin/bash

declare -a options=(
'aria2 go'
'aria2 kill'
)

choice=$(printf '%s\n' "${options[@]}" | dmenu -p 'Run' "${@}")

case $choice in
  'aria2 go') aria2c --enable-rpc &&  notify-send "⬇️  Downloading with Aria2" ;;
  'aria2 kill') killall aria2c && notify-send "☠️  Killied Aria2" ;;
esac

```

### Downloading
- With or without dmenu, begin downloading with:
```
$ aria2c --enable-rpc
```
- Adjust how aria2 functions and check download progress with:
```
$ aria2p
```
- If you need help with *aria2p*, type `?` to bring up a help menu

### Wrapping things up
- If desired, kill *aria2* with the *dmenu* script above, or simply:
```
killall aria2c
```
- Note that `~/.cache/dm-aria/magnet_uris.txt` is now empty
