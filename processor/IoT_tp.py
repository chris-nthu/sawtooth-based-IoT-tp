from sawtooth_sdk.processor.core import TransactionProcessor
from tpLib.IoT_handler import IoT_TransactionHandler

VALIDATOR_ADDRESS = 'tcp://127.0.0.1:4004'

def main():
    # In docker, the url would be the validator's container name with
    # port 4004
    processor = TransactionProcessor(url=VALIDATOR_ADDRESS)

    handler = IoT_TransactionHandler()

    processor.add_handler(handler)

    print('Starting IoT transaction processor')
    print('Connecting to sawtooth validator at ' + VALIDATOR_ADDRESS)

    processor.start()

if __name__ == "__main__":
    main()
