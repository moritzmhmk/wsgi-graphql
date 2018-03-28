from setuptools import setup

version = '0.0.1'
url = 'https://github.com/moritzmhmk/wsgi-graphql'
download_url = '{}/archive/v{}.tar.gz'.format(url, version)

setup(
    name='wsgi_graphql',
    py_modules=['wsgi_graphql'],
    version=version,
    description='Create a WSGI Application for a GraphQL schema.',
    long_description=open('README.rst').read(),
    author='Moritz K.',
    author_email='moritzmhmk@googlemail.com',
    url=url,
    download_url=download_url,
    install_requires=['graphql-server-core'],
    license='MIT',
    keywords=['graphql', 'wsgi', 'api', 'rest'],
    classifiers=[],
)
