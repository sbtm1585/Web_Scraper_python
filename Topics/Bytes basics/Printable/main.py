code_point = int(input())
print(chr(code_point) if code_point in range(32, 127) else False)