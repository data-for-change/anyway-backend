import datetime
import json
import logging
from collections import namedtuple

from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from six import iteritems
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Index, desc, \
    sql, Table, \
    ForeignKeyConstraint, func, and_, TIMESTAMP
from sqlalchemy.orm import relationship, load_only, backref

from anyway.core.localization import Localization
from anyway.core.constants import CONST
from anyway.core.database import CBSBase
from anyway.core.utils import Utils

from anyway import db

MarkerResult = namedtuple('MarkerResult', ['accident_markers', 'rsa_markers', 'total_records'])
logging.basicConfig(level=logging.DEBUG)
db_encoding = 'utf-8'

class Point(object):
    id = Column(Integer(), primary_key=True)
    latitude = Column(Float())
    longitude = Column(Float())


class MarkerMixin(Point):
    type = Column(Integer())
    title = Column(String(100))
    created = Column(DateTime, default=datetime.datetime.now, index=True)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    @staticmethod
    def format_description(field, value):
        # if the field's value is a static localizable field, fetch it.
        if field in Localization.get_supported_tables():
            value = Utils.decode_hebrew(Localization.get_field(field, value), db_encoding)
        name = Utils.decode_hebrew(Localization.get_field(field), db_encoding)
        return u"{0}: {1}".format(name, value)

class AccidentMarker(MarkerMixin, CBSBase):
    __tablename__ = "markers"
    __table_args__ = (
        Index('acc_long_lat_idx', 'latitude', 'longitude'),
        Index('id_idx_markers', 'id', unique=False),
        Index('provider_and_id_idx_markers', 'provider_and_id', unique=False),

    )

    __mapper_args__ = {
        'polymorphic_identity': CONST.MARKER_TYPE_ACCIDENT
    }
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    file_type_police = Column(Integer())
    description = Column(Text())
    accident_type = Column(Integer())
    accident_severity = Column(Integer())
    address = Column(Text())
    location_accuracy = Column(Integer())
    road_type = Column(Integer())
    road_shape = Column(Integer())
    day_type = Column(Integer())
    police_unit = Column(Integer())
    mainStreet = Column(Text())
    secondaryStreet = Column(Text())
    junction = Column(Text())
    one_lane = Column(Integer())
    multi_lane = Column(Integer())
    speed_limit = Column(Integer())
    road_intactness = Column(Integer())
    road_width = Column(Integer())
    road_sign = Column(Integer())
    road_light = Column(Integer())
    road_control = Column(Integer())
    weather = Column(Integer())
    road_surface = Column(Integer())
    road_object = Column(Integer())
    object_distance = Column(Integer())
    didnt_cross = Column(Integer())
    cross_mode = Column(Integer())
    cross_location = Column(Integer())
    cross_direction = Column(Integer())
    involved = relationship("Involved")
    vehicles = relationship("Vehicle")
    video_link = Column(Text())
    road1 = Column(Integer())
    road2 = Column(Integer())
    km = Column(Float())
    km_raw = Column(Text())
    km_accurate = Column(Boolean())
    yishuv_symbol = Column(Integer())
    yishuv_name = Column(Text())
    geo_area = Column(Integer())
    day_night = Column(Integer())
    day_in_week = Column(Integer())
    traffic_light = Column(Integer())
    region = Column(Integer())
    district = Column(Integer())
    natural_area = Column(Integer())
    municipal_status = Column(Integer())
    yishuv_shape = Column(Integer())
    street1 = Column(Integer())
    street1_hebrew = Column(Text())
    street2 = Column(Integer())
    street2_hebrew = Column(Text())
    house_number = Column(Integer())
    urban_intersection = Column(Integer())
    non_urban_intersection = Column(Integer())
    non_urban_intersection_hebrew = Column(Text())
    accident_year = Column(Integer(), primary_key=True)
    accident_month = Column(Integer())
    accident_day = Column(Integer())
    accident_hour_raw = Column(Integer())
    accident_hour = Column(Integer())
    accident_minute = Column(Integer())
    x = Column(Float())
    y = Column(Float())
    vehicle_type_rsa = Column(Text())
    violation_type_rsa = Column(Text())
    geom = Column(Geometry('POINT'), index=True)
    non_urban_intersection_by_junction_number = Column(Text())
    rsa_severity = Column(Integer())
    rsa_license_plate = Column(Text())

    @staticmethod
    def json_to_description(msg):
        description = json.loads(msg, encoding=db_encoding)
        return "\n".join([AccidentMarker.format_description(field, value) for field, value in iteritems(description)])


class Involved(CBSBase):
    __tablename__ = "involved"
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer())
    file_type_police = Column(Integer())
    accident_id = Column(BigInteger())
    involved_type = Column(Integer())
    license_acquiring_date = Column(Integer())
    age_group = Column(Integer())
    sex = Column(Integer())
    vehicle_type = Column(Integer())
    safety_measures = Column(Integer())
    involve_yishuv_symbol = Column(Integer())
    involve_yishuv_name = Column(Text())
    injury_severity = Column(Integer())
    injured_type = Column(Integer())
    injured_position = Column(Integer())
    population_type = Column(Integer())
    home_region = Column(Integer())
    home_district = Column(Integer())
    home_natural_area = Column(Integer())
    home_municipal_status = Column(Integer())
    home_yishuv_shape = Column(Integer())
    hospital_time = Column(Integer())
    medical_type = Column(Integer())
    release_dest = Column(Integer())
    safety_measures_use = Column(Integer())
    late_deceased = Column(Integer())
    car_id = Column(Integer())
    involve_id = Column(Integer())
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    __table_args__ = (ForeignKeyConstraint([accident_id, provider_code, accident_year],
                                           [AccidentMarker.id, AccidentMarker.provider_code,
                                            AccidentMarker.accident_year],
                                           ondelete="CASCADE"),
                      Index('accident_id_idx_involved', 'accident_id', unique=False),
                      Index('provider_and_id_idx_involved', 'provider_and_id', unique=False),
                      {})



class City(CBSBase):
    __tablename__ = "cities"
    id = Column(Integer(), primary_key=True)
    symbol_code = Column(Integer())
    name = Column(String())
    search_heb = Column(String())
    search_eng = Column(String())
    search_priority = Column(Integer())

class RegisteredVehicle(CBSBase):
    __tablename__ = "cities_vehicles_registered"
    id = Column(Integer(), primary_key=True)
    city_id = Column(Integer())
    year = Column(Integer())
    name = Column(String())
    name_eng = Column(String())
    search_name = Column(String())
    motorcycle = Column(Integer())
    special = Column(Integer())
    taxi = Column(Integer())
    bus = Column(Integer())
    minibus = Column(Integer())
    truck_over3500 = Column(Integer())
    truck_upto3500 = Column(Integer())
    private = Column(Integer())
    population_year = Column(Integer())
    population = Column(Integer())
    total = Column(Integer())


class Vehicle(CBSBase):
    __tablename__ = "vehicles"
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer())
    file_type_police = Column(Integer())
    accident_id = Column(BigInteger())
    engine_volume = Column(Integer())
    manufacturing_year = Column(Integer())
    driving_directions = Column(Integer())
    vehicle_status = Column(Integer())
    vehicle_attribution = Column(Integer())
    vehicle_type = Column(Integer())
    seats = Column(Integer())
    total_weight = Column(Integer())
    car_id = Column(Integer())
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    vehicle_damage = Column(Integer())
    __table_args__ = (ForeignKeyConstraint([accident_id, provider_code, accident_year],
                                           [AccidentMarker.id, AccidentMarker.provider_code,
                                            AccidentMarker.accident_year],
                                           ondelete="CASCADE"),
                      Index('accident_id_idx_vehicles', 'accident_id', unique=False),
                      Index('provider_and_id_idx_vehicles', 'provider_and_id', unique=False),
                      {})


class ColumnsDescription(CBSBase):
    __tablename__ = "columns_description"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    column_description = Column(Text(), nullable=True)


class PoliceUnit(CBSBase):
    __tablename__ = "police_unit"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    police_unit_hebrew = Column(Text(), nullable=True)


class RoadType(CBSBase):
    __tablename__ = "road_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_type_hebrew = Column(Text(), nullable=True)


class AccidentSeverity(CBSBase):
    __tablename__ = "accident_severity"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    accident_severity_hebrew = Column(Text(), nullable=True)


class AccidentType(CBSBase):
    __tablename__ = "accident_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    accident_type_hebrew = Column(Text(), nullable=True)


class RoadShape(CBSBase):
    __tablename__ = "road_shape"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_shape_hebrew = Column(Text(), nullable=True)


class OneLane(CBSBase):
    __tablename__ = "one_lane"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    one_lane_hebrew = Column(Text(), nullable=True)


class MultiLane(CBSBase):
    __tablename__ = "multi_lane"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    multi_lane_hebrew = Column(Text(), nullable=True)


class SpeedLimit(CBSBase):
    __tablename__ = "speed_limit"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    speed_limit_hebrew = Column(Text(), nullable=True)


class RoadIntactness(CBSBase):
    __tablename__ = "road_intactness"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_intactness_hebrew = Column(Text(), nullable=True)


class RoadWidth(CBSBase):
    __tablename__ = "road_width"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_width_hebrew = Column(Text(), nullable=True)


class RoadSign(CBSBase):
    __tablename__ = "road_sign"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_sign_hebrew = Column(Text(), nullable=True)


class RoadLight(CBSBase):
    __tablename__ = "road_light"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_light_hebrew = Column(Text(), nullable=True)


class RoadControl(CBSBase):
    __tablename__ = "road_control"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_control_hebrew = Column(Text(), nullable=True)


class Weather(CBSBase):
    __tablename__ = "weather"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    weather_hebrew = Column(Text(), nullable=True)


class RoadSurface(CBSBase):
    __tablename__ = "road_surface"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_surface_hebrew = Column(Text(), nullable=True)


class RoadObjecte(CBSBase):
    __tablename__ = "road_object"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    road_object_hebrew = Column(Text(), nullable=True)


class ObjectDistance(CBSBase):
    __tablename__ = "object_distance"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    object_distance_hebrew = Column(Text(), nullable=True)


class DidntCross(CBSBase):
    __tablename__ = "didnt_cross"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    didnt_cross_hebrew = Column(Text(), nullable=True)


class CrossMode(CBSBase):
    __tablename__ = "cross_mode"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    cross_mode_hebrew = Column(Text(), nullable=True)


class CrossLocation(CBSBase):
    __tablename__ = "cross_location"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    cross_location_hebrew = Column(Text(), nullable=True)


class CrossDirection(CBSBase):
    __tablename__ = "cross_direction"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    cross_direction_hebrew = Column(Text(), nullable=True)


class DrivingDirections(CBSBase):
    __tablename__ = "driving_directions"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    driving_directions_hebrew = Column(Text(), nullable=True)


class VehicleStatus(CBSBase):
    __tablename__ = "vehicle_status"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    vehicle_status_hebrew = Column(Text(), nullable=True)


class InvolvedType(CBSBase):
    __tablename__ = "involved_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    involved_type_hebrew = Column(Text(), nullable=True)


class SafetyMeasures(CBSBase):
    __tablename__ = "safety_measures"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    safety_measures_hebrew = Column(Text(), nullable=True)


class InjurySeverity(CBSBase):
    __tablename__ = "injury_severity"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    injury_severity_hebrew = Column(Text(), nullable=True)


class DayType(CBSBase):
    __tablename__ = "day_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    day_type_hebrew = Column(Text(), nullable=True)


class DayNight(CBSBase):
    __tablename__ = "day_night"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    day_night_hebrew = Column(Text(), nullable=True)


class DayInWeek(CBSBase):
    __tablename__ = "day_in_week"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    day_in_week_hebrew = Column(Text(), nullable=True)


class TrafficLight(CBSBase):
    __tablename__ = "traffic_light"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    traffic_light_hebrew = Column(Text(), nullable=True)


class VehicleAttribution(CBSBase):
    __tablename__ = "vehicle_attribution"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    vehicle_attribution_hebrew = Column(Text(), nullable=True)


class VehicleType(CBSBase):
    __tablename__ = "vehicle_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    vehicle_type_hebrew = Column(Text(), nullable=True)


class InjuredType(CBSBase):
    __tablename__ = "injured_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    injured_type_hebrew = Column(Text(), nullable=True)


class InjuredPosition(CBSBase):
    __tablename__ = "injured_position"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    injured_position_hebrew = Column(Text(), nullable=True)


class AccidentMonth(CBSBase):
    __tablename__ = "accident_month"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    accident_month_hebrew = Column(Text(), nullable=True)


class PopulationType(CBSBase):
    __tablename__ = "population_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    population_type_hebrew = Column(Text(), nullable=True)


class Sex(CBSBase):
    __tablename__ = "sex"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    sex_hebrew = Column(Text(), nullable=True)


class GeoArea(CBSBase):
    __tablename__ = "geo_area"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    geo_area_hebrew = Column(Text(), nullable=True)


class Region(CBSBase):
    __tablename__ = "region"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    region_hebrew = Column(Text(), nullable=True)


class MunicipalStatus(CBSBase):
    __tablename__ = "municipal_status"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    municipal_status_hebrew = Column(Text(), nullable=True)


class District(CBSBase):
    __tablename__ = "district"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    district_hebrew = Column(Text(), nullable=True)


class NaturalArea(CBSBase):
    __tablename__ = "natural_area"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    natural_area_hebrew = Column(Text(), nullable=True)


class YishuvShape(CBSBase):
    __tablename__ = "yishuv_shape"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    yishuv_shape_hebrew = Column(Text(), nullable=True)


class AgeGroup(CBSBase):
    __tablename__ = "age_group"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    age_group_hebrew = Column(Text(), nullable=True)


class AccidentHourRaw(CBSBase):
    __tablename__ = "accident_hour_raw"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    accident_hour_raw_hebrew = Column(Text(), nullable=True)


class EngineVolume(CBSBase):
    __tablename__ = "engine_volume"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    engine_volume_hebrew = Column(Text(), nullable=True)


class TotalWeight(CBSBase):
    __tablename__ = "total_weight"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    total_weight_hebrew = Column(Text(), nullable=True)


class HospitalTime(CBSBase):
    __tablename__ = "hospital_time"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    hospital_time_hebrew = Column(Text(), nullable=True)


class MedicalType(CBSBase):
    __tablename__ = "medical_type"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    medical_type_hebrew = Column(Text(), nullable=True)


class ReleaseDest(CBSBase):
    __tablename__ = "release_dest"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    release_dest_hebrew = Column(Text(), nullable=True)


class SafetyMeasuresUse(CBSBase):
    __tablename__ = "safety_measures_use"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    safety_measures_use_hebrew = Column(Text(), nullable=True)


class LateDeceased(CBSBase):
    __tablename__ = "late_deceased"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    late_deceased_hebrew = Column(Text(), nullable=True)


class LocationAccuracy(CBSBase):
    __tablename__ = "location_accuracy"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    location_accuracy_hebrew = Column(Text(), nullable=True)


class ProviderCode(CBSBase):
    __tablename__ = "provider_code"
    id = Column(Integer(), primary_key=True, index=True)
    provider_code_hebrew = Column(Text(), nullable=True)


class VehicleDamage(CBSBase):
    __tablename__ = "vehicle_damage"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer(), primary_key=True, index=True)
    provider_code = Column(Integer(), primary_key=True, index=True)
    vehicle_damage_hebrew = Column(Text(), nullable=True)

class RoadSegments(CBSBase):
    __tablename__ = "road_segments"
    id = Column(Integer(), primary_key=True)
    segment_id = Column(Integer())
    road = Column(Integer())
    segment = Column(Integer())
    from_km = Column(Float())
    from_name = Column(Text())
    to_km = Column(Float())
    to_name = Column(Text())


class TrafficVolume(CBSBase):
    __tablename__ = "traffic_volume"
    id = Column(Integer(), primary_key=True, index=True)
    year = Column(Integer())
    road = Column(Integer())
    section = Column(Integer())
    lane = Column(Integer())
    month = Column(Integer())
    day = Column(Integer())
    day_of_week = Column(Integer())
    hour = Column(Integer())
    volume = Column(Integer())
    status = Column(Integer())
    duplicate_count = Column(Integer())


class AccidentMarkerView(CBSBase):
    __tablename__ = "markers_hebrew"
    id = Column(BigInteger(), primary_key=True)
    accident_timestamp = Column(DateTime, default=None)
    provider_code = Column(Integer(), primary_key=True)
    provider_code_hebrew = Column(Text())
    accident_type = Column(Integer())
    accident_type_hebrew = Column(Text())
    accident_severity = Column(Integer())
    accident_severity_hebrew = Column(Text())
    location_accuracy = Column(Integer())
    location_accuracy_hebrew = Column(Text())
    road_type = Column(Integer())
    road_type_hebrew = Column(Text())
    road_shape = Column(Integer())
    road_shape_hebrew = Column(Text())
    day_type = Column(Integer())
    day_type_hebrew = Column(Text())
    police_unit = Column(Integer())
    police_unit_hebrew = Column(Text())
    one_lane = Column(Integer())
    one_lane_hebrew = Column(Text())
    multi_lane = Column(Integer())
    multi_lane_hebrew = Column(Text())
    speed_limit = Column(Integer())
    speed_limit_hebrew = Column(Text())
    road_intactness = Column(Integer())
    road_intactness_hebrew = Column(Text())
    road_width = Column(Integer())
    road_width_hebrew = Column(Text())
    road_sign = Column(Integer())
    road_sign_hebrew = Column(Text())
    road_light = Column(Integer())
    road_light_hebrew = Column(Text())
    road_control = Column(Integer())
    road_control_hebrew = Column(Text())
    weather = Column(Integer())
    weather_hebrew = Column(Text())
    road_surface = Column(Integer())
    road_surface_hebrew = Column(Text())
    road_object = Column(Integer())
    road_object_hebrew = Column(Text())
    object_distance = Column(Integer())
    object_distance_hebrew = Column(Text())
    didnt_cross = Column(Integer())
    didnt_cross_hebrew = Column(Text())
    cross_mode = Column(Integer())
    cross_mode_hebrew = Column(Text())
    cross_location = Column(Integer())
    cross_location_hebrew = Column(Text())
    cross_direction = Column(Integer())
    cross_direction_hebrew = Column(Text())
    road1 = Column(Integer(), index=True)
    road2 = Column(Integer(), index=True)
    km = Column(Float())
    km_raw = Column(Text())
    km_accurate = Column(Boolean())
    yishuv_symbol = Column(Integer(), index=True)
    yishuv_name = Column(Text(), index=True)
    geo_area = Column(Integer())
    geo_area_hebrew = Column(Text())
    day_night = Column(Integer())
    day_night_hebrew = Column(Text())
    day_in_week = Column(Integer())
    day_in_week_hebrew = Column(Text())
    traffic_light = Column(Integer())
    traffic_light_hebrew = Column(Text())
    region = Column(Integer())
    region_hebrew = Column(Text())
    district = Column(Integer())
    district_hebrew = Column(Text())
    natural_area = Column(Integer())
    natural_area_hebrew = Column(Text())
    municipal_status = Column(Integer())
    municipal_status_hebrew = Column(Text())
    yishuv_shape = Column(Integer())
    yishuv_shape_hebrew = Column(Text())
    street1 = Column(Integer())
    street1_hebrew = Column(Text(), index=True)
    street2 = Column(Integer())
    street2_hebrew = Column(Text(), index=True)
    non_urban_intersection_hebrew = Column(Text(), index=True)
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    accident_day = Column(Integer())
    accident_hour_raw = Column(Integer())
    accident_hour_raw_hebrew = Column(Text())
    accident_hour = Column(Integer())
    accident_minute = Column(Integer())
    geom = Column(Geometry('POINT'), index=True)
    latitude = Column(Float())
    longitude = Column(Float())
    x = Column(Float())
    y = Column(Float())
    road_segment_id = Column(Integer(), index=True)
    road_segment_name = Column(Text(), index=True)
    road_segment_number = Column(Integer())
    road_segment_from_km = Column(Text())
    road_segment_to_km = Column(Text())
    road_segment_length_km = Column(Float())

class InvolvedView(CBSBase):
    __tablename__ = "involved_hebrew"
    accident_id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    file_type_police = Column(Integer())
    involved_type = Column(Integer())
    involved_type_hebrew = Column(Text())
    license_acquiring_date = Column(Integer())
    age_group = Column(Integer())
    age_group_hebrew = Column(Text())
    sex = Column(Integer())
    sex_hebrew = Column(Text())
    vehicle_type = Column(Integer())
    vehicle_type_hebrew = Column(Text())
    safety_measures = Column(Integer())
    safety_measures_hebrew = Column(Text())
    involve_yishuv_symbol = Column(Integer())
    involve_yishuv_name = Column(Text())
    injury_severity = Column(Integer())
    injury_severity_hebrew = Column(Text())
    injured_type = Column(Integer())
    injured_type_hebrew = Column(Text())
    injured_position = Column(Integer())
    injured_position_hebrew = Column(Text())
    population_type = Column(Integer())
    population_type_hebrew = Column(Text())
    home_region = Column(Integer())
    home_region_hebrew = Column(Text())
    home_district = Column(Integer())
    home_district_hebrew = Column(Text())
    home_natural_area = Column(Integer())
    home_natural_area_hebrew = Column(Text())
    home_municipal_status = Column(Integer())
    home_municipal_status_hebrew = Column(Text())
    home_yishuv_shape = Column(Integer())
    home_yishuv_shape_hebrew = Column(Text())
    hospital_time = Column(Integer())
    hospital_time_hebrew = Column(Text())
    medical_type = Column(Integer())
    medical_type_hebrew = Column(Text())
    release_dest = Column(Integer())
    release_dest_hebrew = Column(Text())
    safety_measures_use = Column(Integer())
    safety_measures_use_hebrew = Column(Text())
    late_deceased = Column(Integer())
    late_deceased_hebrew = Column(Text())
    car_id = Column(Integer())
    involve_id = Column(Integer(), primary_key=True)
    accident_year = Column(Integer())
    accident_month = Column(Integer())


class InvolvedMarkerView(CBSBase):
    __tablename__ = "involved_markers_hebrew"
    accident_id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    file_type_police = Column(Integer())
    involved_type = Column(Integer())
    involved_type_hebrew = Column(Text())
    license_acquiring_date = Column(Integer())
    age_group = Column(Integer())
    age_group_hebrew = Column(Text())
    sex = Column(Integer())
    sex_hebrew = Column(Text())
    involve_vehicle_type = Column(Integer())
    involve_vehicle_type_hebrew = Column(Text())
    safety_measures = Column(Integer())
    safety_measures_hebrew = Column(Text())
    involve_yishuv_symbol = Column(Integer())
    involve_yishuv_name = Column(Text())
    injury_severity = Column(Integer())
    injury_severity_hebrew = Column(Text())
    injured_type = Column(Integer())
    injured_type_hebrew = Column(Text())
    injured_position = Column(Integer())
    injured_position_hebrew = Column(Text())
    population_type = Column(Integer())
    population_type_hebrew = Column(Text())
    involve_home_region = Column(Integer())
    involve_home_region_hebrew = Column(Text())
    involve_home_district = Column(Integer())
    involve_home_district_hebrew = Column(Text())
    involve_home_natural_area = Column(Integer())
    involve_home_natural_area_hebrew = Column(Text())
    involve_home_municipal_status = Column(Integer())
    involve_home_municipal_status_hebrew = Column(Text())
    involve_home_yishuv_shape = Column(Integer())
    involve_home_yishuv_shape_hebrew = Column(Text())
    hospital_time = Column(Integer())
    hospital_time_hebrew = Column(Text())
    medical_type = Column(Integer())
    medical_type_hebrew = Column(Text())
    release_dest = Column(Integer())
    release_dest_hebrew = Column(Text())
    safety_measures_use = Column(Integer())
    safety_measures_use_hebrew = Column(Text())
    late_deceased = Column(Integer())
    late_deceased_hebrew = Column(Text())
    car_id = Column(Integer())
    involve_id = Column(Integer(), primary_key=True)
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    accident_timestamp = Column(DateTime, default=None)
    provider_code_hebrew = Column(Text())
    accident_type = Column(Integer(), index=True)
    accident_type_hebrew = Column(Text(), index=True)
    accident_severity = Column(Integer(), index=True)
    accident_severity_hebrew = Column(Text(), index=True)
    location_accuracy = Column(Integer())
    location_accuracy_hebrew = Column(Text())
    road_type = Column(Integer())
    road_type_hebrew = Column(Text())
    road_shape = Column(Integer())
    road_shape_hebrew = Column(Text())
    day_type = Column(Integer())
    day_type_hebrew = Column(Text())
    police_unit = Column(Integer())
    police_unit_hebrew = Column(Text())
    one_lane = Column(Integer())
    one_lane_hebrew = Column(Text())
    multi_lane = Column(Integer())
    multi_lane_hebrew = Column(Text())
    speed_limit = Column(Integer())
    speed_limit_hebrew = Column(Text())
    road_intactness = Column(Integer())
    road_intactness_hebrew = Column(Text())
    road_width = Column(Integer())
    road_width_hebrew = Column(Text())
    road_sign = Column(Integer())
    road_sign_hebrew = Column(Text())
    road_light = Column(Integer())
    road_light_hebrew = Column(Text())
    road_control = Column(Integer())
    road_control_hebrew = Column(Text())
    weather = Column(Integer())
    weather_hebrew = Column(Text())
    road_surface = Column(Integer())
    road_surface_hebrew = Column(Text())
    road_object = Column(Integer())
    road_object_hebrew = Column(Text())
    object_distance = Column(Integer())
    object_distance_hebrew = Column(Text())
    didnt_cross = Column(Integer())
    didnt_cross_hebrew = Column(Text())
    cross_mode = Column(Integer())
    cross_mode_hebrew = Column(Text())
    cross_location = Column(Integer())
    cross_location_hebrew = Column(Text())
    cross_direction = Column(Integer())
    cross_direction_hebrew = Column(Text())
    road1 = Column(Integer(), index=True)
    road2 = Column(Integer(), index=True)
    km = Column(Float())
    km_raw = Column(Text())
    km_accurate = Column(Boolean())
    accident_yishuv_symbol = Column(Integer(), index=True)
    accident_yishuv_name = Column(Text(), index=True)
    geo_area = Column(Integer())
    geo_area_hebrew = Column(Text())
    day_night = Column(Integer())
    day_night_hebrew = Column(Text())
    day_in_week = Column(Integer())
    day_in_week_hebrew = Column(Text())
    traffic_light = Column(Integer())
    traffic_light_hebrew = Column(Text())
    accident_region = Column(Integer())
    accident_region_hebrew = Column(Text())
    accident_district = Column(Integer())
    accident_district_hebrew = Column(Text())
    accident_natural_area = Column(Integer())
    accident_natural_area_hebrew = Column(Text())
    accident_municipal_status = Column(Integer())
    accident_municipal_status_hebrew = Column(Text())
    accident_yishuv_shape = Column(Integer())
    accident_yishuv_shape_hebrew = Column(Text())
    street1 = Column(Integer())
    street1_hebrew = Column(Text(), index=True)
    street2 = Column(Integer())
    street2_hebrew = Column(Text(), index=True)
    non_urban_intersection_hebrew = Column(Text(), index=True)
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    accident_day = Column(Integer())
    accident_hour_raw = Column(Integer())
    accident_hour_raw_hebrew = Column(Text())
    accident_hour = Column(Integer())
    accident_minute = Column(Integer())
    geom = Column(Geometry('POINT'), index=True)
    latitude = Column(Float())
    longitude = Column(Float())
    x = Column(Float())
    y = Column(Float())
    road_segment_id = Column(Integer(), index=True)
    road_segment_name = Column(Text(), index=True)
    road_segment_number = Column(Integer(), index=True)
    road_segment_from_km = Column(Text())
    road_segment_to_km = Column(Text())
    road_segment_length_km = Column(Float())
    engine_volume = Column(Integer())
    engine_volume_hebrew = Column(Text())
    manufacturing_year = Column(Integer())
    driving_directions = Column(Integer())
    driving_directions_hebrew = Column(Text())
    vehicle_status = Column(Integer())
    vehicle_status_hebrew = Column(Text())
    vehicle_attribution = Column(Integer())
    vehicle_attribution_hebrew = Column(Text())
    seats = Column(Integer())
    total_weight = Column(Integer())
    total_weight_hebrew = Column(Text())
    vehicle_vehicle_type = Column(Integer())
    vehicle_vehicle_type_hebrew = Column(Text())
    vehicle_damage = Column(Integer())
    vehicle_damage_hebrew = Column(Text())


class VehiclesView(CBSBase):
    __tablename__ = "vehicles_hebrew"
    id = Column(BigInteger(), primary_key=True)
    accident_id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    engine_volume = Column(Integer())
    engine_volume_hebrew = Column(Text())
    manufacturing_year = Column(Integer())
    driving_directions = Column(Integer())
    driving_directions_hebrew = Column(Text())
    vehicle_status = Column(Integer())
    vehicle_status_hebrew = Column(Text())
    vehicle_attribution = Column(Integer())
    vehicle_attribution_hebrew = Column(Text())
    seats = Column(Integer())
    total_weight = Column(Integer())
    total_weight_hebrew = Column(Text())
    vehicle_type = Column(Integer())
    vehicle_type_hebrew = Column(Text())
    vehicle_damage = Column(Integer())
    vehicle_damage_hebrew = Column(Text())
    accident_year = Column(Integer(), primary_key=True)
    accident_month = Column(Integer())


class VehiclesMarkersView(CBSBase):
    __tablename__ = "vehicles_markers_hebrew"
    provider_code_hebrew = Column(Text())
    accident_timestamp = Column(DateTime, default=None)
    accident_type = Column(Integer(), index=True)
    accident_type_hebrew = Column(Text(), index=True)
    accident_severity = Column(Integer(), index=True)
    accident_severity_hebrew = Column(Text(), index=True)
    location_accuracy = Column(Integer(), index=True)
    location_accuracy_hebrew = Column(Text(), index=True)
    road_type = Column(Integer())
    road_type_hebrew = Column(Text())
    road_shape = Column(Integer())
    road_shape_hebrew = Column(Text())
    day_type = Column(Integer())
    day_type_hebrew = Column(Text())
    police_unit = Column(Integer())
    police_unit_hebrew = Column(Text())
    one_lane = Column(Integer())
    one_lane_hebrew = Column(Text())
    multi_lane = Column(Integer())
    multi_lane_hebrew = Column(Text())
    speed_limit = Column(Integer())
    speed_limit_hebrew = Column(Text())
    road_intactness = Column(Integer())
    road_intactness_hebrew = Column(Text())
    road_width = Column(Integer())
    road_width_hebrew = Column(Text())
    road_sign = Column(Integer())
    road_sign_hebrew = Column(Text())
    road_light = Column(Integer())
    road_light_hebrew = Column(Text())
    road_control = Column(Integer())
    road_control_hebrew = Column(Text())
    weather = Column(Integer())
    weather_hebrew = Column(Text())
    road_surface = Column(Integer())
    road_surface_hebrew = Column(Text())
    road_object = Column(Integer())
    road_object_hebrew = Column(Text())
    object_distance = Column(Integer())
    object_distance_hebrew = Column(Text())
    didnt_cross = Column(Integer())
    didnt_cross_hebrew = Column(Text())
    cross_mode = Column(Integer())
    cross_mode_hebrew = Column(Text())
    cross_location = Column(Integer())
    cross_location_hebrew = Column(Text())
    cross_direction = Column(Integer())
    cross_direction_hebrew = Column(Text())
    road1 = Column(Integer(), index=True)
    road2 = Column(Integer(), index=True)
    km = Column(Float())
    km_raw = Column(Text())
    km_accurate = Column(Boolean())
    road_segment_id = Column(Integer(), index=True)
    road_segment_name = Column(Text(), index=True)
    road_segment_number = Column(Integer())
    road_segment_from_km = Column(Text())
    road_segment_to_km = Column(Text())
    road_segment_length_km = Column(Float())
    accident_yishuv_symbol = Column(Integer(), index=True)
    accident_yishuv_name = Column(Text(), index=True)
    geo_area = Column(Integer())
    geo_area_hebrew = Column(Text())
    day_night = Column(Integer())
    day_night_hebrew = Column(Text())
    day_in_week = Column(Integer())
    day_in_week_hebrew = Column(Text())
    traffic_light = Column(Integer())
    traffic_light_hebrew = Column(Text())
    accident_region = Column(Integer())
    accident_region_hebrew = Column(Text())
    accident_district = Column(Integer())
    accident_district_hebrew = Column(Text())
    accident_natural_area = Column(Integer())
    accident_natural_area_hebrew = Column(Text())
    accident_municipal_status = Column(Integer())
    accident_municipal_status_hebrew = Column(Text())
    accident_yishuv_shape = Column(Integer())
    accident_yishuv_shape_hebrew = Column(Text())
    street1 = Column(Integer())
    street1_hebrew = Column(Text())
    street2 = Column(Integer())
    street2_hebrew = Column(Text())
    non_urban_intersection_hebrew = Column(Text())
    accident_year = Column(Integer(), primary_key=True)
    accident_month = Column(Integer())
    accident_day = Column(Integer())
    accident_hour_raw = Column(Integer())
    accident_hour_raw_hebrew = Column(Text())
    accident_hour = Column(Integer())
    accident_minute = Column(Integer())
    geom = Column(Geometry('POINT'), index=True)
    latitude = Column(Float())
    longitude = Column(Float())
    x = Column(Float())
    y = Column(Float())
    id = Column(BigInteger())
    accident_id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    file_type_police = Column(Integer())
    engine_volume = Column(Integer())
    engine_volume_hebrew = Column(Text())
    manufacturing_year = Column(Integer())
    driving_directions = Column(Integer())
    driving_directions_hebrew = Column(Text())
    vehicle_status = Column(Integer())
    vehicle_status_hebrew = Column(Text())
    vehicle_attribution = Column(Integer())
    vehicle_attribution_hebrew = Column(Text())
    seats = Column(Integer())
    total_weight = Column(Integer())
    total_weight_hebrew = Column(Text())
    vehicle_type = Column(Integer())
    vehicle_type_hebrew = Column(Text())
    vehicle_damage = Column(Integer())
    vehicle_damage_hebrew = Column(Text())
    car_id = Column(Integer(), primary_key=True)
