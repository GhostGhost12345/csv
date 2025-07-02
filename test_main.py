import pytest
import sys
from main import apply_filter, apply_aggregate, load_csv, print_table, main


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
    with pytest.raises(ValueError):
        apply_filter(rows, "price>>100")


def test_apply_aggregate_invalid_func():
    with pytest.raises(ValueError):
        apply_aggregate(rows, "price=median")


def test_load_csv(tmp_path):
    csv_content = "name,price\nitem1,100\nitem2,200\n"
    file = tmp_path / "test.csv"
    file.write_text(csv_content)

    loaded = load_csv(str(file))
    assert len(loaded) == 2
    assert loaded[0]["name"] == "item1"
    assert loaded[1]["price"] == "200"


def test_print_table(capsys):
    data = [{"col1": "a", "col2": "b"}, {"col1": "c", "col2": "d"}]
    print_table(data)
    captured = capsys.readouterr()
    assert "col1" in captured.out
    assert "col2" in captured.out
    assert "a" in captured.out
    assert "d" in captured.out


def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit):
        main()


def test_main_print_all(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,price\nitem1,100\nitem2,200\n")
    monkeypatch.setattr(sys, "argv", ["main.py", str(csv_file)])
    main()
    out = capsys.readouterr().out
    assert "item1" in out and "item2" in out


def test_main_filter(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,price\nitem1,600\nitem2,400\n")
    monkeypatch.setattr(sys, "argv", ["main.py", str(csv_file), "--where", "price>500"])
    main()
    out = capsys.readouterr().out
    assert "item1" in out and "item2" not in out


def test_main_aggregate(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,price\nitem1,100\nitem2,300\n")
    monkeypatch.setattr(sys, "argv", ["main.py", str(csv_file), "--aggregate", "price=avg"])
    main()
    out = capsys.readouterr().out
    assert "avg(price)" in out and "200.0" in out


def test_main_filter_bad_condition(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,price\nitem1,100\n")
    monkeypatch.setattr(sys, "argv", ["main.py", str(csv_file), "--where", "price>>10"])
    main()
    out = capsys.readouterr().out
    assert "Filter error" in out


def test_main_aggregate_bad_func(tmp_path, monkeypatch, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,price\nitem1,100\n")
    monkeypatch.setattr(sys, "argv", ["main.py", str(csv_file), "--aggregate", "price=median"])
    main()
    out = capsys.readouterr().out
    assert "Aggregate error" in out

