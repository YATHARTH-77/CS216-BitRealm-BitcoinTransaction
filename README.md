# CS216 – Bitcoin Transaction Lab 🪙

> **Course:** CS216 – Introduction to Blockchains   
> **Team Name:** BitRealm

A hands-on lab exploring **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** Bitcoin transactions on a local **regtest** network. The project creates, signs, broadcasts, and decodes raw transactions to compare the two formats — highlighting differences in transaction size, virtual size, and script structure.

---

## 👥 Team Members

| S.No. | Name                    | Roll Number |
|:-----:|-------------------------|:-----------:|
| 1     | Yatharth Maurya         |  240001082  |
| 2     | Adharsh Gopalakrishnan  |  240002004  |
| 3     | Aditya Rai              |  240041002  |
| 4     | Harshitkumar Singh      |  240002027  |

---

## 📌 Project Overview

Bitcoin supports multiple address/script types. This project demonstrates two of them end-to-end on a local **regtest** blockchain:

| Part | Transaction Type | Address Type | Key Idea |
|------|-----------------|--------------|----------|
| **1** | Legacy | P2PKH (`legacy`) | Signature is embedded **inside** the transaction (`scriptSig`), contributing to total size. |
| **2** | SegWit | P2SH-P2WPKH (`p2sh-segwit`) | Witness data (signatures) is moved **outside** the main transaction body, reducing virtual size (`vsize`). |

### What the Script Does

1. **Wallet Setup** — Creates (or loads) a wallet named `lab_wallet`.
2. **Mining** — Mines 101 blocks so the coinbase reward becomes spendable.
3. **Legacy Transactions (Part 1)**
   - Generates three legacy addresses: **A**, **B**, **C**.
   - Funds address **A** with 1 BTC.
   - Creates & broadcasts **Tx 1: A → B** (0.999 BTC).
   - Creates & broadcasts **Tx 2: B → C** (0.998 BTC).
   - Prints transaction `size` and `vsize` for comparison.
4. **SegWit Transactions (Part 2)**
   - Generates three SegWit addresses: **A'**, **B'**, **C'**.
   - Funds address **A'** with 1 BTC.
   - Creates & broadcasts **Tx 3: A' → B'** (0.999 BTC).
   - Creates & broadcasts **Tx 4: B' → C'** (0.998 BTC).
   - Prints transaction `size` and `vsize` for comparison.
5. **Hex Export** — Saves raw signed transaction hexes to `legacy.hex` and `segwit.hex` for further analysis with `btcdeb`.

---

## ⚙️ Prerequisites

| Dependency | Purpose | Install |
|------------|---------|---------|
| **Bitcoin Core (`bitcoind`)** | Local regtest node | [bitcoin.org/en/download](https://bitcoin.org/en/download) |
| **Python 3.8+** | Script runtime | [python.org](https://www.python.org/downloads/) |
| **`python-bitcoinlib` / `python-bitcoinrpc`** | JSON-RPC client for `bitcoind` | `pip install python-bitcoinrpc` |
| **`btcdeb`** | Debugger for raw transaction scripts | [github.com/bitcoin-core/btcdeb](https://github.com/bitcoin-core/btcdeb) |

---

---

```markdown
## 🚀 How to Run (WSL / Linux Environment)

This project requires a Linux environment (such as WSL or Ubuntu) to properly support the Bitcoin daemon and to compile and run the `btcdeb` low-level script debugger. 

### Prerequisites

Ensure you have Bitcoin Core (v28.1+) installed and the `btcdeb` debugger compiled in your home directory (`~/btcdeb/btcdeb`). You also need Python 3 and a few dependencies:

```bash
sudo apt update
sudo apt install python3-pip jq -y
pip3 install python-bitcoinrpc --break-system-packages

```

---

### Step 1: Configure the Local Bitcoin Node

The Python script requires a local Regtest node. Regtest is a local testing environment where we can instantly mine blocks and generate fake bitcoins for testing without spending real money.

Create the Bitcoin data directory and set up the configuration file:

```bash
mkdir -p ~/.bitcoin
cat << 'EOF' > ~/.bitcoin/bitcoin.conf
# --- Global Settings ---
regtest=1
server=1

[regtest]
rpcuser=admin
rpcpassword=admin
rpcallowip=127.0.0.1
rpcport=18443

paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
EOF

```

---

### Step 2: Start the Regtest Node

Launch the Bitcoin daemon in the background. This starts the blockchain engine, initializes the wallet database, and allows our Python script to communicate with it via RPC.

```bash
bitcoind -regtest -daemon

```

> **Note:** Wait about 5-10 seconds for the node to fully wake up. You can verify it is running by checking the block count: `bitcoin-cli -regtest getblockchaininfo`.

---

### Step 3: Run the Automated Lab Script

Navigate to the project directory where the Python script is located, and execute it. This script handles the wallet funding and generates the transaction chains (A → B → C).

```bash
# Navigate to the project directory
cd "/mnt/c/Users/YATHARTH MAURYA/Desktop/4th SEM/BLOCKCHAIN/CS216-BitRealm-BitcoinTransaction"

# Run the script
python3 bitcoin_lab.py

```

**What this script does:**

1. Mines 101 blocks to fund a local testing wallet.
2. Generates a **Legacy (P2PKH)** transaction chain.
3. Generates a **SegWit (P2SH-P2WPKH)** transaction chain.
4. Outputs the generated Addresses, Transaction IDs (TXIDs), and calculates the Virtual Size (vSize) differences.

> ⚠️ **Keep the terminal output open!** You will need the specific Addresses and TXIDs printed by the script for the debugging phase.

---

### Step 4: Low-Level Script Analysis with `btcdeb`

To prove the execution logic of the transactions, we must extract the **Locking Script** (The Puzzle) and **Unlocking Data** (The Keys) directly from the node and manually push them to the debugger stack.

*(Note: Replace the placeholder variables below with the actual data printed from Step 3).*

#### Part A: Debugging the Legacy Transaction (P2PKH)

1. **Extract the Puzzle (`scriptPubKey`):**
```bash
bitcoin-cli -regtest getaddressinfo <PASTE_ADDRESS_B_HERE>

```


*Copy the `hex` string from the `scriptPubKey` field (typically starts with `76a914...`).*
2. **Extract the Keys (`scriptSig`):**
```bash
bitcoin-cli -regtest gettransaction <PASTE_TXID_B_TO_C_HERE> true

```


*Look in the `vin` array for `scriptSig.asm`. Copy the two long hex strings separated by a space (The Signature and the Public Key).*
3. **Run the Debugger:**
Navigate to the `btcdeb` folder and pass the three strings as arguments to pre-load the stack:
```bash
cd ~/btcdeb
./btcdeb [Paste_Puzzle_Hex] [Paste_Signature_Hex] [Paste_PubKey_Hex]

```


*Type `step` in the debugger to watch the `OP_DUP`, `OP_HASH160`, `OP_EQUALVERIFY`, and `OP_CHECKSIG` execution flow.*

#### Part B: Debugging the SegWit Transaction (P2SH-P2WPKH)

1. **Extract the Witness Program:**
```bash
bitcoin-cli -regtest getaddressinfo <PASTE_SEGWIT_ADDRESS_B_HERE>

```


*Copy the **inner** `scriptPubKey` hex from the `embedded` section (starts with `0014...`).*
2. **Extract the Witness Data:**
```bash
bitcoin-cli -regtest gettransaction <PASTE_SEGWIT_TXID_B_TO_C_HERE> true

```


*Scroll to the `txinwitness` array. It contains two strings: the Witness Signature and Witness Public Key. Copy both.*
3. **Run the Debugger:**
```bash
./btcdeb [Paste_Witness_Program_Hex] [Paste_Witness_Sig] [Paste_Witness_PubKey]

```


*Type `step` to validate the SegWit execution. Notice how the logic is deferred to the SegWit version byte (`OP_0`) rather than executing explicit heavy opcodes on the main stack, proving why SegWit transactions are cheaper and smaller in vSize.*

---

### Step 5: Cleanup

Once the stack analysis is complete and your screenshots are captured, safely shut down the local Bitcoin node to prevent database corruption.

```bash
bitcoin-cli -regtest stop

```




## 📁 Project Structure

```
CS216-BitRealm-BitcoinTransaction/
├── bitcoin.conf       # Bitcoin Core configuration for regtest
├── bitcoin_lab.py     # Main lab script (Legacy + SegWit transactions)
└── README.md          # This file
```

**Generated at runtime:**

```
├── legacy.hex         # Raw hex of a signed Legacy transaction
└── segwit.hex         # Raw hex of a signed SegWit transaction
```

---

## 🔍 Key Observations

| Metric | Legacy (P2PKH) | SegWit (P2SH-P2WPKH) |
|--------|:--------------:|:---------------------:|
| **Size** | 191 bytes | 215 bytes |
| **Virtual Size (vsize)** | 191 vbytes | 134 vbytes |

- **SegWit transactions** have a smaller **virtual size** because witness data is discounted (counted at ¼ weight).
- This means SegWit transactions pay **lower fees** for the same logical operation, making them more economical.

---

