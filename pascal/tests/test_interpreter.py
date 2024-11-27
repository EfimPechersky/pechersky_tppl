import pytest
from interpreter import Interpreter

@pytest.fixture
def interpreter():
    return Interpreter()

class TestInterpreter:

    def test_complex_statement(self,interpreter):
        assert interpreter.eval("BEGIN\nEND.") == {}
    
    def test_assign(self, interpreter):
        assert interpreter.eval("BEGIN\n x:=10\n END.")=={'x':10}
        assert interpreter.eval("BEGIN\n x:=10;\n y:=20\n END.")=={'x':10, 'y':20}

    @pytest.mark.parametrize(
        "complex_statement, vars",
        [("BEGIN\n x:=+10 + 2 - 10\n END.", {'x':2}),
         ("BEGIN\n x:=10 * 2 / 10\n END.", {'x':2}),
         ("BEGIN\n x:=10 - 2 * 10\n END.",{'x':-10}),
         ("BEGIN\n x:=(10 - 2) * 10\n END.",{'x':80}),
         ("BEGIN\n x:=(-10 + 2 * 3) * 10\n END.",{'x':-40})])
    def test_math_ops(self,complex_statement, vars, interpreter):
        assert interpreter.eval(complex_statement)==vars
    
    @pytest.mark.parametrize(
        "complex_statement, vars",
        [("BEGIN\n x:=10;\n y:=x;\n END.", {'x':10, 'y':10}),
         ("BEGIN\n x:=10;\n y:=x*2;\n END.",{'x':10, 'y':20}),
         ("BEGIN\n x:=10;\n x:=x*2;\n END.",{'x':20}),
         ("BEGIN\n x:=10;\n y:=x-8;\n z:=x * y - y;\n END.",{'x':10, 'y':2, 'z':18})])
    def test_vars(self,complex_statement, vars, interpreter):
        assert interpreter.eval(complex_statement)==vars
    
    @pytest.mark.parametrize(
        "complex_statement, vars",
        [("BEGIN\nBEGIN\n \n END;\n END.", {}),
         ("BEGIN\n x:=10; \nBEGIN\n \n END;\n END.",{'x':10}),
         ("BEGIN\n \nBEGIN\n x:=20 \n END;\n END.",{'x':20}),
         ("BEGIN\n x:=10; \nBEGIN\n y:=10+x \n END;\n END.",{'x':10, 'y':20})])
    def test_complex_in_complex(self,complex_statement, vars, interpreter):
        assert interpreter.eval(complex_statement)==vars

    @pytest.mark.parametrize(
        "complex_statement, exc",
        [("BEGIN\n x:=\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n x:=10\n y:=10\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n x:=*10\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n 10*10\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n x:=y+10\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n x:=10@2\n END.",pytest.raises(SyntaxError)),
         ("BEGIN\n x:=10",pytest.raises(SyntaxError)),
         ("BEGIN\n x:10;",pytest.raises(SyntaxError))])
    def test_exceptions(self,complex_statement, exc, interpreter):
        with exc:
            assert interpreter.eval(complex_statement)

    
