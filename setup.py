from setuptools import find_packages, setup

setup(
    name="git-recommend",
    version="0.1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "git-recommend=main:main",
        ],
    },
    packages=find_packages(),
    install_requires=[
        # any dependencies, e.g. "requests>=2.0"
        "google-generativeai",
        "python-dotenv",
        "rank_bm25"
    ],
)
