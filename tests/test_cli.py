import argparse
import json
import sys
from types import SimpleNamespace

import pytest

import rofinder


def make_args(**overrides):
    defaults = {
        "full": False,
        "sections": None,
        "avatar": False,
        "friends": False,
        "games": False,
        "detailed": False,
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_parse_sections_rejects_unknown_sections():
    with pytest.raises(argparse.ArgumentTypeError, match="unknown section"):
        rofinder.parse_sections(make_args(sections="profile,wat"))


def test_parse_sections_accepts_aliases_and_trims_tokens():
    sections = rofinder.parse_sections(make_args(sections=" profile, games "))

    assert sections == {"profile", "favorites"}


@pytest.mark.parametrize("value", ["0", "-1", "not-a-number"])
def test_positive_int_rejects_invalid_limits(value):
    with pytest.raises(argparse.ArgumentTypeError):
        rofinder.positive_int(value)


def test_json_mode_does_not_use_rich_progress(monkeypatch, capsys):
    class FakeAPI:
        def __init__(self, api_domain):
            self.api_domain = api_domain

        def resolve_user(self, user):
            assert user == "roblox"
            return 1, {
                "id": 1,
                "name": "Roblox",
                "displayName": "Roblox",
                "created": "2006-02-27T21:06:40.3Z",
                "isBanned": False,
            }

    class ExplodingProgress:
        def __init__(self, *args, **kwargs):
            raise AssertionError("JSON mode should not create Rich progress UI")

    monkeypatch.setattr(rofinder, "RobloxAPI", FakeAPI)
    monkeypatch.setattr(rofinder, "Progress", ExplodingProgress)
    monkeypatch.setattr(sys, "argv", ["rofinder.py", "roblox", "--sections", "profile", "--json"])

    rofinder.main()

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["profile"]["name"] == "Roblox"
    assert output.strip().startswith("{")
