# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='messages',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x0emessages.proto\x12\x08messages\"\x9a\x01\n\rCommonMessage\x12+\n\x0cmessage_type\x18\x01 \x02(\x0e\x32\x15.messages.MessageType\x12\x1e\n\x04join\x18\x02 \x01(\x0b\x32\x0e.messages.JoinH\x00\x12,\n\x0btransaction\x18\x03 \x01(\x0b\x32\x15.messages.TransactionH\x00\x42\x0e\n\x0cmessage_body\"\r\n\x0bTransaction\"\x8a\x01\n\x04Join\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x02(\t\x12\x0c\n\x04port\x18\x02 \x02(\x05\x12\x0e\n\x06pubkey\x18\x03 \x02(\t\x12\x10\n\x08nickname\x18\x04 \x01(\t\x12&\n\tjoin_type\x18\x05 \x02(\x0e\x32\x13.messages.Join.Type\"\x19\n\x04Type\x12\x08\n\x04INIT\x10\x00\x12\x07\n\x03\x41\x43K\x10\x01*(\n\x0bMessageType\x12\x08\n\x04JOIN\x10\x00\x12\x0f\n\x0bTRANSACTION\x10\x01')
)

_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='messages.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='JOIN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSACTION', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=341,
  serialized_end=381,
)
_sym_db.RegisterEnumDescriptor(_MESSAGETYPE)

MessageType = enum_type_wrapper.EnumTypeWrapper(_MESSAGETYPE)
JOIN = 0
TRANSACTION = 1


_JOIN_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='messages.Join.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INIT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ACK', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=314,
  serialized_end=339,
)
_sym_db.RegisterEnumDescriptor(_JOIN_TYPE)


_COMMONMESSAGE = _descriptor.Descriptor(
  name='CommonMessage',
  full_name='messages.CommonMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_type', full_name='messages.CommonMessage.message_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='join', full_name='messages.CommonMessage.join', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='messages.CommonMessage.transaction', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='message_body', full_name='messages.CommonMessage.message_body',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=29,
  serialized_end=183,
)


_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='messages.Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=185,
  serialized_end=198,
)


_JOIN = _descriptor.Descriptor(
  name='Join',
  full_name='messages.Join',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='messages.Join.address', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='messages.Join.port', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pubkey', full_name='messages.Join.pubkey', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='messages.Join.nickname', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='join_type', full_name='messages.Join.join_type', index=4,
      number=5, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOIN_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=201,
  serialized_end=339,
)

_COMMONMESSAGE.fields_by_name['message_type'].enum_type = _MESSAGETYPE
_COMMONMESSAGE.fields_by_name['join'].message_type = _JOIN
_COMMONMESSAGE.fields_by_name['transaction'].message_type = _TRANSACTION
_COMMONMESSAGE.oneofs_by_name['message_body'].fields.append(
  _COMMONMESSAGE.fields_by_name['join'])
_COMMONMESSAGE.fields_by_name['join'].containing_oneof = _COMMONMESSAGE.oneofs_by_name['message_body']
_COMMONMESSAGE.oneofs_by_name['message_body'].fields.append(
  _COMMONMESSAGE.fields_by_name['transaction'])
_COMMONMESSAGE.fields_by_name['transaction'].containing_oneof = _COMMONMESSAGE.oneofs_by_name['message_body']
_JOIN.fields_by_name['join_type'].enum_type = _JOIN_TYPE
_JOIN_TYPE.containing_type = _JOIN
DESCRIPTOR.message_types_by_name['CommonMessage'] = _COMMONMESSAGE
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.message_types_by_name['Join'] = _JOIN
DESCRIPTOR.enum_types_by_name['MessageType'] = _MESSAGETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CommonMessage = _reflection.GeneratedProtocolMessageType('CommonMessage', (_message.Message,), dict(
  DESCRIPTOR = _COMMONMESSAGE,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:messages.CommonMessage)
  ))
_sym_db.RegisterMessage(CommonMessage)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), dict(
  DESCRIPTOR = _TRANSACTION,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:messages.Transaction)
  ))
_sym_db.RegisterMessage(Transaction)

Join = _reflection.GeneratedProtocolMessageType('Join', (_message.Message,), dict(
  DESCRIPTOR = _JOIN,
  __module__ = 'messages_pb2'
  # @@protoc_insertion_point(class_scope:messages.Join)
  ))
_sym_db.RegisterMessage(Join)


# @@protoc_insertion_point(module_scope)