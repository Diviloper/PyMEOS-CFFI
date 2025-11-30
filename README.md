# ![MEOS Logo](https://raw.githubusercontent.com/MobilityDB/PyMEOS/master/docs/images/PyMEOS%20Logo.png)

[MEOS (Mobility Engine, Open Source)](https://www.libmeos.org/) is a C library which enables the manipulation of
temporal and spatio-temporal data based on [MobilityDB](https://mobilitydb.com/)'s data types and functions.

PyMEOS CFFI is a Python library that wraps the MEOS C library using CFFI, providing a set of python functions
that allows to use all MEOS functionality while automatically taking care of conversions between basic Python and C types
(such as Python's `str` to C's `char *`).  

This library is not meant to be used directly by the user, since most of the functions receive or return C objects 
(CFFI's `cdata` type).  

The [PyMEOS](../pymeos) library is built on top of this library and exposes all the functionality
of MEOS through a set of Python classes.

# Wrappers

This package wraps the MEOS C library in two different levels:

- **MEOS Python binding:** wrapper around the MEOS C library, created with the CFFI package, that allows calling the MEOS functions from Python. The resulting wrapper is a shared library (`_meos_cffi.so` in linux, `_meos_cffi.dylib` in macOS) that can be imported in Python. It requires MEOS to be installed in the system.
- **PyMEOS-CFFI package:** wrapper around the MEOS Python binding that handles many standard conversions between Python and C (e.g. `char *` and `str`) types and manages the error system. The resulting wrapper is a standard Python package that can be installed via `pip` or other package managers. The resulting package comes with MEOS and the Python binding bundled.

# Usage

## Installation

````shell
pip install pymeos-cffi
````

## Source installation
If the pre-built distribution is not available for your system, `pip` will try to make source distribution. For that, you will 
need to make sure you have the following requirements:

- C compiler
- [MEOS Library](https://www.libmeos.org/)

If the installation fails, you can submit an issue in the [PyMEOS-CFFI issue tracker](https://github.com/MobilityDB/PyMEOS-CFFI/issues)

# Building the MEOS Python binding

To build the binding, you just need to perform two steps

1. Generate the header file
2. Build the binding

To do so, simply run the following commands:

```bash
uv run builder/build_header.py
uv run builder/build_pymeos.py
```

If any of the steps fails, or you want more information about the process, the following subsections provide more details.

## 1. Generate the header file

This step is only necessary if the underlying MEOS Library has been updated. Otherwise, you can skip this step (although running it will not break anything).

To generate the header file, you just need to run the following command:

```bash
uv run builder/build_header.py
```

This command grabs the meos header and binary files from the default location and combines them into a single file ([`builder/meos.h`](builder/meos.h)) that will be used to generate the binding.

The default locations are:
- For Linux:
  - Header files: taken from `/usr/local/include/`.
  - Binary: `/usr/local/lib/libmeos.so`.
- For macOS:
  - Header files: taken from `/usr/local/include`.
  - Binary: `/usr/local/lib/libmeos.dylib`.
- For arm macOS:
  - Header files: taken from `/opt/homebrew/include`.
  - Binary: `/opt/homebrew/lib/libmeos.dylib`.

If you installed meos in a different location, you can pass the paths to the command (note that all header files must be in the same directory, as only one path is allowed):
```bash
uv run builder/build_header.py /path/to/directory/with/headers/ /path/to/binary.so
```

## 2. Build bindings

This step builds the shared library based on the generated header file, and links it with the MEOS library.

To build the bindings, just run the following command:
```bash
uv run builder/build_pymeos.py
```

As in the previous step, this command assumes that the MEOS header and binary files are in the default locations.

If they are not, you can specify alternative locations with the `MEOS_INCLUDE_DIR` and `MEOS_LIB_DIR` environment variables. Here, you can specify multiple paths for each, separated by a semicolon.

```bash
export MEOS_INCLUDE_DIR="/path/to/include/;/path/to/include2/"
export MEOS_LIB_DIR=/path/to/lib/dir/
uv run builder/build_pymeos.py
```

# Building the PyMEOS-CFFI Package

To update and build the PyMEOS-CFFI wrapper, you need to go through the following steps.

1. Generate the header file
2. Generate the function wrappers
3. Build package

To do so, you can simply run the following commands:

```bash
uv run builder/build_header.py
uv run builder/build_pymeos_functions.py

uv build
```

If any of the steps fails, or you want more information about the process, the following subsections provide more details.

## 1. Generate the header file

This step is only necessary if the underlying MEOS Library has been updated. Otherwise, you can skip this step (although running it will not break anything).

To generate the header file, you just need to run the following command:

```bash
uv run builder/build_header.py
```

This command grabs the meos header and binary files from the default location and combines them into a single file ([`builder/meos.h`](builder/meos.h)) that will be used to generate the binding.

The default locations are:
- For Linux:
  - Header files: taken from `/usr/local/include/`.
  - Binary: `/usr/local/lib/libmeos.so`.
- For macOS:
  - Header files: taken from `/usr/local/include`.
  - Binary: `/usr/local/lib/libmeos.dylib`.
- For arm macOS:
  - Header files: taken from `/opt/homebrew/include`.
  - Binary: `/opt/homebrew/lib/libmeos.dylib`.

If you installed meos in a different location, you can pass the paths to the command (note that all header files must be in the same directory, as only one path is allowed):
```bash
uv run builder/build_header.py /path/to/directory/with/headers/ /path/to/binary.so
```

## 2. Generate the function wrappers

This step takes every function in the generated header file and wraps it into a Python function. The functions
