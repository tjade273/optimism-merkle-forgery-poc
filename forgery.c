#include "keccak256.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>


#define NODE_LEN 32

int check_candidate(unsigned char *candidate, SHA3_CTX *ctx, unsigned char *hash) {
    keccak_init(ctx);
    keccak_update(ctx, candidate, NODE_LEN);
    keccak_final(ctx, hash);
    return (
        hash[0] == 0xde &&
        hash[1] == 0x20 &&
        hash[2] == 0x9c &&
        hash[31] == 0
    );
}

void *thread(void *nonce) {
    unsigned char candidate[NODE_LEN] = "\xdf \x9d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00";
    SHA3_CTX ctx;
    unsigned char hash[32];
    ((uint64_t*)candidate)[1] = (uint64_t) nonce;
    while (!check_candidate(candidate, &ctx, hash)) {
        ((uint64_t*)candidate)[3]++;
        if ((uint64_t) nonce == 0){
            if ((((uint64_t*)candidate)[3] & 0xffffff) == 0) {
                printf("Checked %08llx\n", ((uint64_t*)candidate)[3]);
            }
        }
    }
    printf("Found candidate: ");
    for (unsigned int i = 0; i < 32; i++) {
        printf("%02x", candidate[i]);
    }
    printf("\nHash: ");
    for (unsigned int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n"); 
    exit(0);
    return NULL;
}

int main(int argc, char **argv){
    uint64_t nthreads = 1;
    if (argc > 1) {
        nthreads = atoll(argv[1]);
    }

    pthread_t threads[nthreads];
    for (uint64_t i = 0; i < nthreads; i++) {
        pthread_create(&threads[i], NULL, thread, (void*) i);
    }
    for (uint64_t i = 0; i < nthreads; i++) {
        pthread_join(threads[i], NULL);
    }
}