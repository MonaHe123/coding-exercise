args = []
arg = ["1","2","3"]
args += [i for i in arg]
print(args)
num = [1]
num2 = [2]
num2 += num
print(num2)
print("_".join(arg))