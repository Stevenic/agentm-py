from setuptools import setup, find_packages

setup(
    name='agentm-py',
    version='0.1',
    python_requires='>=3.9',
    install_requires=['openai>=1.40', 'pydantic>=2', 'jsonschema>=4', 'tiktoken'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)