# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from setuptools import setup, find_packages

desc = '\n'.join(("Универсальная библиотека python для большинства задач", 'A universal python library for most tasks'))
req = open('requirements.txt').read().split('\n')


setup(
    name='hrenpack',
    version='2.0.0',
    author_email='magilyas.doma.09@list.ru',
    author='Маг Ильяс DOMA (MagIlyas_DOMA)',
    description=desc,
    license='BSD 3-Clause License',
    url='https://github.com/MagIlyas-DOMA/hrenpack',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=req,
    package_data={'hrenpack': ['hrenpack/resources/*']},
    include_package_data=True,
)
