---
name: setup-pantry
description: "Set up your pantry: create a new, empty one or connect to one that already exists. Run once, before the first use of the other mise-en-place skills."
disable-model-invocation: true
---

# Setup pantry

The **pantry** is the knowledge base the mise-en-place skills read from and write to: what the kitchen knows about the code (`technical`), what the products do (`docs`), and every ticket (`tickets`). Each user has one pantry for all their projects; a team can share one.

Two files tie it together:

- **`pantry.yaml`**, at the pantry root, describes the pantry. Its presence is what makes a folder a pantry.
- **The pointer**, `~/.claude/brigade.yaml`, tells the skills where the user's pantry is. It is personal: each user has their own.

This skill writes the pantry and the pointer. It is prompt-driven: explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Read the pointer.

- **It names a folder holding a `pantry.yaml`**: the user already has a pantry. Tell them where it is and stop. If they asked you to verify it, compare it with [seed/](seed/), run `python config/tooling/validate_pantry.py` from the pantry root, and report both results, writing nothing. If they want to switch to another pantry, go on to step 2.
- **It names a folder without a `pantry.yaml`, or a folder that is gone**: tell the user, then go on to step 2.
- **There is no pointer**: go on to step 2.

Done when you know which of the three cases applies.

### 2. Ask

One question, one answer, then the next. Lead each question with the recommended answer, so the user can accept it in a word.

**New or existing.**

> Do you want a new pantry, or to connect to one that already exists? (recommended: **new**)

**New pantry: where.** Propose `~/pantry`. The folder must be empty or not exist yet.

**Existing pantry: where.** A folder on this machine, or a git URL to clone (then ask where to clone it). Check that its root holds a `pantry.yaml`; a folder without one is not a pantry, so tell the user and ask again.

Done when you have a folder and know whether to create it or connect to it.

### 3. Confirm

Show the user a draft:

- **New pantry**: the folder tree you will create from [seed/](seed/), and the pointer.
- **Existing pantry**: the pointer.

Let them edit it. Done when the user approves the draft.

### 4. Write

**New pantry:**

1. Copy [seed/](seed/) into the folder.
2. Set `created` in `pantry.yaml` to today's date.
3. Run `git init` and commit everything as the first commit.

**Both cases**, write the pointer:

```yaml
pantry: <absolute path of the pantry>
```

Done when the pointer names a folder whose root holds `pantry.yaml`.

### 5. Done

Tell the user where the pantry is, and that `grill-from-pantry`, `restock`, `inventory` and `bill` now read it. To check the pantry later, they run this skill again and ask it to verify.
