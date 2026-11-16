---
name: costing
description: Size a recipe in hours: the development breakdown, documentation and test. Use when recipe sizes the spec it writes, and when the user asks for the hours of a recipe or a recalculation.
---

# Costing

You are the **quantity surveyor** on this ticket. The design is signed off and the drawings are in your hand; you walk the code with a tape measure and come back with the bill.

## 1. Take the recipe

Called by `recipe`, size the spec settled in this session, before it becomes a file. Called on its own, read the recipe from the text the user pasted, or from the ticket in the pantry: `core/tickets/{pending|served}/{product}/{code}/recipe.md`.

Done when you hold the delta to build.

## 2. Establish the facts

The breakdown rests on four facts:

- where the behaviour to change originates, as `file:line`;
- whether the change alters a signature, externally visible semantics, or when the existing code runs, and how many callers it has, hidden ones included: schedulers, batch jobs, other services;
- the overloads carrying the same logic;
- whether the impacted code has tests.

Read them off the recipe and what this session has established; get each one still missing from the code, through `locate-stations`. Ask the user for whatever only they know.

Done when all four are established.

## 3. Build the breakdown

Every development hour is decided here, once. **The base hour** is the time a developer who knows the product takes to build it by hand, with no surprises: net, not prudential. Each line is estimated in base hours.

| Line | When |
|---|---|
| The delta work | always: one line per activity or layer |
| Caller check | the change alters a signature, visible semantics, or when the code runs |
| Overload replication | the logic lives in several signatures |
| Context re-entry | the ticket can be interrupted by higher priorities |
| Preparatory security task | `haccp` sent a weakness already in the code to a task of its own |

A fact that moves the hours **becomes a line with its price**: a hidden consumer, an overload, a copy constructor carrying the field, a piece with no tests. A surveyor who finds a load-bearing wall the drawings missed puts it in the bill; the design stays signed off.

Callers count when the change makes code run in cases it did not run in before. A branch rewritten to do the same work differently leaves them at zero, however many there are. The size of a class costs nothing: a point change in a 30,000-line class costs what it costs in a 300-line one.

## 4. Set the size

The lines of step 3 add up to the size. The size sets documentation and test.

| Size | Lines of step 3 | Documentation | Test |
|---|---|---|---|
| XS | up to 4h | 0.5h | 2h |
| S | 4-8h | 0.5h | 2h |
| M | 8-24h | 1h | 4h |
| L | 24-40h | 1h | 6h |
| XL | 40-100h | 2h | 8h |
| XXL | over 100h | 2h | 10h |

Test is the manual test of the finished work.

## 5. Print

Development is the lines plus documentation, rounded up to the next half hour. The total adds development and test. Print the block in the language the pantry is written in:

```
ESTIMATE - {CODE} - {TITLE}

Development:
  - {activity / layer} ............ {h}h   {note}
  - Check of {N} callers .......... {h}h   {only when callers count}
  - Replication on {N} overloads .. {h}h
  - Context re-entry x{N} ......... {h}h   {only when the ticket can be interrupted}
  - Preparatory security task ..... {h}h   {only when haccp sent one}
                                   ---------
                          lines ... {h}h   (size {XS|S|M|L|XL|XXL})
  - Documentation ................. {h}h

Development estimate: ~{N}h
Test estimate:        ~{N}h
TOTAL:                ~{N}h
```

Called on its own on a recipe in the pantry, offer to write the block into its `## Estimate`, and write it on the user's go.

## The standard

An estimate is either certain or not delivered. A datum you lack, you ask for. A piece resting on data you cannot reach (a running system, figures nobody has yet) stays unestimated, and you name it. A safety margin added on top hides an unfinished analysis.
