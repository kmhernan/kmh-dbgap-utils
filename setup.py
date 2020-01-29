from setuptools import setup, find_packages

setup(
    name = "kmh-dbgap-utils",
    author = "Kyle Hernandez",
    version = 0.1,
    description = "Helper utils for dbGap", 
    license = "Apache 2.0",
    packages = find_packages(),
    setup_requires = [],
    tests_require = [],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points= {
        'console_scripts': [
            'kmh-dbgap-utils = kmh_dbgap_utils.__main__:main'
        ]
    }
)
