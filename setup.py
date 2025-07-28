import os
import shutil

from setuptools import setup

# Copy PROJ data to package data
package_data = []

# Conditionally copy PROJ DATA to make self-contained wheels
if os.environ.get("PACKAGE_DATA"):
    print("Copying PROJ data to package data")
    projdatadir = os.environ.get(
        "PROJ_DATA", os.environ.get("PROJ_LIB", "/usr/local/share/proj")
    )
    if os.path.exists(projdatadir):
        shutil.rmtree("pymeos_cffi/proj_data", ignore_errors=True)
        shutil.copytree(
            projdatadir,
            "pymeos_cffi/proj_data",
            ignore=shutil.ignore_patterns("*.txt", "*.tif"),
        )  # Don't copy .tiff files and their related .txt files
    else:
        raise FileNotFoundError(
            f"PROJ data directory not found at {projdatadir}. "
            f"Unable to generate self-contained wheel."
        )
    package_data.append("proj_data/*")
else:
    print("Not copying PROJ data to package data")

# Copy MEOS spatial reference table (spatial_ref_sys.csv)
print("Copying MEOS spatial reference table to package data")
spatial_ref_sys_path = os.environ.get(
    "MEOS_SPATIAL_REF_SYS_PATH", "/usr/local/share/spatial_ref_sys.csv"
)
shutil.rmtree("pymeos_cffi/meos_data", ignore_errors=True)
os.makedirs("pymeos_cffi/meos_data", exist_ok=True)
shutil.copy(
    spatial_ref_sys_path,
    "pymeos_cffi/meos_data/spatial_ref_sys.csv",
)
package_data.append("meos_data/*")

setup(
    packages=["pymeos_cffi"],
    package_data={"pymeos_cffi": package_data},
    setup_requires=["cffi"],
    cffi_modules=["builder/build_pymeos.py:ffibuilder"],
)
