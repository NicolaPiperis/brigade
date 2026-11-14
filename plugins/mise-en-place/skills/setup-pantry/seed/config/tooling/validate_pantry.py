#!/usr/bin/env python3
"""Validator of the pantry.

Checks, for every file in core/:

  1. body sections  -> against the templates in config/templates/
  2. frontmatter    -> against the schemas in config/schemas/
  3. names          -> against the vocabularies in config/vocabulary/
  4. placement      -> entries in the folder of their type, tickets where their state says

The templates are the contract: every `## ` heading in a template is an allowed section,
and it is required when its guide comment starts with "required". A heading in braces
(`## {topic}`) is a placeholder: that document has no section contract.

Usage:
    python config/tooling/validate_pantry.py             # the whole pantry
    python config/tooling/validate_pantry.py <file> ...  # single files

Exits 0 when everything passes, 1 otherwise. Needs PyYAML.
"""
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TECHNICAL_LEVEL_DOCS = ("map.md", "rules.md", "structure.md")
DOCS_FILES = ("overview.md", "topic.md")
ENTRY_FOLDERS = {"gotchas": "gotcha", "decisions": "decision", "patterns": "pattern"}
TICKET_STATES = ("pending", "served")


class StringDateLoader(yaml.SafeLoader):
    """Keeps `created: 2026-06-08` a string, so it is checked against the ISO pattern."""


StringDateLoader.add_constructor("tag:yaml.org,2002:timestamp", StringDateLoader.construct_yaml_str)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_yaml(path):
    try:
        return yaml.load(read(path), Loader=StringDateLoader) or {}
    except yaml.YAMLError as e:
        return {"__error__": str(e).split("\n")[0]}


def frontmatter(text):
    """The YAML block at the top: None when missing, {'__error__': ...} when malformed."""
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    try:
        fields = yaml.load(m.group(1), Loader=StringDateLoader)
    except yaml.YAMLError as e:
        return {"__error__": str(e).split("\n")[0]}
    return fields if isinstance(fields, dict) else {"__error__": "the frontmatter is not a mapping"}


def headings(text):
    return [line[3:].strip() for line in text.split("\n") if line.startswith("## ")]


def section_rules():
    """Required and optional sections per template, read from the templates themselves."""
    rules = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "config", "templates", "*", "*.md"))):
        kind = os.path.basename(f)[:-3]
        required, allowed, placeholder = [], [], False
        for block in re.finditer(r"^## (.+?)$(.*?)(?=^## |\Z)", read(f), re.M | re.S):
            title = block.group(1).strip()
            if title.startswith("{"):
                placeholder = True
                break
            allowed.append(title)
            guide = re.search(r"<!--\s*(\w+)", block.group(2))
            if guide and guide.group(1).lower() == "required":
                required.append(title)
        if not placeholder and allowed:
            rules[kind] = (required, [t for t in allowed if t not in required])
    return rules


def check_sections(text, kind, rules):
    if kind not in rules:
        return []
    problems = []
    required, optional = rules[kind]
    present = [h.lower() for h in headings(text)]
    for s in required:
        if s.lower() not in present:
            problems.append("body: missing required section '## %s'" % s)
    allowed = [s.lower() for s in required + optional]
    for h in headings(text):
        if h.lower() not in allowed:
            problems.append("body: section '## %s' is not part of a %s (allowed: %s)"
                            % (h, kind, ", ".join(required + optional)))
    return problems


def load_vocabulary():
    voc = os.path.join(ROOT, "config", "vocabulary")
    projects = set((load_yaml(os.path.join(voc, "projects.yaml")).get("projects") or {}))
    products = load_yaml(os.path.join(voc, "products.yaml")).get("products") or {}
    tags = set()
    for group in (load_yaml(os.path.join(voc, "tags.yaml")).get("tags") or {}).values():
        tags.update(group or [])
    topology = {}
    for f in glob.glob(os.path.join(voc, "topology", "*.yaml")):
        topology[os.path.basename(f)[:-5]] = load_yaml(f)
    return projects, products, tags, topology


def check_vocabulary_links(projects, products):
    """Every product names the projects it runs on, and each one must exist."""
    problems = []
    for name, p in products.items():
        listed = (p or {}).get("projects")
        if not isinstance(listed, list):
            problems.append("product '%s': missing the 'projects' list" % name)
            continue
        for proj in listed:
            if proj not in projects:
                problems.append("product '%s': project '%s' is not in projects.yaml" % (name, proj))
    return problems


def check_schema(fields, schema):
    problems = []
    for name in schema.get("required", []):
        if name not in fields:
            problems.append("frontmatter: missing required field '%s'" % name)
    for name, value in fields.items():
        spec = schema.get("properties", {}).get(name)
        if spec is None:
            problems.append("frontmatter: field '%s' is not in the schema" % name)
            continue
        if value is None or value == "":
            problems.append("frontmatter: field '%s' is declared but empty: remove it or fill it" % name)
            continue
        if "enum" in spec and value not in spec["enum"]:
            problems.append("frontmatter: '%s' = '%s' is not allowed (expected: %s)"
                            % (name, value, ", ".join(spec["enum"])))
        if spec.get("type") == "string" and "pattern" in spec and not re.match(spec["pattern"], str(value)):
            problems.append("frontmatter: '%s' = '%s' does not match the expected format" % (name, value))
    for rule in schema.get("allOf", []):
        cond = rule.get("if", {}).get("properties", {})
        if not cond or any(fields.get(k) != v.get("const") for k, v in cond.items()):
            continue
        key, expected = next(iter(cond.items()))
        then = rule.get("then", {})
        for name in then.get("required", []):
            if name not in fields:
                problems.append("frontmatter: with %s '%s' the field '%s' is needed"
                                % (key, expected["const"], name))
        forbidden = then.get("allOf", []) + ([then["not"]] if "not" in then else [])
        for f in forbidden:
            for name in f.get("not", f).get("required", []):
                if name in fields:
                    problems.append("frontmatter: with %s '%s' the field '%s' does not belong"
                                    % (key, expected["const"], name))
    return problems


def check_topology(fields, topo, root_name):
    """Module and feature must exist in the topology, at the right place in the tree."""
    module, feature, topic = fields.get("module"), fields.get("feature"), fields.get("topic")
    if not module:
        return []
    if topo is None:
        return ["vocabulary: no topology/%s.yaml, so module and feature cannot be checked" % root_name]
    modules = topo.get("modules") or {}
    if module not in modules:
        return ["vocabulary: module '%s' is not in topology/%s.yaml" % (module, root_name)]
    if not feature:
        return []
    features = (modules[module] or {}).get("features") or {}
    if feature not in features:
        return ["vocabulary: feature '%s' is not under module '%s'" % (feature, module)]
    if topic and topic not in ((features[feature] or {}).get("topics") or []):
        return ["vocabulary: topic '%s' is not under feature '%s'" % (topic, feature)]
    return []


def check_ticket(path, schema, products):
    problems = []
    fields = load_yaml(path)
    if "__error__" in fields:
        return ["invalid YAML - %s" % fields["__error__"]]
    parts = os.path.relpath(path, os.path.join(ROOT, "core", "tickets")).replace(os.sep, "/").split("/")
    if len(parts) != 4 or parts[0] not in TICKET_STATES:
        return ["a ticket lives in core/tickets/{pending|served}/{product}/{code}/"]
    state, product, code = parts[0], parts[1], parts[2]
    problems += [p.replace("frontmatter: ", "") for p in check_schema(fields, schema)]
    if fields.get("product") not in products:
        problems.append("product '%s' is not in products.yaml" % fields.get("product"))
    if fields.get("product") != product:
        problems.append("the folder says product '%s', meta.yaml says '%s'" % (product, fields.get("product")))
    if str(fields.get("code")) != code:
        problems.append("the folder says code '%s', meta.yaml says '%s'" % (code, fields.get("code")))
    has_bill = os.path.exists(os.path.join(os.path.dirname(path), "bill.md"))
    if state == "served" and not has_bill:
        problems.append("a served ticket needs a bill.md")
    if state == "pending" and has_bill:
        problems.append("the ticket has a bill.md, so it belongs in served/")
    return problems


def check_file(path, rules, schemas, vocabulary):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    name = os.path.basename(path)
    projects, products, tags, topology = vocabulary

    if rel.startswith("core/tickets/"):
        return check_ticket(path, schemas["tickets"], products) if name == "meta.yaml" else []

    text = read(path)
    in_technical = rel.startswith("core/technical/")
    if in_technical and name in TECHNICAL_LEVEL_DOCS:
        return check_sections(text, name[:-3], rules)

    fields = frontmatter(text)
    if fields is None:
        return ["missing the YAML frontmatter at the top of the file"]
    if "__error__" in fields:
        return ["frontmatter: invalid YAML - %s" % fields["__error__"]]

    if in_technical:
        problems = check_schema(fields, schemas["technical"])
        folder = os.path.basename(os.path.dirname(path))
        if ENTRY_FOLDERS.get(folder) != fields.get("type"):
            problems.append("placement: a %s lives in %s/" % (fields.get("type"),
                            {v: k for k, v in ENTRY_FOLDERS.items()}.get(fields.get("type"), "?")))
        root_name = fields.get("project")
        if root_name and root_name not in projects:
            problems.append("vocabulary: project '%s' is not in projects.yaml" % root_name)
        kind = fields.get("type")
    else:
        problems = check_schema(fields, schemas["docs"])
        if name not in DOCS_FILES:
            problems.append("placement: core/docs/ holds only overview.md and topic.md")
        root_name = fields.get("product")
        if root_name and root_name not in products:
            problems.append("vocabulary: product '%s' is not in products.yaml" % root_name)
        kind = name[:-3]

    for t in fields.get("tags") or []:
        if t not in tags:
            problems.append("vocabulary: tag '%s' is not in tags.yaml" % t)
    problems += check_topology(fields, topology.get(root_name), root_name)
    problems += check_sections(text, kind, rules)
    return problems


def main():
    rules = section_rules()
    schemas = {d: json.loads(read(os.path.join(ROOT, "config", "schemas", d + ".json")))
               for d in ("technical", "docs", "tickets")}
    vocabulary = load_vocabulary()

    if len(sys.argv) > 1:
        files = [os.path.abspath(f) for f in sys.argv[1:]]
    else:
        files = sorted(glob.glob(os.path.join(ROOT, "core", "**", "*.md"), recursive=True))
        files = [f for f in files if "/core/tickets/" not in f.replace(os.sep, "/")]
        files += sorted(glob.glob(os.path.join(ROOT, "core", "tickets", "**", "meta.yaml"), recursive=True))

    total = 0
    problems = check_vocabulary_links(vocabulary[0], vocabulary[1])
    if problems:
        total += len(problems)
        print("\nconfig/vocabulary/products.yaml")
        for p in problems:
            print("   - %s" % p)

    for f in files:
        problems = check_file(f, rules, schemas, vocabulary)
        if problems:
            total += len(problems)
            print("\n%s" % os.path.relpath(f, ROOT).replace(os.sep, "/"))
            for p in problems:
                print("   - %s" % p)

    print("\n%d files checked, %d problems" % (len(files), total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
