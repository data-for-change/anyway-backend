from flask_restplus import Api

from .markers.api import markers_api
from .rsa.api import rsa_api
from .road_segments.api import road_segments_api


api = Api(
    title='Anyway',
    version='1.0',
    description='Anyway API'
)

api.add_namespace(markers_api, path='/markers')
api.add_namespace(rsa_api, path='/rsa')
api.add_namespace(road_segments_api, path='/road_segments')