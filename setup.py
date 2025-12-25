from setuptools import setup, find_packages

setup(
    name="ds-algo-lab",
    version="0.1.0",
    description="A Python-based educational platform for studying data structures and algorithms",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "pytest>=7.0.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
    ],
)

