# Hrenpack v2.1.2
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from setuptools import setup, find_packages

desc = '\n'.join(("Универсальная библиотека python для большинства задач", 'A universal python library for most tasks'))

BASE_REQUIREMENTS = [
    'filetype>=1.2.0',
    'bs4>=0.0.2',
    'chardet>=5.2.0',
    'charset-normalizer>=3.4.4',
    'requests>=2.32.5',
    'tqdm>=4.67.1, <=5.0.0',
    'bcrypt==5.0.0',
    'screeninfo>=0.8.1',
    'clipboard>=0.0.4',
    'psutil'
]

FLASK_REQUIREMENTS = [
    'flask>=3.1.2',
    'flask-sqlalchemy>=3.1.1',
    'flask-wtf>=1.2.2',
    'jinja2>=3.1.6',
    'markupsafe>=3.0.3',
]

REQUIREMENTS = {
    'base': BASE_REQUIREMENTS,
    'flask': BASE_REQUIREMENTS + FLASK_REQUIREMENTS,
    'all': BASE_REQUIREMENTS + FLASK_REQUIREMENTS
}

setup(
    name='hrenpack',
    version='2.2.0',
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
    install_requires=BASE_REQUIREMENTS,
    extras_require=REQUIREMENTS,
    package_data={'hrenpack': ['hrenpack/resources/*']},
    include_package_data=True
)
