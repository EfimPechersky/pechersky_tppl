import pytest
from notation import ChangeNotation, ExpressionException

@pytest.fixture
def RightExpressions():
    return "/ + 3  10 * + 2 3 - 3 5", "  3 "
class TestNotation:

    def test_right_expressions(self, RightExpressions):
        re1, re2 = RightExpressions

        assert ChangeNotation(re1) == "3 / 10 + 2 * 3 + 3 - 5"
        assert ChangeNotation(re2) == "3"

    @pytest.mark.parametrize(
        "wrong_exp,exc",
        [("w - 13 4 55", pytest.raises(ExpressionException)),
         ("+- 2 * 2 - 2 1", pytest.raises(ExpressionException)),
         ("+ + 10 20",pytest.raises(ExpressionException)),
         ("/ 5 3 10 * + 2 3 - 3 5",pytest.raises(ExpressionException)),
         ("",pytest.raises(ExpressionException)) ,
         ("   ",pytest.raises(ExpressionException))
        ])
    def test_wrong_expressions(self, wrong_exp,exc):
        with exc:
            assert ChangeNotation(wrong_exp)
            
        
