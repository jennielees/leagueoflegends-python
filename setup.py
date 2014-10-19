from distutils.core import setup

long_description = open('README.md').read()

setup(name="leagueoflegends",
      version="1.4",
      py_modules=["leagueoflegends.leagueoflegends"],
      description="Unofficial libraries for interacting with the official League of Legends API",
      author="Jennie Lees <jennielees@gmail.com>",
      author_email="jennielees@gmail.com",
      license="WTFPL",
      url="http://github.com/jennielees/leagueoflegends-python",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development" +
                   " :: Libraries :: Python Modules",
                   ]
      )
