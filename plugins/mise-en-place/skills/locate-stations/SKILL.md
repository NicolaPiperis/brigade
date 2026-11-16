---
name: locate-stations
description: Locate a pantry project on this machine and read its code: resolve its local path, keep the project-to-path map, find symbols with the right tool. Use whenever a project's code has to be found, opened or read, and when the user adds, edits or lists the paths.
---

# Locate stations

`locate-stations` is the map between the **projects of the pantry**, the stations of the brigade, and their **local paths on this machine**. It has three faces:

- **Lookup**, the main use, called by other skills or by you: returns a project's path.
- **Reading**: how to find symbols in the code once you are there.
- **Management**, on the user's request: add, edit or list the paths.

Why it exists: local paths differ from machine to machine and from user to user, while a pantry can be shared by a team. So the pantry keeps **which projects exist**, the same for everyone, and the pointer keeps **where they sit here**, one user's local state.

## Where the data lives

In the pointer, `~/.claude/brigade.yaml`, under `projects`:

```yaml
pantry: C:/path/to/pantry
projects:
  shelfwise: C:/path/to/shelfwise
```

The keys are the projects registered in the pantry's `config/vocabulary/projects.yaml`. With no pointer there is no pantry yet: tell the user to run `/setup-pantry` and stop.

## Reconcile: every time the pointer is read

Compare the keys under `projects` with the vocabulary:

| Key in the pointer | What to do |
|---|---|
| registered in the vocabulary | keep it |
| missing from the vocabulary | keep it, and tell the user in one line that the project is mapped here but not registered in the pantry |

A path is never lost. When nothing differs, leave the pointer untouched.

## Lookup: resolving a path

1. Read the pointer and reconcile it.
2. Look for the project asked for.
3. Three outcomes:
   - **Mapped** → return the path.
   - **Registered but not mapped** → ask the user for its path, once, validate it (below), write it under `projects`, and return it.
   - **Not registered** → answer that the pantry does not know the project. Registering a name in the vocabulary is a deliberate act, done through `restock`.

Done when the caller holds a path, or knows the project is not registered.

## Reading: finding symbols

For callers, implementations, overrides and usages, use a code-analysis tool when one is available (an IDE engine, a language server): text search finds names, not symbols. Without one, carry on with text search and read each hit to confirm it is the symbol you mean.

When you dispatch a sub-agent to find a fact in the code, tell it which of the two to use: it inherits the tools, not this instruction.

## Management: add, edit, list

Read and reconcile the pointer first, then offer the mode. There are exactly three:

- **Add**: present the registered projects that are not mapped as a numbered list, and ask the user to answer with the numbers or the names they hold locally. For each one, ask for the path, one at a time.
- **Edit**: present the mapped projects; for the chosen ones ask for the new path. Changing an existing path takes an explicit confirmation: a correct path overwritten by mistake is worse than a missing one.
- **List**: show which projects are mapped and which are not.

The mapped projects stay out of Add: a machine already set up stays as it is unless the user asks to change it.

Done when every change the user asked for is written in the pointer.

## Validating a path

Before writing a path the user gave:

- **Normalise** it: forward slashes, no trailing slash.
- **Check that it exists.** Where it does not, say so and ask for confirmation before saving.

A visible error beats a wrong path saved quietly.
