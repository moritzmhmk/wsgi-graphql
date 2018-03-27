"""WSGI GraphQL Application."""

import graphql_server
from urllib.parse import parse_qsl
import http.client


class GraphQLApplication(object):
    """WSGI GraphQL Application."""

    def __init__(
        self,
        schema,
        execute_options={},
        format_error=graphql_server.default_format_error,
        encode=graphql_server.json_encode
    ):
        """Create Application for schema."""
        self.schema = schema
        self.execute_options = execute_options
        self.format_error = format_error
        self.encode = encode

    def __call__(self, environ, start_response):
        """Handle request."""
        try:
            headers = [('Content-type', 'application/json; charset=utf-8')]

            request_method = environ['REQUEST_METHOD'].lower()
            data = _parse_body(environ)
            query_data = dict(parse_qsl(environ.get('QUERY_STRING', '')))
            # pass environ to all callable options:
            execute_options = {
                k: v(environ) if callable(v) else v
                for k, v in self.execute_options.items()
            }

            execution_results, all_params = graphql_server.run_http_query(
                self.schema,
                request_method,
                data,
                query_data=query_data,
                **execute_options
            )

            body, status_code = graphql_server.encode_execution_results(
                execution_results,
                format_error=self.format_error,
                is_batch=isinstance(data, list),
                encode=self.encode
            )
        except Exception as e:
            print('Error {}'.format(e))
            headers = [('Content-type', 'application/json; charset=utf-8')]
            header_dict = getattr(e, 'headers', None) or {}
            headers += list(header_dict.items())
            status_code = getattr(e, 'status_code', 500)
            errors = [self.format_error(e)]
            body = self.encode({'errors': errors})

        start_response(_status(status_code), headers)
        return [body.encode('utf8')]


def _parse_body(environ):
    try:
        content_length = int(environ.get('CONTENT_LENGTH'))
    except ValueError as e:
        print('can\'t parse content_length "{}" (ValueError {})'
              .format(environ.get('CONTENT_LENGTH'), e))
        return {}
    content_type = environ['CONTENT_TYPE'].split(';')
    body = environ['wsgi.input'].read(content_length)
    if content_type[0] == 'application/graphql':
        return {'query': body.decode('utf8')}
    if content_type[0] in ('application/json', 'text/plain'):
        return graphql_server.load_json_body(body.decode('utf8'))
    if content_type[0] == 'application/x-www-form-urlencoded':
        return dict(parse_qsl(body.decode('utf8')))
    else:
        raise graphql_server.HttpQueryError(
            400,
            'Content of type "{}" is not supported.'.format(content_type[0])
        )


def _status(code):
    return '{} {}'.format(code, http.client.responses[code])
