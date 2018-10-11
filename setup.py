from setuptools import setup

setup(
    name='scrapy_fake_useragent',
    version='0.1.0',
    description='Use a random User-Agent provided by fake-useragent for every request',
    long_description=open('README.rst').read(),
    keywords='scrapy proxy user-agent web-scraping',
    license='New BSD License',
    author="Neal Wong",
    author_email='ibprnd@gmail.com',
    url='https://github.com/Qiulin-Wang/scrapy-fake-useragent',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'scrapy_fake_useragent',
    ],
    install_requires=[
        'fake-useragent',
        'user-agents'
    ],
)
