import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_restful import Api, Resource, reqparse


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except:
            str(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
api = Api(app)


class Anything(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sql', required=True, help='SELECT string to perform on database, required parameter')
        parser.add_argument('host', default=app.config.get('HOST'), help='IP of PostgreSQL database')
        parser.add_argument('port', default=app.config.get('PORT'), help='port of PostgreSQL database')
        parser.add_argument('dbname', default=app.config.get('DBNAME'), help='database name')
        parser.add_argument('username', default=app.config.get('USERNAME'), help='username for connecting to database')
        parser.add_argument('password', default=app.config.get('PASSWORD'), help='password for connecting to database')
        dbs_help = 'connection string, can be used in addition or instead of all other ' \
                   'connection params. See [33.1.1.1. Keyword/Value Connection Strings] ' \
                   'https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING '
        parser.add_argument('dcs', default=app.config.get('DCS'), help=dbs_help)
        args = parser.parse_args()

        sql = args['sql']
        if not sql.lower().startswith('select'):
            return {'error': 'Param sql should start with a SELECT'}, 400

        connection_params = {
            'dbname': args['dbname'],
            'user': args['username'],
            'password': args['password'],
            'host': args['host'],
            'port': args['port'],
            'dsn': args['dcs']
        }
        try:
            conn = psycopg2.connect(**connection_params)
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as curs:
                    curs.execute(sql)
                    response = jsonify(curs.fetchall())
                    response.status_code = 200
                    return response
            except psycopg2.Error as e:
                return {'error': type(e).__name__, 'pgcode': e.pgcode, 'pgerror': e.pgerror}, 400
            finally:
                conn.close()
        except psycopg2.Error as e:
            return {'error': type(e).__name__, 'pgcode': e.pgcode, 'pgerror': e.pgerror}, 400


api.add_resource(Anything, '/anything/')


if __name__ == '__main__':
    app.config.from_object('config')
    app.run(debug=True)
