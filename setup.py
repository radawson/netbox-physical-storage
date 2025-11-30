from setuptools import find_packages, setup

setup(
    name='netbox-physical-storage',
    version='0.1.0',
    description='A NetBox plugin for managing physical storage devices',
    author='R. Dawson',
    author_email='dawsonra@clockworx.org',  
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
