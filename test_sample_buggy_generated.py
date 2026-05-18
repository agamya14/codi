import pytest
from sample_buggy import append_item, count_positive

def test_append_item_edge_case():
    assert append_item(None, None) is not None


def test_count_positive_edge_case():
    assert count_positive(None) is not None


