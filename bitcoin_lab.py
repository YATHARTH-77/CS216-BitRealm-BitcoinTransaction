from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time
import os

# --- CONFIGURATION ---
RPC_USER = 'admin'
RPC_PASSWORD = 'admin'
RPC_HOST = '127.0.0.1'
RPC_PORT = '18443'

def get_rpc():
    # Connects to the server we just started
    return AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}")

def print_section(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")

def run_lab():
    print("Connecting to local Bitcoin node...")
    rpc = get_rpc()
    
    # 1. SETUP WALLET
    wallet_name = "lab_wallet"
    try:
        # Try to load it first to avoid errors if you run script twice
        rpc.loadwallet(wallet_name)
        print(f"[+] Wallet '{wallet_name}' loaded.")
    except:
        try:
            rpc.createwallet(wallet_name)
            print(f"[+] Wallet '{wallet_name}' created.")
        except JSONRPCException as e:
             print(f"[!] Wallet info: {e}")

    # 2. GENERATE COINS (We need 101 blocks to make coins spendable)
    print("Mining blocks to fund wallet... (this may take a second)")
    miner_addr = rpc.getnewaddress()
    rpc.generatetoaddress(101, miner_addr)
    print("[+] Wallet funded.")

    # =================================================================
    # PART 1: LEGACY TRANSACTIONS (P2PKH)
    # =================================================================
    print_section("PART 1: LEGACY TRANSACTIONS (P2PKH)")

    # A. Generate Addresses
    addr_A = rpc.getnewaddress("Address_A", "legacy")
    addr_B = rpc.getnewaddress("Address_B", "legacy")
    addr_C = rpc.getnewaddress("Address_C", "legacy")
    print(f"Address A: {addr_A}\nAddress B: {addr_B}\nAddress C: {addr_C}")

    # B. Fund Address A
    txid_fund = rpc.sendtoaddress(addr_A, 1.0)
    rpc.generatetoaddress(1, miner_addr) # Confirm it
    print(f"[+] Funded A. TXID: {txid_fund}")

    # --- Transaction 1: A -> B ---
    print("\n[STEP] Creating Tx 1: A -> B")
    utxo_A = rpc.listunspent(1, 9999999, [addr_A])[0]
    
    inputs = [{"txid": utxo_A['txid'], "vout": utxo_A['vout']}]
    outputs = {addr_B: 0.999} 
    
    raw_tx_1 = rpc.createrawtransaction(inputs, outputs)
    signed_tx_1 = rpc.signrawtransactionwithwallet(raw_tx_1)
    txid_1 = rpc.sendrawtransaction(signed_tx_1['hex'])
    print(f"--> Broadcasted Tx 1 (A->B): {txid_1}")
    rpc.generatetoaddress(1, miner_addr) # Confirm it

    # Analyze Tx 1
    decoded_1 = rpc.decoderawtransaction(signed_tx_1['hex'])
    print(f"    Size: {decoded_1['size']} bytes | VSize: {decoded_1['vsize']} vbytes")

    # --- Transaction 2: B -> C ---
    print("\n[STEP] Creating Tx 2: B -> C")
    utxo_B = rpc.listunspent(1, 9999999, [addr_B])[0]
    
    inputs_2 = [{"txid": utxo_B['txid'], "vout": utxo_B['vout']}]
    outputs_2 = {addr_C: 0.998}
    
    raw_tx_2 = rpc.createrawtransaction(inputs_2, outputs_2)
    signed_tx_2 = rpc.signrawtransactionwithwallet(raw_tx_2)
    txid_2 = rpc.sendrawtransaction(signed_tx_2['hex'])
    print(f"--> Broadcasted Tx 2 (B->C): {txid_2}")
    rpc.generatetoaddress(1, miner_addr)

    # =================================================================
    # PART 2: SEGWIT TRANSACTIONS (P2SH-P2WPKH)
    # =================================================================
    print_section("PART 2: SEGWIT TRANSACTIONS (P2SH-P2WPKH)")

    # A. Generate Addresses (Note: p2sh-segwit)
    addr_As = rpc.getnewaddress("Address_As", "p2sh-segwit")
    addr_Bs = rpc.getnewaddress("Address_Bs", "p2sh-segwit")
    addr_Cs = rpc.getnewaddress("Address_Cs", "p2sh-segwit")
    print(f"Address A' (SegWit): {addr_As}\nAddress B' (SegWit): {addr_Bs}")

    # B. Fund A'
    rpc.sendtoaddress(addr_As, 1.0)
    rpc.generatetoaddress(1, miner_addr)

    # --- Transaction 3: A' -> B' ---
    print("\n[STEP] Creating Tx 3: A' -> B'")
    utxo_As = rpc.listunspent(1, 9999999, [addr_As])[0]
    inputs_s1 = [{"txid": utxo_As['txid'], "vout": utxo_As['vout']}]
    outputs_s1 = {addr_Bs: 0.999}
    
    raw_tx_s1 = rpc.createrawtransaction(inputs_s1, outputs_s1)
    signed_tx_s1 = rpc.signrawtransactionwithwallet(raw_tx_s1)
    txid_s1 = rpc.sendrawtransaction(signed_tx_s1['hex'])
    print(f"--> Broadcasted Tx 3 (A'->B'): {txid_s1}")
    rpc.generatetoaddress(1, miner_addr)

    decoded_s1 = rpc.decoderawtransaction(signed_tx_s1['hex'])
    print(f"    Size: {decoded_s1['size']} bytes | VSize: {decoded_s1['vsize']} vbytes")

    # --- Transaction 4: B' -> C' ---
    print("\n[STEP] Creating Tx 4: B' -> C'")
    utxo_Bs = rpc.listunspent(1, 9999999, [addr_Bs])[0]
    inputs_s2 = [{"txid": utxo_Bs['txid'], "vout": utxo_Bs['vout']}]
    outputs_s2 = {addr_Cs: 0.998}
    
    raw_tx_s2 = rpc.createrawtransaction(inputs_s2, outputs_s2)
    signed_tx_s2 = rpc.signrawtransactionwithwallet(raw_tx_s2)
    txid_s2 = rpc.sendrawtransaction(signed_tx_s2['hex'])
    print(f"--> Broadcasted Tx 4 (B'->C'): {txid_s2}")
    
    # Save files for Debugging (Part of assignment requirement)
    with open("legacy.hex", "w") as f: f.write(signed_tx_1['hex'])
    with open("segwit.hex", "w") as f: f.write(signed_tx_s1['hex'])
    print("\n[SUCCESS] Raw transaction hexes saved to 'legacy.hex' and 'segwit.hex'")
    print("Use these files with 'btcdeb' for your report screenshots.")

if __name__ == "__main__":
    run_lab()