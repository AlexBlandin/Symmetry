from setuptools import setup, find_packages
setup(
  name="BoardSymmetry",
  version=1.0,
  packages=find_packages(),
  scripts=["sym.py"],
  install_requires=["tabulate>=0.8.1", "tqdm>=4.30.0","psutil>=5.0.0","humanize>=2.0.0"],
  package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
  },
  author="Alex Blandin",
    author_email="a.j.blandin@swansea.ac.uk",
    description="This is an Example Package",
    url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)
