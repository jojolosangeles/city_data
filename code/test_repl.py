from repl import Repl

def test_constructor():
    r = Repl(True)
    assert r.interactive == True

def test_constructor2():
    r = Repl(False)
    assert r.interactive == False