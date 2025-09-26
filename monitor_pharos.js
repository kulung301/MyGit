// file: monitor_pharos_rpc.js
const { ethers } = require("ethers");

// RPC Pharos testnet
const RPC = "https://api.zan.top/node/v1/pharos/testnet/7bbf30cd3a774b4ebbd9750aa6204994";

// Address wallet valid
const ADDRESS = "0xdf712323c4b7c67aa3517baa9c1e4c8a924a86cd";

// Jumlah block terakhir untuk dicek
const BLOCK_SCAN = 200; // scan 200 block terakhir

async function getLastTransactions(provider, address, limit = 5) {
  const currentBlock = await provider.getBlockNumber();
  const transactions = [];

  for (let i = currentBlock; i > currentBlock - BLOCK_SCAN && transactions.length < limit; i--) {
    // ethers.js v6: getBlock(blockNumber, includeTransactions)
    const block = await provider.getBlock(i, true);
    if (!block || !block.transactions) continue;

    for (const tx of block.transactions) {
      if (!tx) continue;

      const fromMatch = tx.from && tx.from.toLowerCase() === address.toLowerCase();
      const toMatch = tx.to && tx.to.toLowerCase() === address.toLowerCase();

      if (fromMatch || toMatch) {
        transactions.push(tx);
        if (transactions.length >= limit) break;
      }
    }
  }

  return transactions;
}

async function main() {
  try {
    const provider = new ethers.JsonRpcProvider(RPC);
    const walletAddress = ethers.getAddress(ADDRESS);

    // Ambil balance, tx count, latest block
    const [balance, txCount, blockNumber] = await Promise.all([
      provider.getBalance(walletAddress),
      provider.getTransactionCount(walletAddress),
      provider.getBlockNumber(),
    ]);

    console.log("====================================");
    console.log("🔎 Network latest block:", blockNumber);
    console.log("📬 Address:", walletAddress);
    console.log("💰 Balance:", ethers.formatEther(balance), "PHRS");
    console.log("🔢 Nonce / tx count:", txCount);
    console.log("====================================");

    // Ambil 5 transaksi terakhir langsung dari RPC
    const lastTxs = await getLastTransactions(provider, walletAddress, 5);
    console.log("📜 5 Transaksi Terakhir:");
    if (lastTxs.length === 0) console.log("  (Belum ada transaksi)");
    else {
      lastTxs.forEach((tx, i) => {
        const valueEther = ethers.formatEther(tx.value);
        console.log(
          `${i + 1}. Hash: ${tx.hash}, From: ${tx.from || "(unknown)"}, To: ${tx.to || "(contract creation)"}, Value: ${valueEther} PHRS`
        );
      });
    }
    console.log("====================================");
  } catch (err) {
    console.error("⚠️ Error:", err.message || err);
  }
}

main();
