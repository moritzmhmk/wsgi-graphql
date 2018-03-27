"""Example WSGI Application using GraphQLApplication."""

from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString
from wsgi_graphql import GraphQLApplication

schema = GraphQLSchema(
    query=GraphQLObjectType(
      name='RootQueryType',
      fields={
        'hello': GraphQLField(
          type=GraphQLString,
          resolver=lambda root, info: info.context['greet']
        )
      }
    )
)

application = GraphQLApplication(schema, execute_options={
    'context_value': lambda environ: {
        'greet': environ.get('HTTP_GREET')
    }
})

# curl --request POST\
#  --url http://localhost:8080\
#  --header 'Content-Type: application/graphql'\
#  --header 'greet: world'\
#  --data 'query {hello}'

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    host = 'localhost'
    port = 8080
    srv = make_server(host, port, application)
    print('serving on {}:{}'.format(host, port))
    srv.serve_forever()
