# Week 4 - Day 4 Task Verification Log: `refactor-ai-spec` Execution

## Overview
This document logs the successful implementation, execution, and verification of the custom Claude Skill **`refactor-ai-spec`**. The input legacy code was processed using the custom skill rules defined in `SKILL.md`.

---

## Input Code Provided for Refactoring

```python
def get_user_scores(data):
    if data != None:
        if len(data) > 0:
            res = []
            for x in data:
                if x.get("is_active") == True:
                    if "score" in x:
                        res.append(x["score"] * 2)
            return res
    return []
```
## Refactored Code

```python
from typing import Any


def get_user_scores(data: list[dict[str, Any]] | None) -> list[int | float]:
    """
    Return doubled scores for all active users in the input data.

    Args:
        data: A list of user dicts, each possibly containing "is_active"
              and "score" keys. May be None.

    Returns:
        A list of doubled scores for users where is_active is True and
        a "score" key is present. Returns an empty list if data is
        None, empty, or no users qualify.
    """
    if not data:
        return []

    return [
        user["score"] * 2
        for user in data
        if user.get("is_active") is True and "score" in user
    ]