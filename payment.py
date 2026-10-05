import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Konfigurasi Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token Bot Payment Anda (Ganti jika tokennya berbeda)
TOKEN_BOT_PAYMENT = "8785832887:AAG0YdSgCFHkHuAuGmGxa-QkTjVZ3gjDRvw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    
    if args:
        produk_id = args[0]
        
        # Menyesuaikan informasi produk berdasarkan parameter dari deep link
        if "hijab" in produk_id:
            nama_produk = "Koleksi Eksklusif Suka Hijab"
            harga = "Rp 50.000"
        elif "indo" in produk_id:
            nama_produk = "Koleksi Bocil"
            harga = "Rp 50.000"
        else:
            nama_produk = "Paket Spesial random"
            harga = "Rp 50.000"
            
        teks_tagihan = f"""🛒 **DETAIL PESANAN ANDA**

📦 Produk: {nama_produk}
🆔 ID Pesanan: `{produk_id}`
💰 Total Harga: **{harga}**

📲 Silakan scan QRIS di atas menggunakan aplikasi m-banking atau e-wallet (DANA, OVO, GoPay, BCA, dll) Anda untuk melakukan pembayaran. 

⚠️ Setelah membayar, mohon kirimkan bukti transfer ke Admin untuk verifikasi."""

        # Mengirim gambar QRIS beserta teks tagihan
        try:
            with open("qris.jpg", "rb") as foto_qris:
                await update.message.reply_photo(
                    photo=foto_qris,
                    caption=teks_tagihan,
                    parse_mode="Markdown"
                )
        except FileNotFoundError:
            # Cadangan jika file qris.jpg belum dimasukkan ke folder
            await update.message.reply_text(
                f"{teks_tagihan}\n\n*(Catatan: File gambar qris.jpg belum ditemukan di folder bot)*", 
                parse_mode="Markdown"
            )
            
    else:
        await update.message.reply_text("Halo! Bot ini digunakan untuk memproses pembayaran. Silakan pilih produk melalui grup preview terlebih dahulu.")

def main():
    app = ApplicationBuilder().token(TOKEN_BOT_PAYMENT).build()
    
    # Menangkap perintah /start beserta parameter produk
    app.add_handler(CommandHandler("start", start))

    print("Bot Payment sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
