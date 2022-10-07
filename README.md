# Process Killer

A small program which runs with specified interval and kills processes by specified predicates.

Should work on Windows and Linux

>**Note**
>Make sure to run it with administrator privileges on Windows

## Configuration

ProcessKiller is configured via `config.toml` file. A [config example](config.toml) is included in the repository.

## Known limitations

Currently, only by-name predicates are supported, but other predicates support can be added as needed

## Requirements

- Python 3.10.1+ (earlier versions are untested, but may work)
- [toml](https://pypi.org/project/toml/)
- [psutil](https://pypi.org/project/psutil/)
