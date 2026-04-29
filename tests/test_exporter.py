from exporter import RoFinderExporter


def sample_data():
    return {
        "profile": {
            "id": 1,
            "name": "Roblox",
            "displayName": "Roblox",
            "created": "2006-02-27T21:06:40.3Z",
            "isBanned": False,
        },
        "stats": {"friends": 1, "followers": 2, "following": 3},
        "status": {"presence": {"userPresenceType": 0}, "premium": False},
        "avatar_url": "https://example.com/avatar.png",
        "friends_list": [{"id": 156, "name": "builderman", "displayName": "builderman"}],
    }


def test_txt_export_creates_parent_directories_and_includes_friends(tmp_path):
    exporter = RoFinderExporter()
    report_path = tmp_path / "reports" / "roblox-report"

    saved_path = exporter.export_txt(sample_data(), report_path)

    text = (tmp_path / "reports" / "roblox-report.txt").read_text(encoding="utf-8")
    assert saved_path.endswith("roblox-report.txt")
    assert "builderman" in text
    assert "FRIENDS" in text


def test_md_export_includes_friends(tmp_path):
    exporter = RoFinderExporter()
    report_path = tmp_path / "roblox-report"

    exporter.export_md(sample_data(), report_path)

    text = (tmp_path / "roblox-report.md").read_text(encoding="utf-8")
    assert "## Friends" in text
    assert "builderman" in text
