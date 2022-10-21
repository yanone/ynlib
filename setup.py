from setuptools import setup, find_packages
import platform

WIN = platform.system() == "Windows"
MAC = platform.system() == "Darwin"
LINUX = platform.system() == "Linux"

install_requires = [  # I get to this in a second
]

setup(
    name="ynlib",  # How you named your package folder (MyLib)
    version="0.1.0",  # .post2
    license="apache-2.0",
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    url="https://github.com/yanone/ynlib",
    install_requires=install_requires,
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    include_package_data=True,
)
