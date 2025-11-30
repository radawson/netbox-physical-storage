from setuptools import find_packages, setup

setup(
    name='netbox-physical-storage',
    version='0.1',
    description='A NetBox plugin',
    install_requires=[
        'netbox>=4.0.0,<4.5.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
