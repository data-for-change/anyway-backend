from flask_restplus import Namespace, Resource, fields
from flask import jsonify
from anyway import db
from anyway.apis.common.models import RoadSegment
from flask_restplus import reqparse

road_segments_api = Namespace('road_segments', description='Polygons API')

@road_segments_api.route('/get_road_segment')
class GetRoadSegment(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('yishuv_name')
        args = parser.parse_args()
        result_all = db.session.query(RoadSegment).filter(RoadSegment.yishuv_name.in_(['חיפה'])).all()
        entries = [road_segment.serialize() for road_segment in result_all]
        retMap = {
            'status_code': 200,
            'data': entries
        }
        return jsonify(retMap)