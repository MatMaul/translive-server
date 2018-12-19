from setuptools import setup

setup(name='translive-server',
      version='0.0.1',
      description='translive-server',
      url="https://github.com/MatMaul/translive-server",
      author='Mathieu Velten',
      author_email='matmaul@gmail.com',
      packages=['translive_server'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
      ],
      install_requires=['pytranslive', 'aiohttp'],
      zip_safe=True)
