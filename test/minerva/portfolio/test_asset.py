from minerva.portfolio.asset import Asset
import pytest


def test_asset():
    with pytest.raises(NotImplementedError):
        Asset()
