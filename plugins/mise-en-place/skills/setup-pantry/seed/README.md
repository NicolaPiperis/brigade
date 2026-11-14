# Pantry

The knowledge base of the mise-en-place skills: what we learned about the code, what the products do, and the record of every ticket.

## What it holds

- `core/technical/`: what working on the code teaches and the code does not say by itself. Traps, the choices made and why, the shapes that repeat, and each project's binding coding rules.
- `core/docs/`: what the products do, with which rules, and how they are used.
- `core/tickets/`: every ticket, from the request to the bill.

## How it is organised

Everything hangs from a precise place:

- technical: project → module → feature
- docs: product → module → feature → topic
- tickets: `pending/` → product → code while the ticket is open, `served/` → product → code once it is implemented

The names of those levels are registered in `config/vocabulary/`: projects in `projects.yaml`, products in `products.yaml`, each project's modules and features in `topology/{project}.yaml`, tags in `tags.yaml`. A name that is not there does not exist; registering one is a deliberate act.

### Technical

Every level has a `map.md`: one line for each thing at that level, title and summary. Entries sit next to it, grouped by type:

- `gotchas/`: the system does something you would not expect
- `decisions/`: a choice made, and why
- `patterns/`: a shape that repeats, and how to follow it

A project also holds `rules.md`, its binding coding rules. A module holds `structure.md`, a snapshot of how it is built.

### Docs

`overview.md` at product, module and feature level; `topics/{topic}/topic.md` at the leaf.

### Tickets

One folder per ticket:

```
{code}/
├── meta.yaml       product, code, type, title
├── order.md        the order: the ticket as it was asked
├── recipe.md       the spec, written by recipe
├── prep-list/      the tasks, one file each, written by prep-list
└── bill.md         the closing, written by bill
```

Where a ticket stands is read from where its folder sits and what it holds: `recipe.md` means it is specced, `prep-list/` that it is planned, `bill.md` that it is closed. `served/` means implemented, not released to production.

## How it is read and written

Read by walking down the `map.md` files and opening only what bears on the work. Written by the mise-en-place skills, which follow the templates in `config/templates/`. Every entry carries `last_verified`: the last time someone confirmed it is still true.

## Where the rules live

`config/` holds no knowledge, only the rules that govern it:

- `vocabulary/`: the allowed names
- `templates/`: the shape of each document, its sections and its metadata
- `schemas/`: the rules for the metadata
- `tooling/`: the validator

Whatever enters the pantry passes the validator, which checks sections against the templates, metadata against the schemas, names against the vocabularies, and where each file sits:

```
python config/tooling/validate_pantry.py
```
