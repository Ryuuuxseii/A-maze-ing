

blockk = '\033[91m██\033[00m'
block = '██'
empty = '  '

array = [
    [1,1,1],
    [1,1,2],
    [1,0,1]
]

for line in array:
    for i in line:
        if i == 1:
            print(block, end="")
        elif i == 0:
            print(empty, end="")
        elif i == 2:
            print(blockk, end="")
    print()

