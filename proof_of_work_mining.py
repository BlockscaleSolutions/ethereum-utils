from sha3 import keccak_256
import time


class Blockchain:
    """Dummy blockchain sample to simulate the mining process, no peers."""

    def __init__(self, genesis_block):
        self.DESIRED_BLOCK_TIME = 1  # simplified target
        self.chain = []
        self.mine_block(genesis_block)  # begin mining on top of the genesis

    def mine_block(self, latest_block):
        print('New block found:', latest_block)

        #  append the latest block and begin to mine the next
        self.chain.append(latest_block)

        if len(self.chain) > 1:
            block_time = latest_block['timestamp'] - self.chain[-2]['timestamp']
            print('Block time:', block_time)

            adjustment_factor = block_time / self.DESIRED_BLOCK_TIME

            # Some thresholds to ensure adjustment is not too significant
            if adjustment_factor < 0.85:
                adjustment_factor = 0.85
                difficulty = latest_block['difficulty'] / adjustment_factor

            elif adjustment_factor > 1.15:
                adjustment_factor = 1.15
                difficulty = latest_block['difficulty'] / adjustment_factor

            else:
                difficulty = latest_block['difficulty']

        else:
            difficulty = latest_block['difficulty']

        # Target value for the next block based on the new difficulty
        target = 2**256 // difficulty
        prev_block_hash = keccak_256(str(latest_block).encode()).hexdigest()

        print('New difficulty:', difficulty)
        # Pad the number to 32 bytes, 64 hex, withe leading 0x
        print('New block target:', '{0:#0{1}x}'.format(int(target), 66))

        # Randomly guess numbers
        for i in range(100000000):
            # print('Trying: ', i)

            # Generate the hash and see if you have found the nonce
            hashed_value = keccak_256(bytes(i) + prev_block_hash.encode()).digest()
            int_hash = int.from_bytes(hashed_value, byteorder='big')  # convert to int to compare against target

            # Answer found return the solution
            if int_hash <= target:
                print('\n\nBlock found!! The solution is:', i)
                new_block = {
                    'difficulty': difficulty,
                    'timestamp': time.time()
                }

                self.mine_block(new_block)


if __name__ == '__main__':
    block = {
        'difficulty': 10000,
        'timestamp': time.time()
    }

    Blockchain(block)