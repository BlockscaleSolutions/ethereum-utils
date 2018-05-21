from sha3 import keccak_256
import time


class Blockchain:
    """
    Dummy blockchain sample to simulate the mining process.
    No peers, consensus rules, transactions, etc. just basic block creation.
    """

    def __init__(self, genesis_block):
        self.DESIRED_BLOCK_TIME = 3     # simplified target, feel free to adjust
        self.chain = []                 # our blockchain, initially an empty list
        self.block_time_sum = 0         # utilized to compute an ongoing average block time
        self.mine_block(genesis_block)  # start mining on top of the genesis block

    def mine_block(self, latest_block):
        self.chain.append(latest_block)

        if len(self.chain) > 1:
            # Require the time it took to find the previous block to determine difficulty adjustment
            block_time = latest_block['timestamp'] - self.chain[-2]['timestamp']
            self.block_time_sum += block_time

            print('Latest block time:', block_time)
            print('Latest difficulty:', latest_block['difficulty'])

            # simplification of adjustment but will adjust based on variance from desired block time
            adjustment_factor = block_time / self.DESIRED_BLOCK_TIME

            # some thresholds to ensure adjustment is not too significant
            # increasing if block time < desired and decreasing if block time > desired
            if adjustment_factor < 0.85:
                adjustment_factor = 0.85

            elif adjustment_factor > 1.15:
                adjustment_factor = 1.15

            # adjust the difficulty for the next block to target the desired block time
            difficulty = latest_block['difficulty'] / adjustment_factor

        else:
            difficulty = latest_block['difficulty']

        # target value for the next block based on the new difficulty
        target = 2**256 // difficulty
        prev_block_hash = keccak_256(str(latest_block).encode()).hexdigest()

        print('Next block difficulty:', difficulty)
        # Pad the number to 32 bytes, 64 hex, withe leading 0x
        print('Next block target:', '{0:#0{1}x}'.format(int(target), 66))
        print('*' * 100)

        print('\n\nBlockchain length:', len(self.chain))
        print('Average block time:', self.block_time_sum / len(self.chain))

        # Mining! Randomly guessing numbers(nonces)
        for i in range(100000000):
            # generate the hash of the nonce and previous block hash and see if you have found the nonce
            hashed_value = keccak_256(bytes(i) + prev_block_hash.encode()).digest()
            int_hash = int.from_bytes(hashed_value, byteorder='big')  # convert to int to compare against target

            # Proof of work found, now mine on top of this block
            if int_hash <= target:
                print('\n\n')
                print('*' * 100)
                print('Block found! The Proof of Work is:', i)

                self.mine_block({
                    'difficulty': difficulty,
                    'timestamp': time.time(),
                    'parent': prev_block_hash
                })


if __name__ == '__main__':
    Blockchain({
        'difficulty': 25000,
        'timestamp': time.time()
    })
