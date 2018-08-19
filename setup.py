import setuptools


with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="front_py_orm",
    version="0.0.1",
    author="Dima Lukashov",
    author_email="lds4ever2000@gmail.com",
    description="""ORM for sqlite which allows using objects from database as reactive objects.
                All changes made with single object will react on its data inside db""",
    long_description=long_description,
    url="https://github.com/DimonLuk/front-py-orm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
