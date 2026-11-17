from hypothesis import given, strategies as st
from self_storage import parse_rental, duration_average, payable_rent


@given(st.text() | st.none())
def test_parse_rental_no_crash(s):
    try:
        parse_rental(s)
    except Exception as e:
        assert False, f"parse_rental crashed with: {e!r}"


@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_rent_no_crash(s):
    try:
        payable_rent(s)
    except Exception as e:
        assert False, f"payable_rent crashed with: {e!r}"
