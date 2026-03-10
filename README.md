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
| **`btcdeb`** *(optional)* | Debugger for raw transaction scripts | [github.com/bitcoin-core/btcdeb](https://github.com/bitcoin-core/btcdeb) |

---

## 🚀 How to Run

### 1. Configure Bitcoin Core

Copy the provided `bitcoin.conf` to your Bitcoin data directory:

| OS | Default Data Directory |
|----|----------------------|
| **Windows** | `%APPDATA%\Bitcoin\` |
| **Linux** | `~/.bitcoin/` |
| **macOS** | `~/Library/Application Support/Bitcoin/` |

The configuration file contents:

```ini
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
```

> **Note:** The `rpcuser` and `rpcpassword` in `bitcoin.conf` must match the values in `bitcoin_lab.py` (default: `admin` / `admin`). You can change them, but make sure both files stay in sync.

### 2. Start the Bitcoin Regtest Node

```bash
bitcoind -regtest
```

Wait a few seconds until the node is fully started. You can verify it's running with:

```bash
bitcoin-cli -regtest getblockchaininfo
```

### 3. Install Python Dependencies

```bash
pip install python-bitcoinrpc
```

### 4. Run the Lab Script

```bash
python bitcoin_lab.py
```

You should see output for each stage — wallet creation, mining, legacy transactions, SegWit transactions, and the saved hex files.

### 5. Analyze Transactions with `btcdeb`

After running the script, use the exported hex files for deeper analysis:

```bash
btcdeb --tx=$(cat legacy.hex)
btcdeb --tx=$(cat segwit.hex)
```

This lets you step through the script execution and inspect opcodes, stack operations, and witness data.

---

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

