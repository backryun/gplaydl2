from setuptools import setup

setup(name='gplaydl',
	version='1.4.0',
	description='Google Play APK downloader command line utility that utilizes gpapi to download APK files of free apps and games.',
	author="Backryun",
	author_email="bakryun0718@gmail.com",
	url="https://github.com/backryun/gplaydl2",
	python_requires='>=3.14.0',
	license="GPLv3",
	entry_points={
		'console_scripts': [
			'gplaydl = gplaydl.gplaydl:main'
		],
	},
	packages=[
		'gplaydl',
		'gplaydl.api'
	],
	package_data={
		'gplaydl.api': ['device.properties']
	},
	install_requires=[
		'certifi==2025.10.5',
		'cffi==2.0.0',
		'chardet==5.2.0',
		'cryptography==46.0.3',
		'decorator==5.2.1',
		'idna==3.11',
		'protobuf==6.33.0',
		'pycparser==2.23',
		'requests==2.32.5',
		'six==1.17.0',
		'termcolor==3.2.0',
		'urllib3==2.5.0',
		'validators==0.35.0'
	]
)
