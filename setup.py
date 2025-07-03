from setuptools import setup,find_packages

with open("requirements.txt") as f:
    lst = (f.readlines())

final = []
for i in range(len(lst)):
    final.append(lst[i][0:-1])

final = final[0:len(final)-1]

setup(
name= "Kunsh Bhatia",
version="0.0.1",
author="Kunsh",
packages=find_packages(),    # Help in figuring out __init__.py file in folders
install_requires=final
)