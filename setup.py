from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='file-manip-toolkit',
    version='1.0',
    description='collection of tools for low level binary manipulations of files',
    long_description=readme,
    author='M B',
    author_email='dont@me',
    license=license,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'unfman=file_manip_toolkit.cli:unfman_main',
            'eswap=file_manip_toolkit.cli:eswap_main'],
        }
    )
