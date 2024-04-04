patterns = [
    {
        "pattern": {
            "isPointer": True,
            "isArray": "dynamic"
        },
        "lines": [
            "<type> *<name>;",
            "unsigned int <name>_length;",
        ]
    },
    {
        "pattern": {
            "isPointer": False,
            "isArray": "dynamic"
        },
        "lines": [
            "<type> *<name>;",
            "unsigned int <name>_length;",
        ]
    },
    {
        "pattern": {
            "isPointer": True,
            "isArray": "static"
        },
        "lines": ["<type> *<name>[<max_length>];"]
    },
    {
        "pattern": {
            "isPointer": False,
            "isArray": "static"
        },
        "lines": ["<type> <name>[<max_length>];"]
    },
    {
        "pattern": {
            "isPointer": True
        },
        "lines": ["<type> *<name>;"]
    },
    {
        "pattern": {},
        "lines": ["<type> <name>;"]
    },
]

size_to_field = {
    "char": 1,
    "unsinged char": 1,
    "short": 2,
    "unsigned short": 2,
    "int": 4,
    "unsigned": 4,
    "unsigned int": 4,
    "long": 8,
    "unsigned long": 8,
    "long long": 8,
    "unsigned long long": 16,
    "float": 4,
    "double": 8,
    "long double": 16,
    "vec2": 8,
    "vec3": 12,
    "vec4": 16,
    "mat2": 16,
    "mat3": 36,
    "mat4": 64,
}

serialize_patterns = [
    {
        "pattern": {
            "isStruct": True
        },
        "serialize_templates": [
            "buffer = <type>_serialize(&value-><name>, buffer);",
        ],
        "deserialize_templates": [
            "buffer = <type>_deserialize(&value-><name>, buffer);",
        ]
    },
    {
        "pattern": {},
        "serialize_templates": [
            "memcpy(&value-><name>, buffer, <size>);",
            "buffer += <size>;"
        ],
        "deserialize_templates": [
            "memcpy(buffer, &value-><name>, <size>);",
            "buffer += <size>;"
        ],
    }
]

comp_template_h = """
#ifndef <NAME>_H
#define <NAME>_H

<includes>

typedef struct <name> {
<fields>
} <name>;

void* <name>_serialize(void *buffer, <name> *value);
void* <name>_deserialize(void *buffer, <name> *value);


#endif
"""

comp_serialize_c = """
#include <comps/<name>.h>
#include <string.h>

void* <name>_serialize(void *buffer, <name> *value)
{
<serialize_code>
    return buffer;
}

void* <name>_deserialize(void *buffer, <name> *value)
{
<deserialize_code>
    return buffer;
}
"""
