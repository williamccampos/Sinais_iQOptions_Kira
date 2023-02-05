"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)


setup(
    name="iqoptionapi",
    version="6.8.9.1",
    packages=find_packages(),
    install_requires=["pylint","requests","websocket-client==0.56"],
    include_package_data = True,
    description="Versão mais atualizada da API IQ Options",
    long_description="Versão mais atualizada da API IQ Options",
    url="https://github.com/williamccampos/iqoptionapi",
    author="William Campos",
    author_email="william.campos29@gmail.com",
    zip_safe=False
)
