# {code} - {title}

**Author:** {developer}
**Date:** {YYYY-MM-DD}

## Work Log
<!-- required: for project managers and developers: technical and precise. -->

### Description
<!-- required: one line per change, saying what changed in the system. The implementation detail (which file, which method, which guard) stays in the tasks' Comments: repeated here, it makes two versions that part ways at the first correction. Measured numbers belong here, where they are evidence. -->

### Notes
<!-- required: one line per note: decisions, technical debt, the scope of the release. What the diff does not say (no script to apply, the backend untouched) goes here. With none: "None." -->

## Changelog
<!-- required: for the customer: at most three lines, one piece of information each, saying what changes for them, not how it was built. -->

## QA Tests
<!-- required: for whoever tests: repeatable steps, verifiable outcomes. -->

### Prerequisites
<!-- required: one line per condition (environment, data, configuration), each saying what kind of record the tests need, with every property the expected outcomes rely on. Where the record has to be created, say so: the test's first steps build it. -->

### Test 1 - {name}
<!-- One test covers what can be done in one pass; a new test only when the login, the starting screen or the data must change.

Steps name what the tester sees: button labels, page, tab and filter names, never a file or a class. A step stays generic and carries its example in brackets. Every step that produces an outcome has its Expected lines right under it; a step whose outcome falls midway is split in two.

An Expected line states the behaviour that must hold, in terms that stay true whatever the data holds: no code, name, value or count taken from an example. When the behaviour shows only by comparison, compare the outcomes of two steps of the same test. When the screen does not show the property an Expected line checks, a QA note says how the tester recognises it; if it cannot be recognised, the line is rewritten.

Steps in another application use its real labels, read in its source. -->

**Goal:** {what is verified}

1. {action} ({example})
   - Expected: {the behaviour that must hold}

### QA Notes
<!-- optional: warnings for whoever tests. -->
