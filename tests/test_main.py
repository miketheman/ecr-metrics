from ecr_metrics.main import cli


def test_cli(monkeypatch):
    monkeypatch.setattr("ecr_metrics.main.cli", lambda x: None)

    assert cli() is None
