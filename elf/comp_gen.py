from comp_templates import patterns, serialize_patterns, comp_template_h, comp_serialize_c, size_to_field
from json import loads
from os.path import basename, splitext, join
from os import walk


def matches(data, pattern):
    for key in pattern:
        if key not in data:
            if pattern[key] == False:
                continue
            return False
        if data[key] != pattern[key]:
            return False
    return True


def apply_template(field, field_name, template):
    template = template.replace(f"<name>", field_name)
    if "type" in field and (field["type"] in size_to_field):
        template = template.replace(
            "<size>", str(size_to_field[field["type"]])
        )
    for k in field:
        template = template.replace(f"<{k}>", str(field[k]))
    return template


def generate_field(field, field_name):
    result = []
    for pattern in patterns:
        if matches(field, pattern["pattern"]):
            templates = pattern["lines"]
            for template in templates:
                result.append(apply_template(field, field_name, template))
            return result
    return result


def generate_fields(fields):
    result = []
    for field_name in fields:
        field = fields[field_name]
        result += generate_field(field, field_name)
    return result


def generate_serialize(field, field_name):
    serializes = []
    deserializes = []
    for pattern in serialize_patterns:
        if matches(field, pattern["pattern"]):
            serialize_templates = pattern["serialize_templates"]
            deserialize_templates = pattern["deserialize_templates"]
            for template in serialize_templates:
                serializes.append(apply_template(field, field_name, template))
            for template in deserialize_templates:
                deserializes.append(apply_template(
                    field, field_name, template))
            return {
                "serializes": serializes,
                "deserializes": deserializes
            }
    return {
        "serializes": serializes,
        "deserializes": deserializes
    }


def generate_serializes(fields):
    serializes = []
    deserializes = []
    for field_name in fields:
        field = fields[field_name]
        result = generate_serialize(field, field_name)
        serializes += result["serializes"]
        deserializes += result["deserializes"]
    return {
        "serializes": serializes,
        "deserializes": deserializes,
    }


def format_code(fields):
    return "\n".join([f"    {field}" for field in fields])


def gen_code(json, name):
    fields = generate_fields(json["fields"])
    serializes = generate_serializes(json["fields"])
    h_code = comp_template_h.replace("<fields>", format_code(fields))
    h_code = h_code.replace("<name>", name)
    h_code = h_code.replace("<NAME>", name.upper())
    h_code = h_code.replace(
        "<includes>",
        "\n".join(json["includes"])
    )
    c_code = comp_serialize_c.replace(
        "<serialize_code>",
        format_code(serializes["serializes"])
    )
    c_code = c_code.replace(
        "<deserialize_code>",
        format_code(serializes["deserializes"])
    )
    c_code = c_code.replace(
        "<includes>",
        "\n".join(json["includes"])
    )
    c_code = c_code.replace("<name>", name)
    return {
        "c_code": c_code,
        "h_code": h_code
    }


def run_gen_code(json_path, c_path, h_path):
    filename = splitext(basename(json_path))[0]
    with open(json_path) as f:
        json = loads(f.read())
        code = gen_code(json, filename)
        with open(c_path, "w") as c:
            c.write(code["c_code"])
        with open(h_path, "w") as h:
            h.write(code["h_code"])


for dirpath, dirnames, filenames in walk("C:\\Projects\\elf-engine\\engine-ecs\\res\\comp"):
    for file in filenames:
        filename = splitext(file)[0]
        run_gen_code(
            join(dirpath, file),
            join(dirpath, "../", "../", "src", "comps", f"{filename}.c"),
            join(dirpath, "../", "../", "include", "comps", f"{filename}.h")
        )
