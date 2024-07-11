x = int(input("N: "))
y = x-1

arr = [[1 for i in range(x)] for j in range(x)]
for i in range(1,x):
	for j in range(i,x):
		arr[i][j] = arr[j][i] = (arr[i-1][j] + arr[i][j-1])

for i in range(x):
	print(" "*y, end="")
	y-=1
	for j in range(i+1):
		if j != 0:
			print(" ", end="")
		print(arr[i-j][j], end="")
	print()
