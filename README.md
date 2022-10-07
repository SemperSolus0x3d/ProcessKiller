# Process Killer

A small program which runs with specified interval and kills processes by specified predicates.

Should work on Windows and Linux

>**Note**
>Make sure to run it with administrator privileges on Windows

## Configuration

ProcessKiller is configured via `config.toml` file. A [config example](config.toml) is included in the repository.

## Known limitations

Currently, only by-name and by-commandline predicates are supported, but other predicates support can be added as needed

## Requirements

- Python 3.10.1+ (earlier versions are untested, but may work)
- [toml](https://pypi.org/project/toml/)
- [psutil](https://pypi.org/project/psutil/)

## License

SPDX-License-Identifier: GPL-3.0-or-later

Copyright (C) 2022  SemperSolus0x3d

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
