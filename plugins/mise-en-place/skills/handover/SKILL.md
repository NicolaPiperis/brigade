---
name: handover
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace. A document meant to outlive the next session (a decision to keep, something for a person) goes where the user says; when they have not said, ask.

Write down only what exists nowhere else: the decisions taken in this session with the reasons behind them, what was tried and dropped, and the questions still open.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for, and what each one is for.

Do not duplicate content already captured in other artifacts (the ticket's recipe and tasks, the pantry's entries, commits, diffs). Reference them by path or URL instead: two documents saying the same thing part ways at the first correction, and the reader cannot tell which one is right.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
