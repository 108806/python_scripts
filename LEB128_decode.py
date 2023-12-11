import sys, os

print(os.getcwd(), sys.executable)


def LEB128_decode(bstr: bytes) -> int:
    """
    # Example bytestring fb41e495b705f17b15b6e4edafa3cc67
    fb 41
    e4 95 b7 05
    f1 7b
    15
    b6 e4 ed af a3 cc 67

    # Basic pattern for convertign any base:
    0xfb + 0x41 * 128 + 0x00 * 128**2 + 0x00 * 128**3 + 0x00 * 128**4 + 0x00 * 128**5 + 0x00
    0xe4 + 0x95 * 128 + 0xb7 * 128**2 + 0x05 * 128**3 + 0x00 * 128**4 + 0x00 * 128**5 + 0x00
    0xf1 + 0x7b * 128 + 0x00 * 128**2 + 0x00 * 128**3 + 0x00 * 128**4 + 0x00 * 128**5 + 0x00
    0x15 + 0x00 * 128 + 0x00 * 128**2 + 0x00 * 128**3 + 0x00 * 128**4 + 0x00 * 128**5 + 0x00
    0xb6 + 0xe4 * 128 + 0xed * 128**2 + 0xaf * 128**3 + 0xa3 * 128**4 + 0xcc * 128**5 + 0x67
    CAN REVERSE ENDIANESS BY REVERSING POWERS!

    # 8443 + 11389668 + 15857 + 21 + 455619626365494 = 455619637779483

    # BIT MASKING TO GET RID OF THE UPPER BIT:
    X -> Y
    0 -> 8
    1 -> 9
    2 -> A
    3 -> B
    4 -> C
    5 -> D
    6 -> E
    7 -> F
    X ^F Y
    In [23]: hex(0xe4 & 127)
    Out[23]: '0x64'
    """

    print("x:", x, ":", x.hex())
    nums, binary = [], ""
    for i in bstr:
        b = f"{bin(i)[2:]:>08}"
        print(
            b,
            hex(int(b, 2)),
            hex(int(b, 2) & 127),
            int(b[1:], 2) * [128 ** (len(binary) // 7 or 0)][0],
        )
        nums.append(int(b[1:], 2) * [128 ** (len(binary) // 7 or 0)][0])
        if b[0] == "1":
            binary += b[1:]
        else:
            binary += b[1:]
            binary = ""
    print(nums)
    return sum(nums)


x = b"\xfb\x41\xe4\x95\xb7\x05\xf1\x7b\x15\xb6\xe4\xed\xaf\xa3\xcc\x67"
print(LEB128_decode(x))


#	sanity check:
someleb128 = ("00000110", "11111100", "10100110")[::-1]
print(
    "\nCorrect result:",  # 114214
    sum(
        int(someleb128[y][1:], 2) * (128**y if y > 0 else 1)
        for y in range(len(someleb128))
    ),
)
L128hex = "".join(
    f"{hex(int(someleb128[x], 2))[2:]:>02}" for x in range(len(someleb128))
)
L128bytes = bytes.fromhex(L128hex)
print(LEB128_decode(L128bytes))  # 455619637779483

