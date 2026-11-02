"""Unit tests using only synthetic, redistributable datasets."""
import csv
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from candleaudit.cli import main
from candleaudit.core import InputError, audit_candles, audit_features, audit_trades, instant, interval_seconds

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


class CandleAuditTests(unittest.TestCase):
    def _temp_csv(self, header, records):
        self.addCleanup(lambda: None)
        t = tempfile.NamedTemporaryFile(mode="w", newline="", suffix=".csv", delete=False, encoding="utf-8")
        self.addCleanup(lambda: Path(t.name).unlink(missing_ok=True))
        writer = csv.writer(t)
        writer.writerow(header)
        writer.writerows(records)
        t.close()
        return Path(t.name)

    def test_clean_candles(self):
        result = audit_candles(EXAMPLES / "candles_clean.csv")
        self.assertTrue(result.as_dict()["ok"])
        self.assertEqual(result.rows, 4)

    def test_bad_candles(self):
        codes = {i.code for i in audit_candles(EXAMPLES / "candles_bad.csv").issues}
        self.assertTrue({"GAP", "INVALID_OHLC", "DUPLICATE"}.issubset(codes))

    def test_negative_volume(self):
        f = self._temp_csv(["timestamp", "symbol", "open", "high", "low", "close", "volume"],
                            [["2026-01-01T00:00:00Z", "S", 1, 2, 1, 2, -1]])
        self.assertIn("NEGATIVE_VOLUME", {i.code for i in audit_candles(f).issues})

    def test_duplicate_headers_rejected(self):
        f = self._temp_csv(["timestamp", "symbol", "symbol", "open", "high", "low", "close", "volume"], [])
        with self.assertRaisesRegex(InputError, "duplicate header"):
            audit_candles(f)

    def test_missing_columns(self):
        f = self._temp_csv(["timestamp", "symbol"], [["2026-01-01T00:00:00Z", "S"]])
        with self.assertRaises(InputError):
            audit_candles(f)

    def test_misaligned_candle(self):
        f = self._temp_csv(["timestamp", "symbol", "open", "high", "low", "close", "volume"],
                            [["2026-01-01T01:00:00Z", "S", 1, 2, 1, 2, 3]])
        self.assertIn("MISALIGNED_OPEN", {i.code for i in audit_candles(f).issues})

    def test_out_of_order(self):
        f = self._temp_csv(["timestamp", "symbol", "open", "high", "low", "close", "volume"],
                            [["2026-01-01T04:00:00Z", "S", 1, 2, 1, 2, 3],
                             ["2026-01-01T00:00:00Z", "S", 1, 2, 1, 2, 3]])
        self.assertIn("OUT_OF_ORDER", {i.code for i in audit_candles(f).issues})

    def test_irregular_step(self):
        f = self._temp_csv(["timestamp", "symbol", "open", "high", "low", "close", "volume"],
                            [["2026-01-01T00:00:00Z", "S", 1, 2, 1, 2, 3],
                             ["2026-01-01T05:00:00Z", "S", 1, 2, 1, 2, 3]])
        self.assertIn("IRREGULAR_STEP", {i.code for i in audit_candles(f).issues})

    def test_utc_required(self):
        with self.assertRaises(InputError):
            instant("2026-01-01T00:00:00")
        self.assertEqual(instant("2026-01-01T01:00:00+01:00"), datetime(2026, 1, 1, tzinfo=timezone.utc))

    def test_unix_millis(self):
        self.assertEqual(instant("1767225600000"), datetime(2026, 1, 1, tzinfo=timezone.utc))

    def test_intervals(self):
        self.assertEqual(interval_seconds("4h"), 14400)
        self.assertEqual(interval_seconds("15m"), 900)
        with self.assertRaises(InputError):
            interval_seconds("0h")

    def test_feature_leakage(self):
        self.assertFalse(audit_features(EXAMPLES / "features_bad.csv").as_dict()["ok"])
        self.assertTrue(audit_features(EXAMPLES / "features_clean.csv").as_dict()["ok"])

    def test_bad_feature_timestamp(self):
        f = self._temp_csv(["symbol", "feature", "signal_time", "available_at"],
                            [["S", "X", "invalid", "2026-01-01T00:00:00Z"]])
        self.assertIn("BAD_TIMESTAMP", {i.code for i in audit_features(f).issues})

    def test_trade_pnl_and_fees(self):
        r = audit_trades(EXAMPLES / "trades_clean.csv", EXAMPLES / "candles_clean.csv")
        self.assertTrue(r.as_dict()["ok"])
        self.assertEqual(r.metrics["trades_priced"], 1)
        self.assertEqual(r.metrics["fees"], "0.106")
        self.assertEqual(r.metrics["net_pnl"], "3.894")

    def test_trade_leakage(self):
        f = self._temp_csv(["symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"],
                           [["EXAMPLEUSDT", "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z", "100", "LONG", "2026-01-01T08:00:00Z", "106", "1"]])
        codes = {i.code for i in audit_trades(f, EXAMPLES / "candles_clean.csv").issues}
        self.assertIn("ENTRY_NOT_NEXT_BAR", codes)

    def test_missing_trade_bar(self):
        f = self._temp_csv(["symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"],
                           [["MISS", "2026-01-01T00:00:00Z", "2026-01-01T04:00:00Z", "100", "LONG", "2026-01-01T08:00:00Z", "106", "1"]])
        self.assertIn("ENTRY_BAR_MISSING", {i.code for i in audit_trades(f, EXAMPLES / "candles_clean.csv").issues})

    def test_cli_codes(self):
        import contextlib
        import io
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["candles", str(EXAMPLES / "candles_clean.csv")]), 0)
            self.assertEqual(main(["candles", str(EXAMPLES / "candles_bad.csv")]), 1)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["candles", "/missing/path.csv"]), 2)

    def test_invalid_trade_is_excluded_from_pnl(self):
        f = self._temp_csv(
            ["symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"],
            [["EXAMPLEUSDT", "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z", 100, "LONG", "2026-01-01T08:00:00Z", 200, 1]],
        )
        result = audit_trades(f, EXAMPLES / "candles_clean.csv")
        self.assertEqual(result.metrics["trades_priced"], 0)
        self.assertEqual(result.metrics["trades_excluded"], 1)
        self.assertEqual(result.metrics["net_pnl"], "0")

    def test_empty_csv_is_not_reported_clean(self):
        f = self._temp_csv(["timestamp", "symbol", "open", "high", "low", "close", "volume"], [])
        with self.assertRaisesRegex(InputError, "no data"):
            audit_candles(f)

    def test_missing_signal_bar_excludes_trade(self):
        f = self._temp_csv(
            ["symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"],
            [["EXAMPLEUSDT", "2025-12-31T20:00:00Z", "2026-01-01T00:00:00Z", 100, "LONG", "2026-01-01T08:00:00Z", 105, 1]],
        )
        result = audit_trades(f, EXAMPLES / "candles_clean.csv")
        self.assertIn("SIGNAL_BAR_MISSING", {i.code for i in result.issues})
        self.assertEqual(result.metrics["trades_priced"], 0)

    def test_empty_feature_file_is_invalid(self):
        f = self._temp_csv(["symbol", "feature", "signal_time", "available_at"], [])
        with self.assertRaisesRegex(InputError, "no data"):
            audit_features(f)

    def test_empty_trades_file_is_invalid(self):
        f = self._temp_csv(
            ["symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"], [],
        )
        with self.assertRaisesRegex(InputError, "no data"):
            audit_trades(f, EXAMPLES / "candles_clean.csv")

    def test_no_external_data(self):
        self.assertTrue((EXAMPLES / "candles_clean.csv").is_file())


if __name__ == "__main__":
    unittest.main()
