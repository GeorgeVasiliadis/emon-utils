# EmonUtils
A simple integration set of utilities connecting EmonPi's ecosystem with CouchDB

## Features
- Subscribe on EmonPi's feeds of interest and re-transmit the measurements on a CouchDB server

## How To Use
1. Install package by running `pip install emon-utils`
2. Use package with `python -m EmonUtils`

## Configuration
When running for the first time, EmonUtils will fire the auto-configuration scripts up. After that, the system will be ready to use.

> The auto-configuration scripts can be invoked on demand. The functions `from EmonUtils.setup import generate_config, generate_schema` cam be used accordingly.

An other way of configuring EmonUtils is by locating and editing the respective files manually. `from EmonUtils import CONFIG_FILE, SCHEMA_FILE` can be used to examine where those files are stored.

## Important Notes
- Make sure that the underlying server's clock is configured as desired. In the case of EmonPi, the default time zone might lead to obfuscating bugs.
