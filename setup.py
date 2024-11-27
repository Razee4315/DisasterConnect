from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="disasterconnect",
    version="1.0.0",
    author="Saqlain Razee",
    author_email="saqlainrazee@gmail.com",
    description="A real-time disaster response coordination platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Razee4315/DisasterConnect",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "disasterconnect=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "disasterconnect": [
            "resources/*",
            "templates/*",
            "static/*",
        ],
    },
)
