from setuptools import setup

with open("Readme.md", 'r') as f:
    long_description = f.read()

setup(
    name='PyCollision',
    version='0.0.1',
    description="This library helps to detect collision more efficiently for image with transparency",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Paul',
    url="https://github.com/PaulleDemon/PyCollision",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    keywords=['Collision', 'pygame', 'python collision', 'Rectangular collision', 'pycollision'],
    packages=["pycollision"],
    include_package_data=True,
    install_requires=["numpy",
                      "pillow"],
    python_requires='>=3.5',
)