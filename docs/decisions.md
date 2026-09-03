# Engineering Decisions

---

## Decision #001

### Title

Offline First

### Status

Accepted

### Reason

Developers do not want to upload private repositories to external AI services.

Running locally guarantees privacy and allows usage without an internet connection.

### Trade-offs

- Large language models require powerful hardware.
- Local models may be slower than cloud models.

### Date

2026-07-18

---

## Decision #002

### Title

Context builders never render dangling headers

### Status

Accepted

### Reason

`==File==` was printed even when no file section was rendered, and `Dependencies:`
was printed above an always-empty list. Dangling headers pollute the LLM context
and waste tokens. Ownership is now explicit: `ProjectContextFormatter.build_dependencies()`
returns the full block (header + items) or an empty string, and `FileContextBuilder`
starts with an empty string instead of a fixed `==File==` header.

### Trade-offs

- Section headers are split between the formatter (`Dependencies:`) and
  `build_context` (`Relevant Files:`); acceptable until the context format is standardized.
- A regression test (`tests/test_context_output.py`) guards the no-dangling-headers rule.

### Date

2026-09-03