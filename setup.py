#!/usr/bin/env python3
"""
Setup script for Bob_MREF2_MCP package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="bob-mref2-mcp",
    version="2.0.0",
    author="IBM",
    author_email="rbhavar@ibm.com",
    description="MCP Server for Maximo Real Estate and Facilities (TRIRIGA) Integration with IBM Bob",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/ibm/bob-mref2-mcp",  # Update with actual repo URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.9.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bob-mref2-mcp=bob_mref2_mcp.mref_comprehensive_mcp_server:main",
            "mref-fetch-contracts=bob_mref2_mcp.fetch_all_contracts_now:main",
        ],
    },
    include_package_data=True,
    package_data={
        "bob_mref2_mcp": [
            "config.json",
            "*.md",
        ],
    },
    zip_safe=False,
    keywords="mcp tririga maximo real-estate facilities ibm bob",
    project_urls={
        "Documentation": "https://github.com/ibm/bob-mref2-mcp/blob/main/README.md",
        "Source": "https://github.com/ibm/bob-mref2-mcp",
        "Tracker": "https://github.com/ibm/bob-mref2-mcp/issues",
    },
)

# Made with Bob
