"""
Tests for the three FitFindr tools.

Each tool has at least one test for its normal path and one for its failure
mode:
    search_listings  -> no listings found returns []
    suggest_outfit   -> empty wardrobe still returns advice (no crash)
    create_fit_card  -> empty/incomplete outfit returns a message (no crash)

The suggest_outfit / create_fit_card happy-path tests call the Groq LLM and
need a valid GROQ_API_KEY in .env. The failure-mode tests for those tools are
deterministic and do not hit the network.

Run with:  pytest tests/
"""

from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


# ── Tool 1: search_listings ─────────────────────────────────────────────────

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    # Failure mode: nothing matches -> empty list, no exception.
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []


def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)


def test_search_size_filter_token_match():
    # "M" should match a listing sized "S/M" (token-aware, case-insensitive).
    results = search_listings("tee", size="M", max_price=None)
    assert all("m" in item["size"].lower() for item in results)


# ── Tool 2: suggest_outfit ──────────────────────────────────────────────────

def test_suggest_outfit_with_wardrobe():
    item = search_listings("vintage graphic tee", size=None, max_price=50)[0]
    out = suggest_outfit(item, get_example_wardrobe())
    assert isinstance(out, str)
    assert len(out.strip()) > 0


def test_suggest_outfit_empty_wardrobe():
    # Failure mode: empty wardrobe -> still returns non-empty advice, no crash.
    item = search_listings("vintage graphic tee", size=None, max_price=50)[0]
    out = suggest_outfit(item, get_empty_wardrobe())
    assert isinstance(out, str)
    assert len(out.strip()) > 0


def test_suggest_outfit_missing_items_key():
    # Failure mode: wardrobe dict has no 'items' key -> no crash.
    item = search_listings("vintage graphic tee", size=None, max_price=50)[0]
    out = suggest_outfit(item, {})
    assert isinstance(out, str)
    assert len(out.strip()) > 0


# ── Tool 3: create_fit_card ─────────────────────────────────────────────────

def test_create_fit_card_with_outfit():
    item = {"title": "Y2K Baby Tee", "price": 18.0, "platform": "depop",
            "style_tags": ["y2k", "vintage"]}
    outfit = "Pair the tee with baggy jeans and chunky sneakers."
    card = create_fit_card(outfit, item)
    assert isinstance(card, str)
    assert len(card.strip()) > 0


def test_create_fit_card_empty_outfit():
    # Failure mode: empty outfit -> descriptive message string, no exception.
    item = {"title": "Y2K Baby Tee", "price": 18.0, "platform": "depop",
            "style_tags": ["y2k", "vintage"]}
    card = create_fit_card("", item)
    assert isinstance(card, str)
    assert "Couldn't generate a fit card" in card


def test_create_fit_card_whitespace_outfit():
    # Failure mode: whitespace-only outfit treated the same as empty.
    item = {"title": "Y2K Baby Tee", "price": 18.0, "platform": "depop",
            "style_tags": ["y2k"]}
    card = create_fit_card("   ", item)
    assert isinstance(card, str)
    assert "Couldn't generate a fit card" in card
