TLDR: The Lib_MerkleTrie._walkNodePath function conflates “short” node IDs and “long” nodeIDs in a manner that can lead to a collision and proof forgery when the attacker controls the value of some key “near” the target key.

https://github.com/ethereum-optimism/optimism/blob/eb68ef54a6c76f8aa20de8e2183cac44fb4adaab/packages/contracts/contracts/libraries/trie/Lib_MerkleTrie.sol#L151-L166

https://github.com/ethereum-optimism/optimism/blob/eb68ef54a6c76f8aa20de8e2183cac44fb4adaab/packages/contracts/contracts/libraries/rlp/Lib_RLPReader.sol#L104-L119

It is possible to construct two different RLP items, `r1` and `r2` such that
```
keccak256(rlp.encode(r1)) == bytes32(rlp.encode(r2))
```

with `len(rlp.encode(r1)) >= 32` and `len(rlp.encode(r2)) < 32`.


Note that the cast on the RHS pads the encoding with zeroes.


Thus if `r1` is a node in the true trie, the prover may instead prove the existence of node `r2`, and vice-versa.

An example of such `r1` and `r2` can be found via a small brute force search (implemented in [forgery.c](./forgery.c)):

```
keccak256(rlp.encode(b' ', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Qku\x8b\x00\x00\x00\x00'])) == bytes32(rlp.encode([b' ', b'\xd2\xf1\x89~\xe7[\x1a\x9b\xc6\x1c].%\xf1\xa5X\x0e\xcb#\xc5\x98\x89Ndh>\x832']))
```

This bug is not easily exploitable in tries which use hashes for all keys - in the example above we use a leaf node with empty key - this assumes the parent node is a branch and thus that there is some other key in the tree which matches on all by the last nibble. In general we will either need to find a collision which matches on a much longer prefix, which is impractical for 256-bit hashes. I believe the search complexity for an arbitrary collision is 2^64, and for a targeted collision is 2^128.


FIX:

One easy fix is to compare the hashes of the nodes, rather than the nodes themselves. Because the hash is length-dependent the hash of a <32 byte node will be different from the hash of a 32-byte hash.
Even better, throw a domain separator in there so they are oboviously incapable of colliding.