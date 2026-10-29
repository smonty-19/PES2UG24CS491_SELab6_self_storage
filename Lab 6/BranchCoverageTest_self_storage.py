import pytest
from self_storage import rent_due, access_allowed, payment_status

# Test cases chosen so that every decision in self_storage.py evaluates
# to both True and False, plus boundary values for each condition.


# ---------- rent_due ----------

def test_within_deposit_months():
    # extra <= 0 -> True
    assert rent_due("small", 1, False, False) == 0

def test_unknown_unit_size():
    # unit_size not in DEPOSIT_MONTHS -> True
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("tiny", 3, False, False)

def test_negative_months():
    # months < 0 -> True
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)

def test_zero_months():
    # months < 0 -> False at the boundary
    assert rent_due("small", 0, False, False) == 0

def test_member_non_large_gets_extra_month():
    # is_member and unit_size != "large" -> True
    # medium: covered 2 + 1 = 3, extra = 2, rate = 80
    assert rent_due("medium", 5, False, True) == 160

def test_member_large_no_extra_month():
    # is_member True but unit_size == "large" -> False
    # large: covered 3, extra = 2, rate = 80
    assert rent_due("large", 5, False, True) == 160

def test_member_covered_by_extra_month():
    # small member: covered 1 + 1 = 2, months = 2 -> extra = 0
    assert rent_due("small", 2, False, True) == 0

def test_climate_short_stay():
    # is_climate -> True, extra > 6 -> False
    # small: covered 1, extra = 3, rate = 120
    assert rent_due("small", 4, True, False) == 360

def test_non_climate_short_stay():
    # is_climate -> False, extra > 6 -> False
    assert rent_due("small", 4, False, False) == 240

def test_extra_exactly_six_no_discount():
    # extra > 6 -> False at the boundary (extra = 6)
    assert rent_due("small", 7, False, False) == 480

def test_climate_long_stay_discount():
    # extra > 6 -> True, inner is_climate -> True
    # small: extra = 9, rate = 120 - 10 - 5 = 105
    assert rent_due("small", 10, True, False) == 945

def test_non_climate_long_stay_discount():
    # extra > 6 -> True, inner is_climate -> False
    # small: extra = 7, rate = 80 - 10 = 70
    assert rent_due("small", 8, False, False) == 490


# ---------- access_allowed ----------

def test_access_allowed():
    assert access_allowed(12, 1, False) is True

def test_owner_access_within_limit():
    # is_owner -> True, visitors <= 4 -> True
    assert access_allowed(23, 4, True) is True

def test_owner_access_too_many_visitors():
    # is_owner -> True, visitors <= 4 -> False
    assert access_allowed(12, 5, True) is False

def test_access_before_opening():
    # hour < 6 -> True
    assert access_allowed(5, 1, False) is False

def test_access_after_closing():
    # hour > 22 -> True
    assert access_allowed(23, 1, False) is False

def test_access_at_opening_and_closing_hours():
    # boundaries: hour 6 and hour 22 are allowed
    assert access_allowed(6, 2, False) is True
    assert access_allowed(22, 2, False) is True

def test_access_too_many_visitors():
    # within hours, visitors <= 2 -> False
    assert access_allowed(12, 3, False) is False


# ---------- payment_status ----------

def test_payment_current_no_autopay():
    # is_autopay False -> cutoff 5, has_prior_late False
    assert payment_status(10, False, False) == "current"

def test_payment_current_at_cutoff():
    # days_to_due >= cutoff -> True at the boundary
    assert payment_status(5, False, False) == "current"

def test_payment_current_autopay():
    # is_autopay True -> cutoff 0
    assert payment_status(0, True, False) == "current"

def test_payment_grace_autopay_prior_late():
    # autopay + prior late -> cutoff 10, 0 >= -5 -> grace
    assert payment_status(0, True, True) == "grace"

def test_payment_grace_at_lower_boundary():
    # cutoff 5, days = -10 == cutoff - 15 -> grace
    assert payment_status(-10, False, False) == "grace"

def test_payment_lien():
    # cutoff 5, -20 < -10 -> lien
    assert payment_status(-20, False, False) == "lien"

def test_payment_lien_just_below_grace():
    # no autopay + prior late -> cutoff 15, grace from 0, -1 -> lien
    assert payment_status(-1, False, True) == "lien"
