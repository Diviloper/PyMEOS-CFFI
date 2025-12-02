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

# Developing PyMEOS-CFFI

The following files are used to develop PyMEOS-CFFI:

- [`builder`](builder/): directory containing all the files used to generate the MEOS Python binding and the PyMEOS-CFFI wrapper.
  - [`build_header.py`](builder/build_header.py): generates the header file ([`meos.h`](builder/meos.h)) for the MEOS Python binding.
  - [`build_pymeos.py`](builder/build_pymeos.py): builds the MEOS Python binding.
  - [`build_pymeos_functions.py`](builder/build_pymeos_functions.py): generates the Python function wrappers for the PyMEOS-CFFI package.
  - [`build_pymeos_functions_modifiers.py`](builder/build_pymeos_functions_modifiers.py): contains modifiers for some of the Python function wrappers.
  - [`objects.py`](builder/objects.py): contains the definitions of several standard conversions between Python and C types.
  - [`templates`](builder/templates/): directory containing all the template files used to generate the PyMEOS-CFFI wrapper.
    - [`init.py`](builder/templates/init.py): template for the `__init__.py` file of the PyMEOS-CFFI package. In particular, it contains the version number for the package.
    - [`functions.py`](builder/templates/functions.py): template for the `functions.py` file of the PyMEOS-CFFI package.
- [`pymeos_cffi`](pymeos_cffi/): directory containing all the files of the PyMEOS-CFFI package.
  - [`__init__.py`](pymeos_cffi/__init__.py): contains the declarations for the PyMEOS-CFFI package. This file is generated automatically.
  - [`functions.py`](pymeos_cffi/functions.py): contains the Python function wrappers for the PyMEOS-CFFI package. This file is generated automatically.
  - [`enums.py`](pymeos_cffi/enums.py): contains the Python enum wrappers for the PyMEOS-CFFI package.
  - [`errors.py`](pymeos_cffi/errors.py): contains the Python error wrappers and management functions.

> [!IMPORTANT]
> Do NOT modify manually `builder/meos.h`, `pymeos_cffi/functions.py`, or `pymeos_cffi/__init__.py`, as they are generated automatically.
> If you need to manually change the generation of the meos header file (`meos.h`), check the [builder code](builder/build_header.py) to see how it is generated.
> If you need to add some manual changes to the `pymeos_cffi` files, do them in the template files (in [`builder/templates`](builder/templates)) or through the function modifiers.

The following sections show how to build the two wrappers.
This is only needed for local testing, as the wrappers are build automatically on the repository as part of the release pipeline.

# Building the MEOS Python binding

To build the binding, you just need to perform two steps

1. Generate the header file
2. Build the binding

To do so, simply run the following commands:

```bash
uv run --no-project builder/build_header.py
uv run --no-project  builder/build_pymeos.py
```

If any of the steps fails, or you want more information about the process, the following subsections provide more details.

## 1. Generate the header file

This step is only necessary if the underlying MEOS Library has been updated. Otherwise, you can skip this step (although running it will not break anything).

To generate the header file, you just need to run the following command:

```bash
uv run --no-project  builder/build_header.py
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
uv run --no-project  builder/build_header.py /path/to/directory/with/headers/ /path/to/binary.so
```

## 2. Build bindings

This step builds the shared library based on the generated header file, and links it with the MEOS library.

To build the bindings, just run the following command:
```bash
uv run --no-project  builder/build_pymeos.py
```

As in the previous step, this command assumes that the MEOS header and binary files are in the default locations.

If they are not, you can specify alternative locations with the `MEOS_INCLUDE_DIR` and `MEOS_LIB_DIR` environment variables. Here, you can specify multiple paths for each, separated by a semicolon.

```bash
export MEOS_INCLUDE_DIR="/path/to/include/;/path/to/include2/"
export MEOS_LIB_DIR=/path/to/lib/dir/
uv run --no-project  builder/build_pymeos.py
```

> [!TIP]
> If there is any error during compilation, it is likely that the underlying MEOS platform has some changes that need special attention. Good luck with that :)

# Building the PyMEOS-CFFI Package

To update and build the PyMEOS-CFFI wrapper, you need to go through the following steps.

1. Generate the header file
2. Generate the function wrappers
3. Build package

To do so, you can simply run the following commands:

```bash
uv run --no-project  builder/build_header.py

uv run --no-project  builder/build_pymeos_functions.py
uvx ruff format
uvx ruff check --fix

uv build
```

If any of the steps fails, or you want more information about the process, the following subsections provide more details.

## 1. Generate the header file

This step is only necessary if the underlying MEOS Library has been updated. Otherwise, you can skip this step (although running it will not break anything).

To generate the header file, you just need to run the following command:

```bash
uv run --no-project  builder/build_header.py
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
uv run --no-project  builder/build_header.py /path/to/directory/with/headers/ /path/to/binary.so
```

## 2. Generate the function wrappers

This step takes every function in the generated header file and wraps it into a Python function. The functions take care of performing standard conversions between Python and C types, as well as checking if there has been any error during the execution of the MEOS function, and raising a Python exception if necessary.

To generate the function wrappers, run the following command:

```bash
uv run --no-project  builder/build_pymeos_functions.py
```

If you want to build the package afterwards, it is recommended to run the formatter on the generated code:

```bash
uvx ruff format
uvx ruff check --fix
```

> [!IMPORTANT]  
> If you are building the package to publish it, formatting is mandatory!

## 3. Build package

To build the package, just run the following command:

```bash
uv build
```

This will create a source distribution (`dist/pymeos_cffi-<version>.tar.gz`) and a built distribution (`dist/pymeos_cffi-<version>.whl`) that can be installed.

> [!NOTE]
> If you want to publish the package to PyPI, you don't need to build it first. Just push the changes to the repository and check the next section.

# Publishing to PyPI

Publishing to PyPI and creating GitHub Releases is done automatically through GitHub Actions.
To trigger it, push all the changes and then create a new tag with the following format `v<major>.<minor>.<patch>[dev]`, where `<major>`, `<minor>`, and `<patch>` are integers and `[dev]` is an optional string for development versions (e.g. `a1` or `rc3`).

Development versions are marked as prereleases automatically.

> [!IMPORTANT]
> Make sure the version of the tag matches exactly the version of the package. Otherwise, the workflow will fail and the package will not be published.
> If publishing a new version, remember always to update the version number in the (init template)[builder/tempaltes/init.py].
