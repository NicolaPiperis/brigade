---
name: grill-from-pantry
description: A relentless interview to sharpen a plan or design, which also writes to the pantry (terms and decisions) as we go.
disable-model-invocation: true
---

Call the Skill tool twice, for "mise-en-place:grilling" and "mise-en-place:menu".

## The ticket

Before the first round, ask once whether the work is a ticket (recommended: **yes**).

- **A ticket with an `order.md`**: find it by its code under the pantry's `core/tickets/pending/` and read it. It is the request as it was made: grill from it.
- **A ticket without one**: open it now, before the grill reshapes the request.
  1. Ask for the ticket's code once. With none, propose a short name drawn from the request (`partial-cancellation`) for the user to confirm or change.
  2. Deduce the product from `config/vocabulary/products.yaml`. A product the vocabulary lacks is registered first, through `restock`.
  3. Draft `core/tickets/pending/{product}/{code}/order.md` from the template `config/templates/tickets/order.md`, with the request in the user's words. Show it whole and write it on the user's go.
- **Not a ticket**: grill the design as the user states it.

Done when the request the grill starts from is settled: the order read, the order written, or the design stated.

## Established facts

**A decision closes only on facts checked in this session.** A fact you can reach, in the code or the pantry, you check now: open the file, read the entry, or send a sub-agent. A fact you cannot reach (it needs a person, a running system, data that does not exist yet) stays open: say who can check it, and mark every decision that rests on it as waiting. Writing "to verify" next to a closed decision hides an open question: whoever checks later either finds nothing, and the note was useless, or finds something, and reopens a design everyone thought was settled.

**What the pantry holds is established**, unless `inventory` flags it as stale. A question this interview is about to ask may already be answered there, at the cost of one file instead of a search through the code: look there first. Whenever the interview reaches a module the first read did not cover, read it with `inventory`.

## Facts from the code

Go into the code through `locate-stations`: it gives the project's path and how to find symbols there.

Where the design makes existing code run in cases it did not run in before (a condition dropped or widened), find who reaches it: each caller is a case to decide.

## Then, the threats

Once the rest of the design is settled, call the Skill tool with "mise-en-place:haccp". Its questions join the rounds.

## Last, the seams

Once everything else is settled, the threats included, decide **where this will be tested**: the seams that will host its functional and security tests. Prefer a seam that already exists, take the highest one, and the fewest possible: one is the ideal number. Propose only the kinds of test the project's `rules.md` allows; with no rule on it, none is excluded. The seam vocabulary is `partie`'s.

A seam where a test would pass **without catching the real defect** is not a seam. Awkward seams in old code are fine; the one that matters is the one that would give false confidence. Where that is all there is, offer `/deep-clean`, which redesigns the seam before the recipe is written. Offer it, never impose it: the answer may be that there is no time, and then the choice is a weaker seam or no test. If the user accepts, they type the command themselves: it cannot be invoked from here.

**Whichever way it goes, it is written down.** Six months later, a test skipped on purpose and a test forgotten look the same to someone reading a green suite.

## Done

The session is done when grilling's frontier is empty and every fact a decision stands on is established here. With such a fact still missing, the session is not done: say which decisions wait on it.
