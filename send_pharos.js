// send_pharos.js
const { JsonRpcProvider, Wallet, parseEther } = require("ethers");

// Ambil argumen CLI
const to = process.argv[2];
const amountInput = process.argv[3];
const privateKey = process.env.PRIVATE_KEY;

// RPC Pharos testnet
const provider = new JsonRpcProvider("https://api.zan.top/node/v1/pharos/testnet/7bbf30cd3a774b4ebbd9750aa6204994");

// Inisialisasi wallet
const wallet = new Wallet(privateKey, provider);

async function main() {
  if (!to || !amountInput) {
    console.error("❌ Usage: node send_pharos.js <toAddress> <amount>");
    process.exit(1);
  }

  console.log("====================================");
  console.log("🔑 Sender :", wallet.address);
  console.log("📬 Receiver:", to);
  console.log("💰 Amount :", amountInput, "PHRS");
  console.log("====================================");

  const amount = parseEther(amountInput);

  const tx = {
    to: to,
    value: amount,
    gasLimit: 21000,
  };

  console.log("🚀 Sending transaction...");
  const sentTx = await wallet.sendTransaction(tx);
  console.log("⏳ Tx hash:", sentTx.hash);

  const receipt = await sentTx.wait();
  console.log("✅ Confirmed in block:", receipt.blockNumber);
}

main().catch((err) => {
  console.error("❌ Error:", err);
});
