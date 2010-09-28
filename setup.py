from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1.1'

install_requires = [
    'Flask>=0.6',
]

setup(name='briefs-caster',
    version=version,
    description="A server for exposing your briefcasts to the world",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development',
    ],
    keywords='',
    author='Rob Madole',
    author_email='robmadole@gmail.com',
    url='',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    scripts=['src/briefscaster/bin/bc-bs',
        'src/briefscaster/bin/bc-compact-briefs'],
    entry_points={
        'console_scripts':
            ['briefs-caster=briefscaster:main']
    }
)
