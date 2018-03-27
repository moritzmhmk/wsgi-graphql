from distutils.core import setup
setup(
    name='wsgi_graphql',
    py_modules=['wsgi_graphql'],
    version='0.0.1',
    description='Create a WSGI Application for a GraphQL schema.',
    long_description=open('README.rst').read(),
    author='Moritz K.',
    author_email='moritzmhmk@googlemail.com',
    url='https://github.com/moritzmhmk/wsgi-graphql',
    download_url='https://github.com/moritzmhmk/wsgi-graphql/archive/0.0.1.tar.gz',
    install_requires=['graphql-server-core'],
    license='MIT',
    keywords=['graphql', 'wsgi', 'api', 'rest'],
    classifiers=[],
)
