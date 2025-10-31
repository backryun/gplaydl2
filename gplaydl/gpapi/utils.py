#!/usr/bin/python

import struct

def readInt(data, offset):
    return struct.unpack('>I', data[offset:offset + 4])[0]

def toBigInt(data):
    return int.from_bytes(data, byteorder='big')

def hasPrefetch(message):
    return len(message.preFetch) > 0

def hasDoc(entry):
    return entry.doc.docid != ""

def hasTosContent(tocResponse):
    return tocResponse.tosContent != ""

def hasTosToken(tocResponse):
    return tocResponse.tosToken != ""

def hasCookie(tocResponse):
    return tocResponse.cookie != ""

def parseProtobufObj(obj):
    """Parse a protobuf object into a dictionary"""
    result = {}
    for field in obj.DESCRIPTOR.fields:
        value = getattr(obj, field.name)
        if field.type == field.TYPE_MESSAGE:
            if field.label == field.LABEL_REPEATED:
                result[field.name] = [parseProtobufObj(item) for item in value]
            else:
                result[field.name] = parseProtobufObj(value)
        elif field.type == field.TYPE_ENUM:
            result[field.name] = field.enum_type.values_by_number[value].name
        else:
            result[field.name] = value
    return result