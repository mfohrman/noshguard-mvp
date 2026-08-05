# Engineering Rules — NoshGuard

**Read this before writing or modifying any code in this repository.**

NoshGuard is a food-safety product. Its entire value is that a number on a screen
is true. A wrong number here is not a cosmetic defect — it is the product failing
at its only job. These rules exist because every one of them was violated, found
in production, and cost real time to undo.

---

## 1. Never fabricate a value

If a value is unknown, unavailable, or not yet computed:

- Return `None`, `null`, or an empty collection.
- Display `n/a`, `unknown`, or nothing at all.

**Never** substitute a placeholder, sample, representative, plausible, or
"reasonable default" value for something the system does not actually know.

This applies to defaults in `.get()` calls. `r.get("units_affected", 0)` is a
default. `r.get("units_affected", 50000)` is a fabrication.

## 2. Empty must render as empty

If a query returns no rows, the UI shows "no results." It does not fall back to
sample data, session data, demo data, or anything else. An empty database is a
valid state and must be displayed honestly.

Never generate example records inside a code path that production also runs.

## 3. Demo data lives behind an explicit flag

Demo or seed data is permitted only behind a flag the operator sets deliberately.
It is never a fallback triggered by an error, an empty table, or a failed API call.

If a live path fails, surface the failure. Do not silently substitute demo data.

## 4. UI copy is a factual claim — verify it in the code first

Before writing or keeping any statement about what the system does — data
retention, security, transmission, persistence, alert behavior — trace the actual
code path and confirm it is true.

If you cannot verify it, do not write it. If you find existing copy that is not
true, flag it immediately, even if you were not asked to look.

## 5. Fail closed

Missing config, missing secret, missing credential, unexpected state: deny,
raise, or stop. Never default to permissive behavior.

## 6. No secrets in source

No API keys, tokens, passwords, or credentials in code — this repository is
public. Read them from environment variables or the platform's secret store,
with no hardcoded fallback value.

## 7. Do not swallow exceptions

No bare `except:` and no `except: pass`. Catch specific exceptions and log them
with enough context to identify the function and the failure. A silent failure
is worse than a crash: a crash gets fixed, a silent failure ships.

## 8. Say what you did not verify

When reporting work, state explicitly what was checked and what was assumed.
"I did not verify X" is a useful sentence. Confident silence about an unchecked
assumption is how bad code ships.

---

## Codebase-specific traps

**`dashboard.py` truncation.** `web_fetch` silently cuts this file at ~2,070
lines. The real file is ~4,600. Always pull it through the browser and confirm
the line count before analyzing or editing. This has misled three separate
sessions, including one that concluded the file "did not match the spec."

**Bracket notation.** Fields
