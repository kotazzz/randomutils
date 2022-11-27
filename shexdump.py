
def hexdump(data: bytes):
    print(f'       {"  ".join([hex(x)[2:] for x in range(16)])}')
    for i in range(0, len(data), 16):
        s = data[i:i+16]
        hexa = ' '.join(["%02X" % x for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        print(f"{i:04x}  {hexa:<48} {text}")

hexdump(b'Hello, a;lkdfpghoerigworld!')