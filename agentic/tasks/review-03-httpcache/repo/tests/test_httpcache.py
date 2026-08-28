"""Project self-tests. Run with:  python -m unittest discover -s tests -v

These cover the public API with representative inputs. The final grade is
decided by separate hidden tests.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpcache.headers import Headers, parse_list
from httpcache.datefmt import parse_http_date, format_http_date
from httpcache.etags import parse_etag, etag_matches, if_none_match_passes, if_match_passes
from httpcache.freshness import response_age, freshness_lifetime, is_fresh
from httpcache.vary import vary_fields, cache_key_with_vary
from httpcache.conditional import evaluate_conditional
from httpcache.ranges import parse_range_header, ByteRange
from httpcache.content import apply_range, RangeNotSatisfiable
from httpcache.cachekey import request_cache_key
from httpcache.store import ResponseStore


class TestHeaders(unittest.TestCase):
    def test_case_insensitive(self):
        h = Headers([("Content-Type", "text/plain")])
        self.assertEqual(h.get("content-type"), "text/plain")
        self.assertIn("CONTENT-TYPE", h)

    def test_parse_list(self):
        self.assertEqual(parse_list("a, b ,c"), ["a", "b", "c"])
        self.assertEqual(parse_list(None), [])


class TestDate(unittest.TestCase):
    def test_roundtrip(self):
        ts = parse_http_date("Sun, 06 Nov 1994 08:49:37 GMT")
        self.assertEqual(ts, 784111777)
        self.assertEqual(format_http_date(784111777), "Sun, 06 Nov 1994 08:49:37 GMT")

    def test_bad_date(self):
        self.assertIsNone(parse_http_date("not a date"))


class TestEtags(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_etag('W/"abc"'), (True, "abc"))
        self.assertEqual(parse_etag('"xyz"'), (False, "xyz"))

    def test_strong_vs_weak(self):
        self.assertTrue(etag_matches('"a"', '"a"', strong=True))
        self.assertFalse(etag_matches('W/"a"', '"a"', strong=True))
        self.assertTrue(etag_matches('W/"a"', '"a"', strong=False))

    def test_if_none_match(self):
        # current etag listed -> 304 (returns False = do not proceed)
        self.assertFalse(if_none_match_passes('"a", "b"', '"a"'))
        # not listed -> proceed
        self.assertTrue(if_none_match_passes('"c"', '"a"'))
        # star with existing -> 304
        self.assertFalse(if_none_match_passes('*', '"a"'))

    def test_if_match(self):
        self.assertTrue(if_match_passes('"a"', '"a"'))
        self.assertFalse(if_match_passes('"a"', '"b"'))
        self.assertTrue(if_match_passes('*', '"a"'))
        self.assertFalse(if_match_passes('*', None))


class TestFreshness(unittest.TestCase):
    def test_age_and_lifetime(self):
        h = Headers([("Cache-Control", "max-age=60"), ("Age", "10")])
        # age = 10 (Age header) + 5 resident
        self.assertEqual(response_age(h, now=1005, response_time=1000), 15)
        self.assertEqual(freshness_lifetime(h), 60)
        self.assertTrue(is_fresh(h, now=1005, response_time=1000))

    def test_stale(self):
        h = Headers([("Cache-Control", "max-age=5")])
        self.assertFalse(is_fresh(h, now=1010, response_time=1000))


class TestVary(unittest.TestCase):
    def test_key(self):
        resp = Headers([("Vary", "Accept-Encoding")])
        req = Headers([("Accept-Encoding", "gzip")])
        self.assertEqual(cache_key_with_vary("K", req, resp), "K|accept-encoding=gzip")

    def test_star(self):
        resp = Headers([("Vary", "*")])
        self.assertIsNone(cache_key_with_vary("K", Headers(), resp))


class TestConditional(unittest.TestCase):
    def test_none_match_304(self):
        req = Headers([("If-None-Match", '"a"')])
        self.assertEqual(evaluate_conditional(req, '"a"', None), 304)

    def test_match_412(self):
        req = Headers([("If-Match", '"a"')])
        self.assertEqual(evaluate_conditional(req, '"b"', None), 412)

    def test_modified_since(self):
        req = Headers([("If-Modified-Since", "Sun, 06 Nov 1994 08:49:37 GMT")])
        self.assertEqual(evaluate_conditional(req, None, 784111777 - 100), 304)
        self.assertEqual(evaluate_conditional(req, None, 784111777 + 100), 200)


class TestRangesParsing(unittest.TestCase):
    def test_explicit(self):
        r = parse_range_header("bytes=2-5")
        self.assertEqual((r[0].first, r[0].last), (2, 5))

    def test_open_ended(self):
        r = parse_range_header("bytes=8-")
        self.assertEqual((r[0].first, r[0].last), (8, None))

    def test_suffix(self):
        r = parse_range_header("bytes=-3")
        self.assertTrue(r[0].is_suffix())
        self.assertEqual(r[0].suffix_length, 3)

    def test_malformed(self):
        self.assertIsNone(parse_range_header("items=1-2"))
        self.assertIsNone(parse_range_header("bytes=5-2"))
        self.assertIsNone(parse_range_header("bytes=abc"))
        self.assertIsNone(parse_range_header(None))


class TestContentApply(unittest.TestCase):
    BODY = b"0123456789"  # length 10

    def test_explicit_slice(self):
        r = parse_range_header("bytes=2-5")
        self.assertEqual(apply_range(self.BODY, r[0]), b"2345")

    def test_open_ended(self):
        r = parse_range_header("bytes=8-")
        self.assertEqual(apply_range(self.BODY, r[0]), b"89")

    def test_suffix(self):
        r = parse_range_header("bytes=-3")
        self.assertEqual(apply_range(self.BODY, r[0]), b"789")

    def test_end_over_length_is_clamped(self):
        r = parse_range_header("bytes=0-100")
        self.assertEqual(apply_range(self.BODY, r[0]), self.BODY)

    def test_suffix_larger_than_body(self):
        r = parse_range_header("bytes=-50")
        self.assertEqual(apply_range(self.BODY, r[0]), self.BODY)

    def test_empty_body_416(self):
        r = parse_range_header("bytes=0-1")
        with self.assertRaises(RangeNotSatisfiable):
            apply_range(b"", r[0])


class TestCacheKeyStore(unittest.TestCase):
    def test_key_and_store(self):
        key = request_cache_key("GET", "HTTP://Example.com/Path", Headers(), Headers())
        self.assertEqual(key, "GET http://example.com/Path")
        store = ResponseStore()
        self.assertTrue(store.put(key, Headers(), b"x", 0))
        self.assertIsNotNone(store.get(key))
        self.assertEqual(len(store), 1)

    def test_uncacheable_method(self):
        self.assertIsNone(request_cache_key("POST", "http://x/", Headers(), Headers()))


if __name__ == "__main__":
    unittest.main()
