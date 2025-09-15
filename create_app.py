#!/usr/bin/env python3
"""
postman_to_pojo.py

Generate Java POJO classes (with package directories) from a Postman Collection JSON
that contains JSON request bodies (raw). The script follows Java naming standards and
creates separate .java files for nested objects. Each class contains:
 - package declaration
 - imports (List, Objects, JsonProperty)
 - private fields
 - no-arg constructor
 - all-args constructor
 - getters and setters
 - toString(), equals(), hashCode()

Enhancements:
 - For each service/API (request item), create a separate folder named after the request.
 - Nested classes are also created in the same service folder.
 - Field names follow camelCase properly (e.g., "initiatorInformation").

Usage:
    python postman_to_pojo.py COLLECTION.json com.example.models ./output_dir
"""

import json
import os
import re
import sys
from collections import OrderedDict


JAVA_PRIMITIVE_MAP = {
    'string': 'String',
    'integer': 'Integer',
    'number': 'Double',
    'boolean': 'Boolean',
    'null': 'Object'
}


def to_pascal_case(s: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s)
    parts = s.split()
    return ''.join(p.capitalize() for p in parts) or 'AutoGen'


def to_camel_case(s: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s)
    parts = s.split()
    if not parts:
        return "field"
    first = parts[0].lower()
    rest = ''.join(p.capitalize() for p in parts[1:])
    return first + rest


def safe_class_name(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]", "_", name)
    name = re.sub(r"^(\d+)", r"N\1", name)
    return to_pascal_case(name)


class JavaClass:
    def __init__(self, name, package, service_folder):
        self.name = name
        self.package = package
        self.service_folder = service_folder
        self.fields = OrderedDict()  # field_name -> (type_str, json_name)
        self.nested = OrderedDict()  # nested_class_name -> JavaClass

    def add_field(self, field_name, java_type, json_name=None):
        if json_name is None:
            json_name = field_name
        self.fields[field_name] = (java_type, json_name)

    def add_nested(self, nested_class):
        self.nested[nested_class.name] = nested_class

    def uses_list(self):
        return any('List<' in t for t, _ in self.fields.values())

    def uses_objects(self):
        return any(t == 'Object' or 'Map<' in t for t, _ in self.fields.values())

    def render(self):
        lines = []
        if self.package:
            lines.append(f"package {self.package}.{self.service_folder};\n")

        imports = set()
        if self.uses_list():
            imports.add('java.util.List')
            imports.add('java.util.ArrayList')
        if self.uses_objects():
            imports.add('java.util.Map')
            imports.add('java.util.HashMap')
        imports.add('java.util.Objects')
        imports.add('com.fasterxml.jackson.annotation.JsonProperty')

        for imp in sorted(imports):
            lines.append(f"import {imp};")
        lines.append("")

        lines.append(f"public class {self.name} {{")

        for fname, (ftype, json_name) in self.fields.items():
            if json_name != fname:
                lines.append(f"    @JsonProperty(\"{json_name}\")")
            lines.append(f"    private {ftype} {fname};")
            lines.append("")

        lines.append(f"    public {self.name}() {{ }}\n")

        if self.fields:
            params = ', '.join(f"{t} {n}" for n, (t, _) in self.fields.items())
            lines.append(f"    public {self.name}({params}) {{")
            for n in self.fields.keys():
                lines.append(f"        this.{n} = {n};")
            lines.append("    }\n")

        for fname, (ftype, _) in self.fields.items():
            cap = fname[0].upper() + fname[1:]
            lines.append(f"    public {ftype} get{cap}() {{")
            lines.append(f"        return this.{fname};")
            lines.append("    }")
            lines.append("")
            lines.append(f"    public void set{cap}({ftype} {fname}) {{")
            lines.append(f"        this.{fname} = {fname};")
            lines.append("    }\n")

        fields_str = ' + ", " + '.join([f'"{n}=" + {n}' for n in self.fields.keys()]) if self.fields else '""'
        lines.append("    @Override")
        lines.append("    public String toString() {")
        lines.append(f"        return \"{self.name}{{\" + {fields_str} + \"}}\";")
        lines.append("    }\n")

        lines.append("    @Override")
        lines.append("    public boolean equals(Object o) {")
        lines.append("        if (this == o) return true;")
        lines.append("        if (o == null || getClass() != o.getClass()) return false;")
        lines.append(f"        {self.name} that = ({self.name}) o;")
        if self.fields:
            comparisons = ' && '.join([f"Objects.equals({n}, that.{n})" for n in self.fields.keys()])
            lines.append(f"        return {comparisons};")
        else:
            lines.append("        return true;")
        lines.append("    }\n")

        if self.fields:
            args = ', '.join(self.fields.keys())
            lines.append("    @Override")
            lines.append("    public int hashCode() {")
            lines.append(f"        return Objects.hash({args});")
            lines.append("    }")

        lines.append("}")

        return '\n'.join(lines)


def detect_type(value, class_prefix, package, service_folder, classes):
    if value is None:
        return 'Object'
    if isinstance(value, bool):
        return JAVA_PRIMITIVE_MAP['boolean']
    if isinstance(value, int):
        return JAVA_PRIMITIVE_MAP['integer']
    if isinstance(value, float):
        return JAVA_PRIMITIVE_MAP['number']
    if isinstance(value, str):
        return JAVA_PRIMITIVE_MAP['string']
    if isinstance(value, dict):
        class_name = safe_class_name(class_prefix)
        key = f"{service_folder}.{class_name}"
        if key in classes:
            jc = classes[key]
        else:
            jc = JavaClass(class_name, package, service_folder)
            classes[key] = jc
            for k, v in value.items():
                field_name = to_camel_case(k)
                nested_type = detect_type(v, class_prefix + '_' + k, package, service_folder, classes)
                jc.add_field(field_name, nested_type, json_name=k)
        return class_name
    if isinstance(value, list):
        if not value:
            elem_type = 'Object'
        else:
            elem_types = set()
            for el in value:
                t = detect_type(el, class_prefix + '_Item', package, service_folder, classes)
                elem_types.add(t)
            elem_type = elem_types.pop() if len(elem_types) == 1 else 'Object'
        return f"List<{elem_type}>"
    return 'Object'


def process_json_root(root_obj, root_name, package, service_folder, classes):
    class_name = safe_class_name(root_name)
    key = f"{service_folder}.{class_name}"
    jc = JavaClass(class_name, package, service_folder)
    classes[key] = jc
    if isinstance(root_obj, dict):
        for k, v in root_obj.items():
            field_name = to_camel_case(k)
            java_type = detect_type(v, class_name + '_' + k, package, service_folder, classes)
            jc.add_field(field_name, java_type, json_name=k)
    else:
        java_type = detect_type(root_obj, class_name + '_value', package, service_folder, classes)
        jc.add_field('value', java_type, json_name='value')


def find_raw_json_bodies(postman_coll):
    items = postman_coll.get('item', [])
    for item in items:
        if 'request' in item:
            req = item['request']
            name = item.get('name') or 'Request'
            body = req.get('body')
            if body and body.get('mode') == 'raw':
                raw = body.get('raw')
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = None
                if parsed is not None:
                    yield name, parsed
        if 'item' in item:
            for subname, subjson in find_raw_json_bodies({'item': item.get('item', [])}):
                yield subname, subjson


def write_classes(classes, outdir, base_package):
    for key, jc in classes.items():
        package_path = base_package.replace('.', os.sep)
        dest_dir = os.path.join(outdir, package_path, jc.service_folder)
        os.makedirs(dest_dir, exist_ok=True)
        file_path = os.path.join(dest_dir, f"{jc.name}.java")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(jc.render())
        print(f"Wrote {file_path}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python postman_to_pojo.py COLLECTION.json com.example.models ./output_dir")
        sys.exit(1)
    coll_path = sys.argv[1]
    base_package = sys.argv[2]
    outdir = sys.argv[3]

    with open(coll_path, 'r', encoding='utf-8') as f:
        coll = json.load(f)

    classes = OrderedDict()
    for req_name, json_obj in find_raw_json_bodies(coll):
        service_folder = safe_class_name(req_name)
        process_json_root(json_obj, req_name, base_package, service_folder, classes)

    if not classes:
        print("No raw JSON bodies found in collection. Exiting.")
        sys.exit(1)

    write_classes(classes, outdir, base_package)
    print("Done. Classes organized per service/API folder, with nested classes also inside.")


if __name__ == '__main__':
    main()
