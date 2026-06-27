```python id="p3w8jr"
import json
import secrets
from datetime import datetime
from pathlib import Path

from eth_account import Account
from web3 import Web3

RPC_ENDPOINT = "https://rpc.example.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"

direct_swaps = "direct swaps"
routes = "routes"
bridge_transactions = "bridge transactions"

client = Web3(
    Web3.HTTPProvider(RPC_ENDPOINT)
)

account = Account.from_key(
    PRIVATE_KEY
)

TARGET_ADDRESS = (
    "0x0000000000000000000000000000000000000000"
)

session_id = secrets.token_hex(5)

notes = [
    direct_swaps,
    routes,
    bridge_transactions,
]


def network_ready():
    return client.is_connected()


def next_nonce():
    return client.eth.get_transaction_count(
        account.address
    )


def estimate():
    return {
        "gas": 126500,
        "price": client.to_wei(
            "4",
            "gwei"
        ),
    }


def create_payload():
    values = estimate()

    payload = {}

    payload["from"] = account.address
    payload["to"] = TARGET_ADDRESS
    payload["value"] = 0
    payload["nonce"] = next_nonce()
    payload["gas"] = values["gas"]
    payload["gasPrice"] = values["price"]
    payload["chainId"] = 1

    return payload


def export_file(content):
    location = Path(
        "interaction_data.json"
    )

    location.write_text(
        json.dumps(
            content,
            indent=2
        )
    )


def display_header():
    print("Session:", session_id)

    print(
        "Created:",
        datetime.utcnow().isoformat()
    )


def display_notes():
    for item in notes:
        print(item)


def display_transaction(tx):
    print(
        "Nonce:",
        tx["nonce"]
    )

    print(
        "Gas:",
        tx["gas"]
    )


def sign(tx):
    result = account.sign_transaction(
        tx
    )

    return result.raw_transaction.hex()


def main():
    display_header()

    tx = create_payload()

    encoded = sign(tx)

    output = {
        "session": session_id,
        "wallet": account.address,
        "connected": network_ready(),
        "raw": encoded,
    }

    export_file(output)

    display_notes()

    display_transaction(tx)

    print(
        "Wallet:",
        account.address
    )

    print(
        "Connection:",
        network_ready()
    )

    print(
        "Characters:",
        len(encoded)
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            "Execution error:",
            error
        )

print("record saved")
print("process finished")
```
