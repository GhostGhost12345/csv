import pytest
from main import apply_filter, apply_aggregate

rows = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]

def test_apply_filter_gt():
    filtered = apply_filter(rows, "price>500")
    prices = [row["price"] for row in filtered]
    assert prices == ["999", "1199"]

def test_apply_filter_eq():
    filtered = apply_filter(rows, "brand=apple")
    names = [row["name"] for row in filtered]
    assert names == ["iphone 15 pro"]

def test_apply_filter_lt():
    filtered = apply_filter(rows, "rating<4.7")
    names = [row["name"] for row in filtered]
    assert names == ["redmi note 12", "poco x5 pro"]

def test_apply_aggregate_avg():
    result = apply_aggregate(rows, "price=avg")
    assert "avg(price)" in result
    # Среднее: (999+1199+199+299)/4 = 674
    assert abs(result["avg(price)"] - 674) < 0.001

def test_apply_aggregate_min():
    result = apply_aggregate(rows, "rating=min")
    assert "min(rating)" in result
    assert abs(result["min(rating)"] - 4.4) < 0.001

def test_apply_aggregate_max():
    result = apply_aggregate(rows, "price=max")
    assert "max(price)" in result
    assert abs(result["max(price)"] - 1199) < 0.001

def test_apply_filter_invalid_condition():
    import pytest
    with pytest.raises(ValueError):
        apply_filter(rows, "price>>100")

def test_apply_aggregate_invalid_func():
    import pytest
    with pytest.raises(ValueError):
        apply_aggregate(rows, "price=median")

