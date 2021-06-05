"""
x86 2-level page table
4k mem pages

32 bits entries
31-22 page directory index
21-12: page table index
12-2: ignore
1: read/write
0: in memory
"""


def put(x, *args):
    print(f'{x:08x}', *args)


pba = (1 << 32) - (1 << 12)  # phys base addr
pd = 0x000e7200              # page dir
vm = {
    # dir
    0x000e7200: 0x0600056f,
    0x000e7204: 0x002000b7,
    0x000e7208: 0x1f00005f,
    0x000e720c: 0x00200961,
    # table 0
    0x06000000: 0x01000729,
    # table 2
    0x1f000000: 0x189aac7d,
    0x1f000004: 0x023fdb95,
    0x1f000008: 0x0b4f30e7,
}

addr = 0x008016b3

pdi = addr >> 22            # page dir idx
pti = (addr >> 12) & 0x3ff  # page tab idx

print(pdi, pti)

pda = pd + pdi * 4
put(pda, 'page dir addr')
pde = vm[pda]
pta = (pde & pba) + pti * 4
put(pta, 'page tab addr')
pte = vm[pta]
pa = (pte & pba) + (addr & 0xfff)
put(pa, 'phys addr')
print('in mem' if pte & 1 else 'not in mem')
print('read/write' if pte & 2 else 'read only')
