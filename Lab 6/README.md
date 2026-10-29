# L6_L7_51
 — Self Storage

Lab 6: Code and Branch Coverage

## About

A small Python module that works out storage rent by unit size, months, climate control and membership, checks whether access is allowed and reports payment status.

## Files

| File | Description |
|------|-------------|
| `self_storage.py` | The module under test |
| `test_self_storage.py` | Starter test file |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Coverage Analysis

| Test file | Tests | Line coverage | Branch coverage |
|-----------|-------|---------------|-----------------|
| `test_self_storage.py` (starter) | 2 | 38% | 32% |
| `CodeCoverageTest_self_storage.py` | 11 | 100% | 98% (missing `21->23`) |
| `BranchCoverageTest_self_storage.py` | 26 | 100% | 100% |

**Code coverage.** The starter tests only ran the "within deposit" path of `rent_due` and one path of `access_allowed`; `payment_status` was never called. `CodeCoverageTest_self_storage.py` adds one test per unexecuted line: invalid unit size, negative months, member discount month, climate and non-climate rates, the long-stay discount, owner access, out-of-hours access, and the current / grace / lien payment results. This gives 100% line coverage.

**Branch coverage.** Even at 100% line coverage, branch coverage reports `21->23` as missed: a long stay (`extra > 6`) was only tested with climate control, so the inner `if is_climate` never evaluated to False. This shows how line coverage can hide untested decisions. `BranchCoverageTest_self_storage.py` adds the non-climate long stay, a large-unit member (where the member bonus does not apply), owners with too many visitors, early and late hours, and boundary values (`months = 0`, `extra = 6`, hours 6 and 22, `days_to_due` at the cutoff and at `cutoff - 15`). This gives 100% branch coverage.

Terminal output screenshots are in the `screenshots/` folder.
