from cases.profiles import CASES, ACTIVE_CASE

LEVEL_ORDER = ["Junior", "Senior", "Head", "Chief", "CEO"]


def get_profile(target_email: str):
    if not target_email:
        return None
    return CASES.get(target_email.lower())


def get_cases_for_target(target_email: str):
    profile = get_profile(target_email)
    if not profile:
        return []
    return profile.get("cases", [])


def get_active_case(target_email: str):
    profile = get_profile(target_email)
    if not profile:
        return None

    email = target_email.lower()
    idx = ACTIVE_CASE.get(email, 0)
    cases = profile.get("cases", [])

    if idx < 0 or idx >= len(cases):
        return None

    return cases[idx]


def get_active_case_index(target_email: str):
    if not target_email:
        return 0
    return ACTIVE_CASE.get(target_email.lower(), 0)


def advance_case(target_email: str):
    email = target_email.lower()
    profile = get_profile(email)

    if not profile:
        return False

    current = ACTIVE_CASE.get(email, 0)
    total = len(profile.get("cases", []))

    if current + 1 < total:
        ACTIVE_CASE[email] = current + 1
        return True
    else:
        # do not move past the last case
        return False


def reset_active_cases():
    for email in CASES.keys():
        ACTIVE_CASE[email.lower()] = 0


def get_all_cases():
    """
    Flatten all cases from all targets into one list.
    Adds owner/target info into each case dict copy.
    """
    all_cases = []

    for target_email, profile in CASES.items():
        for case in profile.get("cases", []):
            case_copy = case.copy()
            case_copy["target_email"] = target_email
            case_copy["target_name"] = profile.get("name")
            case_copy["target_role"] = profile.get("role")
            case_copy["target_department"] = profile.get("department")
            all_cases.append(case_copy)

    return all_cases


def get_cases_by_level(level_name: str):
    return [case for case in get_all_cases() if case.get("level") == level_name]


def get_case_by_id(case_id: str):
    if not case_id:
        return None

    for target_email, profile in CASES.items():
        for case in profile.get("cases", []):
            if case.get("case_id") == case_id:
                case_copy = case.copy()
                case_copy["target_email"] = target_email
                case_copy["target_name"] = profile.get("name")
                case_copy["target_role"] = profile.get("role")
                case_copy["target_department"] = profile.get("department")
                return case_copy

    return None


def normalize_text(text):
    if text is None:
        return ""
    return str(text).strip().lower()


def check_required_info(email_text: str, required_info: list):
    """
    Simple keyword-based checker.
    Useful for backup validation or debugging beside the LLM checker.
    """
    body = normalize_text(email_text)
    matched = []
    missing = []

    for item in required_info:
        item_norm = normalize_text(item)
        if item_norm and item_norm in body:
            matched.append(item)
        else:
            missing.append(item)

    return {
        "status": len(missing) == 0,
        "matched": matched,
        "missing": missing
    }


def build_player_progress(log_rows, player_email: str):
    """
    Reads player progress from logs.
    Expected row keys:
      - player
      - case_id
      - status or success
      - flag (optional)
    """
    completed_case_ids = set()
    collected_flags = set()

    player_email = normalize_text(player_email)

    for row in log_rows:
        row_player = normalize_text(row.get("player"))
        if row_player != player_email:
            continue

        # support both 'status' and 'success'
        raw_status = row.get("status", row.get("success", False))
        success = str(raw_status).strip().lower() in ("true", "1", "yes", "success")

        if not success:
            continue

        case_id = row.get("case_id")
        if case_id:
            completed_case_ids.add(case_id)

        flag = row.get("flag")
        if flag:
            collected_flags.add(flag)

    return {
        "completed_case_ids": completed_case_ids,
        "collected_flags": collected_flags,
    }


def is_level_complete(level_name: str, completed_case_ids: set):
    level_cases = get_cases_by_level(level_name)
    if not level_cases:
        return False

    for case in level_cases:
        if case.get("case_id") not in completed_case_ids:
            return False

    return True


def get_unlocked_levels(completed_case_ids: set):
    """
    Unlock logic:
    - Junior always unlocked
    - Senior unlocks only after all Junior cases are completed
    - Head unlocks only after all Senior cases are completed
    - etc.
    """
    unlocked = []

    for i, level_name in enumerate(LEVEL_ORDER):
        if i == 0:
            unlocked.append(level_name)
            continue

        previous_level = LEVEL_ORDER[i - 1]
        if is_level_complete(previous_level, completed_case_ids):
            unlocked.append(level_name)
        else:
            break

    return unlocked


def is_case_unlocked(case: dict, completed_case_ids: set):
    if not case:
        return False

    case_level = case.get("level")
    unlocked_levels = get_unlocked_levels(completed_case_ids)
    return case_level in unlocked_levels


def get_progress_summary(log_rows, player_email: str):
    progress = build_player_progress(log_rows, player_email)
    completed_case_ids = progress["completed_case_ids"]
    collected_flags = progress["collected_flags"]
    unlocked_levels = get_unlocked_levels(completed_case_ids)

    levels = []
    for level_name in LEVEL_ORDER:
        level_cases = get_cases_by_level(level_name)
        total_count = len(level_cases)
        done_count = sum(
            1 for case in level_cases
            if case.get("case_id") in completed_case_ids
        )

        levels.append({
            "level": level_name,
            "done": done_count,
            "total": total_count,
            "unlocked": level_name in unlocked_levels,
            "completed": total_count > 0 and done_count == total_count
        })

    return {
        "completed_case_ids": completed_case_ids,
        "collected_flags": collected_flags,
        "unlocked_levels": unlocked_levels,
        "levels": levels,
        "total_completed_cases": len(completed_case_ids),
        "total_flags": len(collected_flags)
    }


def can_attempt_case(case: dict, log_rows, player_email: str):
    """
    Used by the backend before checking an email against a case.
    """
    if not case:
        return False

    progress = get_progress_summary(log_rows, player_email)
    return case.get("level") in progress["unlocked_levels"]


def get_available_active_cases_for_player(log_rows, player_email: str):
    """
    Returns the current active case for each target,
    plus whether it is unlocked for this player.
    """
    progress = get_progress_summary(log_rows, player_email)
    completed_case_ids = progress["completed_case_ids"]

    active_cases = []

    for target_email in CASES.keys():
        case = get_active_case(target_email)
        if case:
            case_copy = case.copy()
            case_copy["target_email"] = target_email
            case_copy["target_name"] = CASES[target_email].get("name")
            case_copy["unlocked"] = is_case_unlocked(case_copy, completed_case_ids)
            active_cases.append(case_copy)

    return active_cases

def get_cases_by_level_sorted(level_name: str):
    cases = [case for case in get_all_cases() if case.get("level") == level_name]
    return sorted(cases, key=lambda c: c.get("order_in_level", 999))


def is_case_completed(case_id: str, completed_case_ids: set):
    return case_id in completed_case_ids


def get_first_incomplete_case_in_level(level_name: str, completed_case_ids: set):
    level_cases = get_cases_by_level_sorted(level_name)
    for case in level_cases:
        if case.get("case_id") not in completed_case_ids:
            return case
    return None


def can_open_case(case: dict, completed_case_ids: set):
    if not case:
        return False

    # level must already be unlocked
    unlocked_levels = get_unlocked_levels(completed_case_ids)
    if case.get("level") not in unlocked_levels:
        return False

    # only first incomplete case in that level is playable
    first_incomplete = get_first_incomplete_case_in_level(case.get("level"), completed_case_ids)
    if first_incomplete is None:
        return True

    return case.get("case_id") == first_incomplete.get("case_id")


def get_next_case_in_level(case: dict):
    if not case:
        return None

    level_cases = get_cases_by_level_sorted(case.get("level"))
    current_id = case.get("case_id")

    for i, item in enumerate(level_cases):
        if item.get("case_id") == current_id:
            if i + 1 < len(level_cases):
                return level_cases[i + 1]
            return None
    return None  

def get_cases_by_level_sorted(level_name: str):
    cases = [case for case in get_all_cases() if case.get("level") == level_name]
    return sorted(cases, key=lambda c: c.get("order_in_level", 999))


def is_case_completed(case_id: str, completed_case_ids: set):
    return case_id in completed_case_ids


def get_first_incomplete_case_in_level(level_name: str, completed_case_ids: set):
    level_cases = get_cases_by_level_sorted(level_name)
    for case in level_cases:
        if case.get("case_id") not in completed_case_ids:
            return case
    return None


def can_open_case(case: dict, completed_case_ids: set):
    if not case:
        return False

    unlocked_levels = get_unlocked_levels(completed_case_ids)
    if case.get("level") not in unlocked_levels:
        return False

    first_incomplete = get_first_incomplete_case_in_level(case.get("level"), completed_case_ids)
    if first_incomplete is None:
        return True

    return case.get("case_id") == first_incomplete.get("case_id")


def get_next_case_in_level(case: dict):
    if not case:
        return None

    level_cases = get_cases_by_level_sorted(case.get("level"))
    current_id = case.get("case_id")

    for i, item in enumerate(level_cases):
        if item.get("case_id") == current_id:
            if i + 1 < len(level_cases):
                return level_cases[i + 1]
            return None

    return None     