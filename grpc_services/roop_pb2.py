# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: roop.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'roop.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nroop.proto\x12\x04roop\"p\n\x0cRoopInputMsg\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x11\n\tprocessor\x18\x03 \x01(\t\x12\x1f\n\x17reference_face_position\x18\x04 \x01(\x05\x12\x0c\n\x04\x64\x65st\x18\x05 \x01(\t\",\n\x0cRoopResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x0c\n\x04\x64\x65st\x18\x02 \x01(\t2y\n\x04Roop\x12\x34\n\x08\x66\x61\x63\x65Swap\x12\x12.roop.RoopInputMsg\x1a\x12.roop.RoopResponse\"\x00\x12;\n\x0f\x66\x61\x63\x65\x45nhancement\x12\x12.roop.RoopInputMsg\x1a\x12.roop.RoopResponse\"\x00\x42`\n\x18\x63om.arkai.inference.roopB\x0bRoopServiceP\x01Z.gitlab.in.promiseland.live/ark/ark-api/ai_grpc\xa2\x02\x04ROOPb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'roop_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\030com.arkai.inference.roopB\013RoopServiceP\001Z.gitlab.in.promiseland.live/ark/ark-api/ai_grpc\242\002\004ROOP'
  _globals['_ROOPINPUTMSG']._serialized_start=20
  _globals['_ROOPINPUTMSG']._serialized_end=132
  _globals['_ROOPRESPONSE']._serialized_start=134
  _globals['_ROOPRESPONSE']._serialized_end=178
  _globals['_ROOP']._serialized_start=180
  _globals['_ROOP']._serialized_end=301
# @@protoc_insertion_point(module_scope)
