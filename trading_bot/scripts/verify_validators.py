import sys
from pathlib import Path

# Add project root to sys.path to allow imports from bot package
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.exceptions import (
    InvalidSymbolError,
    InvalidSideError,
    InvalidOrderTypeError,
    InvalidQuantityError,
    InvalidPriceError,
)


def run_tests() -> None:
    passed = 0
    failed = 0

    def assert_valid(func, val, expected, test_name):
        nonlocal passed, failed
        try:
            res = func(val)
            if res == expected:
                print(f"[PASS] {test_name}: Input {repr(val)} -> {repr(res)}")
                passed += 1
            else:
                print(f"[FAIL] {test_name}: Expected {repr(expected)}, got {repr(res)}")
                failed += 1
        except Exception as e:
            print(f"[FAIL] {test_name}: Raised unexpected exception {type(e).__name__}: {e}")
            failed += 1

    def assert_invalid(func, val, expected_exception, test_name, **kwargs):
        nonlocal passed, failed
        try:
            res = func(val, **kwargs)
            print(f"[FAIL] {test_name}: Expected {expected_exception.__name__}, but returned {repr(res)}")
            failed += 1
        except expected_exception as e:
            print(f"[PASS] {test_name}: Correctly raised {expected_exception.__name__} for {repr(val)}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {test_name}: Raised {type(e).__name__} instead of {expected_exception.__name__}")
            failed += 1

    print("--- Running Validator Tests ---")

    # 1. validate_symbol tests
    assert_valid(validate_symbol, "btcusdt", "BTCUSDT", "validate_symbol basic")
    assert_valid(validate_symbol, "  EthUsdt  ", "ETHUSDT", "validate_symbol strip and upper")
    assert_invalid(validate_symbol, None, InvalidSymbolError, "validate_symbol None")
    assert_invalid(validate_symbol, "", InvalidSymbolError, "validate_symbol empty string")
    assert_invalid(validate_symbol, "   ", InvalidSymbolError, "validate_symbol whitespace string")
    assert_invalid(validate_symbol, "BTC_USDT", InvalidSymbolError, "validate_symbol with underscore")
    assert_invalid(validate_symbol, "BTC-USDT", InvalidSymbolError, "validate_symbol with hyphen")
    assert_invalid(validate_symbol, "A", InvalidSymbolError, "validate_symbol too short")
    assert_invalid(validate_symbol, "BTCUSDTBTCUSDTBTCUSDT", InvalidSymbolError, "validate_symbol too long")

    # 2. validate_side tests
    assert_valid(validate_side, "buy", "BUY", "validate_side lowercase")
    assert_valid(validate_side, "  SELL  ", "SELL", "validate_side uppercase and whitespace")
    assert_invalid(validate_side, None, InvalidSideError, "validate_side None")
    assert_invalid(validate_side, "HOLD", InvalidSideError, "validate_side invalid side")
    assert_invalid(validate_side, "", InvalidSideError, "validate_side empty string")

    # 3. validate_order_type tests
    assert_valid(validate_order_type, "limit", "LIMIT", "validate_order_type lowercase")
    assert_valid(validate_order_type, "  MARKET  ", "MARKET", "validate_order_type uppercase and whitespace")
    assert_invalid(validate_order_type, None, InvalidOrderTypeError, "validate_order_type None")
    assert_invalid(validate_order_type, "STOP_LOSS", InvalidOrderTypeError, "validate_order_type invalid type")

    # 4. validate_quantity tests
    assert_valid(validate_quantity, 10, 10.0, "validate_quantity integer")
    assert_valid(validate_quantity, "0.001", 0.001, "validate_quantity float string")
    assert_invalid(validate_quantity, None, InvalidQuantityError, "validate_quantity None")
    assert_invalid(validate_quantity, 0, InvalidQuantityError, "validate_quantity zero boundary")
    assert_invalid(validate_quantity, -1.5, InvalidQuantityError, "validate_quantity negative")
    assert_invalid(validate_quantity, "abc", InvalidQuantityError, "validate_quantity non-numeric string")

    # 5. validate_price tests
    try:
        res = validate_price(None, required=False)
        if res is None:
            print("[PASS] validate_price Not Required: None input -> None")
            passed += 1
        else:
            print(f"[FAIL] validate_price Not Required: Expected None, got {repr(res)}")
            failed += 1
    except Exception as e:
        print(f"[FAIL] validate_price Not Required: Raised unexpected exception {type(e).__name__}: {e}")
        failed += 1

    try:
        res = validate_price("  ", required=False)
        if res is None:
            print("[PASS] validate_price Not Required: whitespace input -> None")
            passed += 1
        else:
            print(f"[FAIL] validate_price Not Required: Expected None, got {repr(res)}")
            failed += 1
    except Exception as e:
        print(f"[FAIL] validate_price Not Required: Raised unexpected exception {type(e).__name__}: {e}")
        failed += 1

    assert_valid(lambda p: validate_price(p, required=False), "1500.5", 1500.5, "validate_price Not Required but provided")
    assert_invalid(validate_price, None, InvalidPriceError, "validate_price Required but None", required=True)
    assert_invalid(validate_price, "  ", InvalidPriceError, "validate_price Required but whitespace", required=True)
    assert_invalid(validate_price, 0, InvalidPriceError, "validate_price zero boundary", required=True)
    assert_invalid(validate_price, -50.0, InvalidPriceError, "validate_price negative", required=True)
    assert_invalid(validate_price, "xyz", InvalidPriceError, "validate_price non-numeric string", required=True)

    print("\n--- Summary ---")
    print(f"Total Tests Passed: {passed}")
    print(f"Total Tests Failed: {failed}")
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
