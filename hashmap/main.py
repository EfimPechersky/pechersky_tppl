from hashmap import HashMap

hashmap=HashMap()
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

print(hashmap.ploc(',,'))
print(hashmap.iloc(0))
