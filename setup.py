from setuptools import setup

setup(name='gplaydl',
	version='1.4.0',
	description='Google Play APK downloader command line utility that utilizes gpapi to download APK files of free apps and games.',
	author="Backryun",
	author_email="bakryun0718@gmail.com",
	url="https://github.com/backryun/gplaydl2",
	python_requires='>3.2.0',
	license="MIT",
	entry_points={
		'console_scripts': [
			'gplaydl = gplaydl.gplaydl:main'
		],
	},
	packages=[
		'gplaydl'
	],
	install_requires=[
		'certifi==2022.12.7',
		'cffi==1.15.1',
		'chardet==5.1.0',
		'cryptography==3.4.8',
		'decorator==4.4.2',
		'gpapi==1.0.0',
		'idna==2.10',
		'protobuf==3.20.3',
		'pycparser==2.21',
		'requests==2.28.2',
		'six==1.14.0',
		'termcolor==1.1.0',
		'urllib3==1.25.11',
		'validators==0.14.3'
	]
)
