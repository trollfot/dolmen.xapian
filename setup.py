import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    
setup(
    name="dolmen.xapian",
    version="0.1",
    install_requires=[
        'setuptools',
        'xappy',
        'transaction',
        'grokcore.component',
        'zope.schema',
        'zope.site',
        'zope.component',
        'zope.container',
        'zope.lifecycleevent'],
    packages=find_packages('src'),
    package_dir= {'':'src'},
    namespace_packages=['dolmen'],
    package_data = {
    '': ['*.txt', '*.zcml'],
    },
    zip_safe=False,
    classifiers = [
        'Intended Audience :: Developers',
        'Framework :: Zope3'
        ],
    url="",
    keywords="zope3 index search xapian xappy",
    author='Souheil Chelfouh, based on the work of Kapil Thangavelu',
    author_email='souheil@chelfouh.com',
    description="A Xapian Content Indexing/Searching Framework for Grok",
    long_description=(
        read('src','dolmen','xapian','README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        + '\n\n'
        ),
    license='GPL',
    )
