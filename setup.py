from setuptools import find_packages, setup

# Find all packages including src as the root namespace
all_packages = ['src'] + [f'src.{pkg}' for pkg in find_packages(where="src")]

setup(
    name="ds-algo-lab",
    version="0.1.0",
    description="A Python-based educational platform for studying data structures and algorithms",
    author="Your Name",
    packages=all_packages,
    package_dir={"src": "src"},
    python_requires=">=3.7",
    install_requires=[
        "pytest>=7.0.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "click>=8.0.0",
        "pillow>=9.0.0",
    ],
    entry_points={
        'console_scripts': [
            'dsa-lab=src.cli.playground_cli:main',
        ],
    },
)
