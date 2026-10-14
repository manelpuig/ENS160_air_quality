from glob import glob
import os

from setuptools import find_packages, setup


package_name = "ens160_air_quality_ros"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Manel Puig",
    maintainer_email="manel.puig@ub.edu",
    description="ROS 2 serial reader for ENS160 air-quality sensors.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "air_quality_node = ens160_air_quality_ros.air_quality_node:main",
        ],
    },
)
