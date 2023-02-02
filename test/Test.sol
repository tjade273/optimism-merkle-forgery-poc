pragma solidity 0.8.14;

import "../src/Lib_RLPReader.sol";
import "../src/Lib_MerkleTrie.sol";
import "../src/Lib_BytesUtils.sol";
import "forge-std/console.sol";

contract Test{
    bytes constant key = hex"0000000000000000000000000000000000000000000000000000000000000000";
    bytes32 constant root = 0x3c88fcfaefa2e96e5192a9ec39e1ec17c71f7b6194875879754a545ac12cb0d7;
    function testProofDivergence() public pure {
        bytes memory proof1 = hex"f8a4b844f842a01000000000000000000000000000000000000000000000000000000000000000a028456157f0fb83de685c3bac05f3a363bc2d9a367596d6001e8b42106f37c892b83bf839a0de209cd2f1897ee75b1a9bc61c5d2e25f1a5580ecb23c598894e64683e833200c82086666f6f626172808080808080808080808080808080a0df209d000000000000000000000000000000000000000000516b758b00000000";
        bytes memory proof2 = hex"f8a3b844f842a01000000000000000000000000000000000000000000000000000000000000000a028456157f0fb83de685c3bac05f3a363bc2d9a367596d6001e8b42106f37c892b83bf839a0de209cd2f1897ee75b1a9bc61c5d2e25f1a5580ecb23c598894e64683e833200c82086666f6f6261728080808080808080808080808080809fde209cd2f1897ee75b1a9bc61c5d2e25f1a5580ecb23c598894e64683e8332";
        (bool exists1, bytes memory value1) = Lib_MerkleTrie.get(key, proof1, root);
        require(exists1, "Proof 1 proved exclusion");
        (bool exists2, bytes memory value2) = Lib_MerkleTrie.get(key, proof2, root);
        require(exists2, "Proof 2 proved exclusion");

        assert(!Lib_BytesUtils.equal(value1, value2));
    }
}
