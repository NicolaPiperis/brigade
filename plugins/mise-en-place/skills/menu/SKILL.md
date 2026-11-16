---
name: menu
description: Build and sharpen a product's domain model. Use when discussing the domain's terminology, writing or editing the Terms of the pantry's overviews, or when a decision worth recording emerges.
---

# Menu

Actively build and sharpen the domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the terms down the moment they crystallise. (Merely *reading* the Terms for vocabulary is not this skill: that's a one-line habit any skill can do, through `inventory`. This skill is for when you're changing the model, not just consuming it.)

## Where the language lives

All of it in the pantry:

- **the Terms**: the `## Terms` section of the docs overviews, what each word of the domain means. A term sits in the lowest overview that covers every place it is used.
- **the vocabularies** in `config/vocabulary/`: the names of projects, products, modules, features and topics. Closed sets: a name that is not there does not exist, and a new one is a candidate, never a name you use.
- **the entries**: where a term diverges in *behaviour* and not just in name, the gap is a gotcha or a decision, sitting at the level it applies to.

Before the session, read the point you design on with `inventory`. Done when you hold the Terms of every overview in its chain.

## During the session

### Challenge against the Terms

When the user uses a term that conflicts with the existing language in the Terms, call it out immediately. "Your Terms define 'cancellation' as X, but you seem to mean Y. Which is it?" A name the vocabulary calls otherwise is the same challenge: "You're saying 'registry'; this project has `vehicle-registry` and `item-registry`. Which one?" A name that resolves to two nodes is a question, not a detail.

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things." The precise term is the one the Terms, the vocabularies, the docs or the code already use; coin a new one only when none of them has it.

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees; `locate-stations` gives you the project's path. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?" A contradiction that survives the check is often a gotcha: offer it to `restock`.

### Write the Terms inline

When a term is resolved, update the Terms right there. Don't batch these up: capture them as they happen. Show the term exactly as it will be saved, and write it on the user's go. Use the format in the `## Terms` comment of the overview template, `config/templates/docs/overview.md`, in the language the pantry is written in.

The Terms should be totally devoid of implementation details. Do not treat them as a spec, a scratch pad, or a repository for implementation decisions. They are a glossary and nothing else.

When the overview the term belongs in does not exist yet, create it from the template: the term, plus a draft of `What it does` and `Contents` from what the session established, shown whole before writing. A product or level the vocabulary lacks is registered first, through `restock`.

### Offer the rest to restock

Offer to `restock`, the moment it crystallises:

- **a decision**, sparingly: only when it passes the three tests in [restock's WHEN-A-DECISION.md](../restock/WHEN-A-DECISION.md), read before offering one;
- **a gotcha**: a contradiction between what is said and what the code does that survived the check;
- **a name** a vocabulary lacks.

On the user's go, call `restock` with it. Its own criteria and confirmation still apply. This holds whoever invoked you.

Done when every term resolved in the session sits in the Terms, and every decision, gotcha and name that crystallised has been offered to `restock`.
