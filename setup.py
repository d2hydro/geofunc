from setuptools import setup


setup(
    name="geofunc",
    description="functions for geoprocessing",
    author="D. Tollenaar",
    author_email="daniel@d2hydro.nl",
    url="http://daniel@d2hydro.nl",
    license="MIT",
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "geopandas",
        "rasterio"
    ],
    packages=["geofunc"],
    package_dir={"geofunc": "geofunc"},
    zip_safe=False,
    keywords="raster, geoprocessing",
)
