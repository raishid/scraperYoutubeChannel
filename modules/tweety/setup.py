from distutils.core import setup

setup(
    name='tweety-ns',
    packages=['tweety', 'tweety.types', 'tweety.events'],
    version='0.9.9.7',
    license='MIT',
    description='An easy Twitter Scraper',
    author='Tayyab Kharl',
    author_email='tayyabmahr@gmail.com',
    url='https://github.com/mahrtayyab/tweety',
    keywords=['TWITTER', 'TWITTER SCRAPE', 'SCRAPE TWEETS'],
    install_requires=[
        'beautifulsoup4',
        'openpyxl',
        'httpx',
        'dateutils',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
