WSGI-GraphQL
=============

Create a WSGI Application for a GraphQL schema.

Usage
-----

Use the ``GraphQLApplication`` from ``wsgi_graphql``.

.. code:: python

    from wsgi_graphql import GraphQLApplication
    application = GraphQLApplication(schema)

Options
~~~~~~~

- ``schema``: ``GraphQLSchema`` to serve with this application.
- ``execute_options``: Dictionary of options to be passed to ``graphql.execute``
  via ``graphql_server.run_http_query``. If the dictionary values are callable
  they will be called (see example below).
- ``format_error``: Function to format errors (defaults to ``graphql_server.default_format_error``).
- ``encode``: Function to encode dictionary (defaults to ``graphql_server.json_encode``).

All ``execute_options`` can be ``callable`` (i.e. functions) and will receive
the current ``environ`` as an argument. This can be used for tasks like parsing
authentication tokens and inserting results as ``context_value``.

This snippet from the ``example.py`` sets the ``context_value`` to a dictionary
containing the value of the request header ``greet``.

.. code:: python

  application = GraphQLApplication(schema, execute_options={
      'context_value': lambda environ: {
          'greet': environ.get('HTTP_GREET')
      }
  })

This ``curl`` command will return ``{"data":{"hello":"world"}}``.

.. code:: bash

  curl --request POST\
   --url http://localhost:8080\
   --header 'Content-Type: application/graphql'\
   --header 'greet: world'\
   --data 'query {hello}'
