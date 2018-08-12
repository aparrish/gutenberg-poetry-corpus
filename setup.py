from setuptools import setup
    
with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='gutenbergpoetrycorpus',
    version='0.0.1',
    author='Allison Parrish',
    author_email='allison@decontextualize.com',
    url='https://github.com/aparrish/gutenberg-poetry-corpus',
    description='A corpus of poetry from Project Gutenberg',
    long_description=readme,
    packages=setuptools.find_packages(),
    install_requires=[
        'gutenbergdammit==0.0.2',
        'wordfilter'
    ],
    dependency_links=[
        'https://github.com/aparrish/gutenberg-dammit/archive/master.zip#egg=gutenbergdammit-0.0.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        'Programming Language :: Python :: 3',
    ],
    platforms='any',
)
