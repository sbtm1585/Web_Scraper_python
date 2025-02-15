encoded = input()
key = int(input())
key_bytes = key.to_bytes(2, 'big')
sum_key_bytes = sum(key_bytes)

decoded = ''.join([chr(ord(ch) + sum_key_bytes) for ch in encoded])

print(decoded)