# Hrenpack v2.1.2
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from setuptools import setup, find_packages

desc = '\n'.join(("Универсальная библиотека python для большинства задач", 'A universal python library for most tasks'))
req = open('requirements.txt').read().split('\n')


setup(
    name='hrenpack',
    version='2.1.2',
    author_email='magilyas.doma.09@list.ru',
    author='Маг Ильяс DOMA (MagIlyasDOMA)',
    description=desc,
    license='MIT',
    url='https://github.com/MagIlyas-DOMA/hrenpack',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    platforms=[
        "Windows",
        "Windows 10",
        "Windows 11",
        "Windows Server 2019+",
    ],
    project_urls=dict(
        Source="https://github.com/MagIlyas-DOMA/hrenpack",
        Documentation="https://magilyasdoma.github.io/hrenpack/documentation.html",
    ),
    python_requires='>=3.10',
    install_requires=req,
    package_data={'hrenpack': ['hrenpack/resources/*']},
    include_package_data=True
)
