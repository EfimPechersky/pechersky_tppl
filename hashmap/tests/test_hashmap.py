import pytest
from hashmap import HashMap

@pytest.fixture
def hashmap():
    return HashMap()

class TestHashMap:


    @pytest.mark.parametrize(
        "index, value",
        [(0, 10),
         (2, 300),
         (5,200),
         (8,3)])
    def test_iloc(self,hashmap, index, value):
        hashmap["value1"] = 1
        hashmap["value2"] = 2
        hashmap["value3"] = 3
        hashmap["1"] = 10
        hashmap["2"] = 20
        hashmap["3"] = 30
        hashmap["1, 5"] = 100
        hashmap["5, 5"] = 200
        hashmap["10, 5"] = 300
        assert hashmap.iloc(index)==value
    
    @pytest.mark.parametrize(
        "cond, value",
        [(">=1", {1:10, 2:20, 3:30}),
         ("=1", {1:10}),
         ("<>2", {1:10, 3:30}),
         ("<3", {1:10, 2:20}),
         (">0, >0", {(1,5):100, (5,5):200, (10,5):300}),
         (">=10, >0", {(10,5):300}),
         ("<5, >=5, >=3", {(1,5,3):400}),
         ("<=5, >=5, >=3", {(1,5,3):400, (5,5,4):500}),
         ('', {1:10,2:20,3:30}),
         (',,', {(1,5,3):400,(5,5,4):500, (10,5,5):600})])
    def test_ploc(self,hashmap,cond, value):
        hashmap["value1"] = 1
        hashmap["value2"] = 2
        hashmap["value3"] = 3
        hashmap["1"] = 10
        hashmap["2"] = 20
        hashmap["3"] = 30
        hashmap["(1, 5)"] = 100
        hashmap["(5, 5)"] = 200
        hashmap["(10, 5)"] = 300
        hashmap["(1, 5, 3)"] = 400
        hashmap["(5, 5, 4)"] = 500
        hashmap["(10, 5, 5)"] = 600
        assert hashmap.ploc(cond)==value

    @pytest.mark.parametrize(
        "cond, exception",
        [(">>2,=1", pytest.raises(SyntaxError)),
         ("<=>1", pytest.raises(SyntaxError)),
         ("1,2", pytest.raises(SyntaxError)),
         (">.1", pytest.raises(SyntaxError))])
    def test_exceptions(self,hashmap,cond, exception):
        hashmap["1,2"]=100
        with exception:
            assert hashmap.ploc(cond)
