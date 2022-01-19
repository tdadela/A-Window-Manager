# A Window Manager
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [License](#license)

## General info
A simple tiling window manager.\
Warning: this is an early version of window manager – lack of crucial features, many bugs.


## Technologies
A window manager is written in python, using the Xlib library.\
Created for GNU/Linux, tested with Python 3.9 and Python 3.10.

The default programs are dmenu (launching applications) and feh (setting background).\
The default emulator for the window manager is Xephyr.\
Please install the above software or change the configuration file.
## Setup

```bash
$ git clone https://github.com/tdadela/A-Window-Manager
$ cd A-Window-Manager
$ ./setup.sh
```
## Usage
To use window manager in the emulator:
```bash
$ ./run.sh
```
With default configuration:\
<kbd>Alt</kbd> + <kbd>d</kbd> – open application launcher\
<kbd>Alt</kbd> + <kbd>f</kbd> – full-screen application\
<kbd>Alt</kbd> + <kbd>q</kbd> – close application\
<kbd>Alt</kbd> + <kbd>1</kbd> – switch to workspace 1\
<kbd>Alt</kbd> + <kbd>2</kbd> – switch to workspace 2\
…\
<kbd>Alt</kbd> + <kbd>0</kbd> – switch to workspace 10\
<kbd>Alt</kbd> + <kbd>Shift</kbd>+ <kbd>1</kbd> – move focused window to workspace 1\
…\
<kbd>Alt</kbd> + <kbd>Shift</kbd>+ <kbd>0</kbd> – move focused window to workspace 10
## Configuration
To customize the window manager, edit the config.py file.

## Contributing
Pull requests are welcome. For considerable changes, please open an issue first to discuss what you would like to change.

## License
MIT
