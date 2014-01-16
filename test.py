a = ''
a += 'zab'
a += 'eel'
print a

def concatinate(data1 , data2):
	temp = data1 << 8
	final = temp | data2
	return final

for i in range (0,10):
	print i

print concatinate(0x01, 0x02)
