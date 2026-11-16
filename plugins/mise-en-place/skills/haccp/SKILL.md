---
name: haccp
description: Threat-model a design or an existing feature with STRIDE, on the trust boundaries it touches, grounded in the code. Use when a design touches a trust boundary, and when the user asks whether a design is secure.
---

# HACCP

## Scope: the trust boundaries

Model only the boundaries the design touches:

- an endpoint added or changed;
- permissions and access checks;
- input from outside: files, imports, integrations, messages;
- data shared across tenants, users or roles;
- credentials and secrets.

With none touched, say so in one line, "no trust boundary touched", and stop.

## STRIDE, boundary by boundary

For each boundary touched, go through the six categories and keep the ones that apply:

- **Spoofing**: can someone act as another user or system?
- **Tampering**: can input or stored data be altered on the way?
- **Repudiation**: can an action go untraced?
- **Information disclosure**: can data reach someone who must not see it: another tenant, user or role?
- **Denial of service**: can a request or an input exhaust the system?
- **Elevation of privilege**: can someone do what their role does not allow?

Put the questions to the user in grilling's rounds: call the Skill tool with "mise-en-place:grilling" when it is not already running.

## Evidence

Go into the code through `locate-stations`.

- A threat is confirmed by its path in the code: the entry point, what checks it, what reaches the data.
- Its severity is its impact: what is lost, and by whom.
- A missing second layer, where the first one holds, is a hardening note.
- What you cannot trace in the code is an open question for whoever can answer it.

## Decisions

For each confirmed threat, the user picks one of three ways:

- **mitigated in the work in hand**: an acceptance criterion of the task that builds that part, with its security test;
- **a weakness already in the code the design touches**: fixed first, by a preparatory task at the head of the plan;
- **out of scope**: named, to be handled on its own, in a ticket of its own.

Done when every confirmed threat has its decision.

## Output

For each boundary touched, a list: the threat with its STRIDE category, its path in the code, its impact, the decision. After it, kept apart, the hardening notes and the open questions, each with who can answer it.

This is the block the recipe carries.
