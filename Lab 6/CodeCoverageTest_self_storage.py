import pytest
from self_storage import rent_due, access_allowed, payment_status

# Test cases chosen so that every line (statement) of self_storage.py is executed.


# ---------- rent_due ----------

def test_within_deposit_months():
    # extra <= 0 -> no rent due
    assert rent_due("small", 1, False, False) == 0

def test_unknown_unit_size():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("tiny", 3, False, False)

def test_negative_months():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)

def test_member_non_climate_short_stay():
    # medium: covered 2 + 1 (member) = 3, extra = 2, rate = 80
    assert rent_due("medium", 5, False, True) == 160

def test_climate_long_stay_discount():
    # small: covered 1, extra = 9 (> 6), rate = 120 - 10 - 5 = 105
    assert rent_due("small", 10, True, False) == 945


# ---------- access_allowed ----------

def test_access_allowed():
    assert access_allowed(12, 1, False) is True

def test_owner_access():
    # owner ignores the hour restriction
    assert access_allowed(23, 3, True) is True

def test_access_outside_hours():
    assert access_allowed(3, 1, False) is False


# ---------- payment_status ----------

def test_payment_current():
    # no autopay -> cutoff 5, 10 >= 5
    assert payment_status(10, False, False) == "current"

def test_payment_grace_autopay_prior_late():
    # autopay -> cutoff 0, prior late -> cutoff 10, 0 >= 10 - 15
    assert payment_status(0, True, True) == "grace"

def test_payment_lien():
    # cutoff 5, -20 < 5 - 15
    assert payment_status(-20, False, False) == "lien"
