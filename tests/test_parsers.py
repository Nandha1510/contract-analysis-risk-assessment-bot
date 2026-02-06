from contract_parser.parsers import parse_txt


def test_parse_txt_simple():
    class Dummy:
        def __init__(self, b):
            self._b = b
        def read(self):
            return self._b

    sample = "Hello\nThis is a test contract."
    f = Dummy(sample.encode("utf-8"))
    out = parse_txt(f)
    assert "test contract" in out
