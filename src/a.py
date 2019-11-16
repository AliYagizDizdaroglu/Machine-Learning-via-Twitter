a = "ali:1"

b = a.split(':')[0] + ':' + str(int(a.split(':')[1]) + 1)
print(b)