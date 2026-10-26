import pandas as pd
import re
import html
import os


# =========================================================
# 1. PENGATURAN FILE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File input berada di folder tweets-data
INPUT_FILE = os.path.join(
    BASE_DIR,
    "tweets-data",
    "gabungan_pajak_marketplace_cleaning.csv"
)

# File hasil
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "tweets-data",
    "hasil_pajak_marketplace.csv"
)


# =========================================================
# 2. CEK FILE INPUT
# =========================================================

if not os.path.exists(INPUT_FILE):

    print("ERROR: File input tidak ditemukan!")
    print("\nFile yang dicari:")
    print(INPUT_FILE)

    print("\nFile CSV yang tersedia:")

    tweets_folder = os.path.join(BASE_DIR, "tweets-data")

    if os.path.exists(tweets_folder):

        for file in os.listdir(tweets_folder):

            if file.lower().endswith(".csv"):
                print("-", file)

    else:
        print("Folder tweets-data tidak ditemukan.")

    exit()


# =========================================================
# 3. MEMBACA DATA
# =========================================================

df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8",
    low_memory=False
)

print("\n" + "=" * 70)
print("DATA AWAL")
print("=" * 70)

print("Jumlah baris :", len(df))
print("Jumlah kolom :", len(df.columns))
print("Kolom :", df.columns.tolist())


# =========================================================
# 4. MENENTUKAN KOLOM TEKS
# =========================================================

if "full_text" in df.columns:

    TEXT_COLUMN = "full_text"

elif "text" in df.columns:

    TEXT_COLUMN = "text"

else:

    print("\nERROR: Kolom full_text/text tidak ditemukan.")
    exit()


# =========================================================
# 5. MENGHAPUS DATA KOSONG
# =========================================================

jumlah_awal = len(df)

df = df.dropna(
    subset=[TEXT_COLUMN]
)

df = df[
    df[TEXT_COLUMN]
    .astype(str)
    .str.strip()
    != ""
]

print("\nData kosong dihapus :", jumlah_awal - len(df))


# =========================================================
# 6. MENGHAPUS DUPLIKAT
# =========================================================

jumlah_sebelum_duplikat = len(df)

if "post_id" in df.columns:

    df = df.drop_duplicates(
        subset=["post_id"]
    )

elif "tweet_id" in df.columns:

    df = df.drop_duplicates(
        subset=["tweet_id"]
    )

else:

    df = df.drop_duplicates(
        subset=[TEXT_COLUMN]
    )


print(
    "Data duplikat dihapus :",
    jumlah_sebelum_duplikat - len(df)
)


# =========================================================
# 7. NORMALISASI KATA
# =========================================================

normalisasi = {

    "yg": "yang",
    "yng": "yang",

    "dgn": "dengan",
    "dg": "dengan",

    "utk": "untuk",

    "krn": "karena",
    "krna": "karena",

    "tdk": "tidak",
    "gak": "tidak",
    "ga": "tidak",
    "gk": "tidak",
    "nggak": "tidak",
    "ngga": "tidak",
    "enggak": "tidak",

    "blm": "belum",
    "belom": "belum",

    "udh": "sudah",
    "udah": "sudah",
    "sdh": "sudah",

    "aja": "saja",

    "bgt": "banget",

    "dpt": "dapat",

    "jd": "jadi",

    "jgn": "jangan",

    "klo": "kalau",
    "kalo": "kalau",

    "tp": "tapi",

    "trs": "terus",
    "trus": "terus",

    "dr": "dari",

    "sm": "sama",

    "org": "orang",

    "emg": "memang",
    "emang": "memang",

    "pajakny": "pajak",
    "pajaknya": "pajak",

    "marketplace": "marketplace",
    "ecommerce": "ecommerce",
    "e-commerce": "ecommerce"
}


# =========================================================
# 8. STOPWORDS
# =========================================================

# Kata negasi sengaja TIDAK dimasukkan.
# Contoh:
# tidak, bukan, jangan, belum

stopwords = {

    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "ini",
    "itu",
    "untuk",
    "dengan",
    "pada",
    "atau",
    "juga",
    "akan",
    "ada",
    "dalam",
    "telah",
    "sudah",
    "bagi",
    "oleh",
    "sebagai",
    "karena",
    "agar",
    "jadi",
    "saat",
    "lebih",
    "sangat",
    "bisa",
    "dapat",
    "mau",
    "saja",
    "nya",
    "lah",
    "pun",
    "kah",

    "the",
    "a",
    "an",
    "of",
    "to",
    "in",
    "on",
    "is",
    "are",
    "was",
    "were",
    "and",
    "or"
}


# =========================================================
# 9. FUNGSI CLEANING
# =========================================================

def clean_text(text):

    text = str(text)

    # -----------------------------------------
    # HTML entity
    # -----------------------------------------

    text = html.unescape(text)

    # -----------------------------------------
    # Lowercase
    # -----------------------------------------

    text = text.lower()

    # -----------------------------------------
    # URL
    # -----------------------------------------

    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )

    # -----------------------------------------
    # Email
    # -----------------------------------------

    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # -----------------------------------------
    # Mention
    # -----------------------------------------

    text = re.sub(
        r"@\w+",
        " ",
        text
    )

    # -----------------------------------------
    # Hashtag
    # #pajakmarketplace
    # menjadi pajakmarketplace
    # -----------------------------------------

    text = re.sub(
        r"#",
        "",
        text
    )

    # -----------------------------------------
    # Emoji
    # -----------------------------------------

    text = re.sub(
        r"[\U00010000-\U0010ffff]",
        " ",
        text
    )

    # -----------------------------------------
    # Angka
    # -----------------------------------------

    text = re.sub(
        r"\d+",
        " ",
        text
    )

    # -----------------------------------------
    # Punctuation & symbol
    # -----------------------------------------

    text = re.sub(
        r"[^a-zA-ZÀ-ÿ\s]",
        " ",
        text
    )

    # -----------------------------------------
    # Karakter berulang
    # contoh:
    # baguuuus -> bagus
    # pajakkkkk -> pajak
    # -----------------------------------------

    text = re.sub(
        r"(.)\1{2,}",
        r"\1",
        text
    )

    # -----------------------------------------
    # Pisahkan kata
    # -----------------------------------------

    words = text.split()

    # -----------------------------------------
    # Normalisasi
    # -----------------------------------------

    normalized_words = []

    for word in words:

        if word in normalisasi:

            word = normalisasi[word]

        normalized_words.append(word)

    # -----------------------------------------
    # Stopword
    # -----------------------------------------

    cleaned_words = []

    for word in normalized_words:

        if word not in stopwords:

            cleaned_words.append(word)

    # -----------------------------------------
    # Gabungkan
    # -----------------------------------------

    text = " ".join(
        cleaned_words
    )

    # -----------------------------------------
    # Excess spaces
    # -----------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# =========================================================
# 10. PROSES CLEANING
# =========================================================

print("\nSedang melakukan cleaning...")

df["clean_text"] = df[
    TEXT_COLUMN
].apply(clean_text)


# =========================================================
# 11. FILTER DATA KOSONG SETELAH CLEANING
# =========================================================

jumlah_sebelum_clean_empty = len(df)

df = df[
    df["clean_text"].str.strip() != ""
]

print(
    "Data kosong setelah cleaning :",
    jumlah_sebelum_clean_empty - len(df)
)


# =========================================================
# 12. KEYWORD TOPIK PAJAK MARKETPLACE
# =========================================================

# Kata yang menunjukkan pembahasan pajak
# marketplace / e-commerce

PAJAK_KEYWORDS = {

    "pajak",
    "pph",
    "ppn",
    "npwp",
    "nik",
    "pajakpenghasilan",
    "pajakecommerce",
    "pajakmarketplace",
    "pungutpajak",
    "pemungutanpajak",
    "potongpajak",
    "potonganpajak",
    "tarifpajak",
    "pajakadalah",
    "pajakdigital",
    "pajakonline",
    "pajakusaha",
    "pajakumkm"
}


MARKETPLACE_KEYWORDS = {

    "marketplace",
    "ecommerce",
    "ecommerce",
    "ecom",
    "tokopedia",
    "shopee",
    "lazada",
    "bukalapak",
    "blibli",
    "tiktokshop",
    "tiktokshop",
    "seller",
    "penjual",
    "pedagang",
    "merchant",
    "platform",
    "online"
}


# =========================================================
# 13. KEYWORD SPAM
# =========================================================

SPAM_KEYWORDS = {

    # Joki / tugas
    "joki",
    "jasajoki",
    "openjoki",
    "jokitugas",
    "tugaskuliah",
    "jasatugas",

    # Giveaway
    "giveaway",
    "giveaways",

    # Follow / engagement
    "followback",
    "followforfollow",
    "follback",
    "likeforlike",
    "retweet",

    # Promo / jualan
    "openorder",
    "order",
    "preorder",
    "preorder",
    "diskon",
    "promo",
    "sale",

    # Crypto / NFT
    "nft",
    "crypto",
    "bitcoin",
    "ethereum",
    "solana",
    "token",
    "pfp",
    "mint",

    # Barang umum
    "sepatu",
    "baju",
    "tas",
    "makeup",
    "skincare",
    "photocard",
    "merch",
    "merchandise"
}


# =========================================================
# 14. KEYWORD TIDAK RELEVAN
# =========================================================

IRRELEVANT_KEYWORDS = {

    # Jual beli umum
    "price",
    "harga",
    "shipping",
    "ongkir",
    "kirim",
    "sold",
    "buy",
    "sell",
    "jualan",
    "belanja",

    # NFT / crypto
    "nft",
    "crypto",
    "bitcoin",
    "ethereum",
    "solana",
    "pfp",
    "mint",

    # Fandom / merchandise
    "gmmtv",
    "photocard",
    "merch",
    "merchandise",

    # Promo umum
    "giveaway",
    "giveaways"
}


# =========================================================
# 15. FUNGSI KLASIFIKASI
# =========================================================

def classify_text(text):

    words = set(text.split())

    # -----------------------------------------
    # A. CEK SPAM
    # -----------------------------------------

    spam_matches = words.intersection(
        SPAM_KEYWORDS
    )

    # -----------------------------------------
    # B. CEK TOPIK PAJAK
    # -----------------------------------------

    pajak_matches = words.intersection(
        PAJAK_KEYWORDS
    )

    marketplace_matches = words.intersection(
        MARKETPLACE_KEYWORDS
    )

    # -----------------------------------------
    # C. PRIORITAS SPAM
    # -----------------------------------------

    if len(spam_matches) >= 2:

        return "SPAM"

    # Joki tugas secara langsung dianggap spam
    if any(
        word in words
        for word in {
            "joki",
            "jasajoki",
            "openjoki",
            "jokitugas"
        }
    ):

        return "SPAM"

    # -----------------------------------------
    # D. RELEVAN
    # -----------------------------------------

    # Minimal ada kata pajak + marketplace/e-commerce
    if (
        len(pajak_matches) >= 1
        and len(marketplace_matches) >= 1
    ):

        return "RELEVAN"

    # -----------------------------------------
    # E. RELEVAN DENGAN PAJAK YANG JELAS
    # -----------------------------------------

    if len(pajak_matches) >= 2:

        return "RELEVAN"

    # -----------------------------------------
    # F. TIDAK RELEVAN
    # -----------------------------------------

    return "TIDAK_RELEVAN"


# =========================================================
# 16. KLASIFIKASI DATA
# =========================================================

print("\nSedang melakukan klasifikasi relevansi...")

df["kategori"] = df[
    "clean_text"
].apply(classify_text)


# =========================================================
# 17. MENAMBAHKAN ALASAN KLASIFIKASI
# =========================================================

def classification_reason(text, kategori):

    words = set(text.split())

    pajak = words.intersection(
        PAJAK_KEYWORDS
    )

    marketplace = words.intersection(
        MARKETPLACE_KEYWORDS
    )

    spam = words.intersection(
        SPAM_KEYWORDS
    )

    if kategori == "SPAM":

        if spam:
            return "Mengandung kata/indikasi spam: " + ", ".join(
                sorted(spam)
            )

        return "Terindikasi spam"

    if kategori == "RELEVAN":

        alasan = []

        if pajak:
            alasan.append(
                "topik pajak: " + ", ".join(sorted(pajak))
            )

        if marketplace:
            alasan.append(
                "marketplace/e-commerce: " +
                ", ".join(sorted(marketplace))
            )

        return " | ".join(alasan)

    return "Tidak ditemukan indikator kuat pajak marketplace"


df["alasan_kategori"] = df.apply(
    lambda row: classification_reason(
        row["clean_text"],
        row["kategori"]
    ),
    axis=1
)


# =========================================================
# 18. HASIL KLASIFIKASI
# =========================================================

print("\n" + "=" * 70)
print("HASIL KLASIFIKASI")
print("=" * 70)

print(
    df["kategori"].value_counts()
)


# =========================================================
# 19. MENAMPILKAN CONTOH
# =========================================================

print("\n" + "=" * 70)
print("CONTOH DATA RELEVAN")
print("=" * 70)

relevan = df[
    df["kategori"] == "RELEVAN"
]

if len(relevan) > 0:

    print(
        relevan[
            [
                TEXT_COLUMN,
                "clean_text",
                "kategori"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

else:

    print("Tidak ada data relevan.")


print("\n" + "=" * 70)
print("CONTOH SPAM")
print("=" * 70)

spam = df[
    df["kategori"] == "SPAM"
]

if len(spam) > 0:

    print(
        spam[
            [
                TEXT_COLUMN,
                "clean_text",
                "kategori"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

else:

    print("Tidak ada data spam.")


print("\n" + "=" * 70)
print("CONTOH TIDAK RELEVAN")
print("=" * 70)

tidak_relevan = df[
    df["kategori"] == "TIDAK_RELEVAN"
]

if len(tidak_relevan) > 0:

    print(
        tidak_relevan[
            [
                TEXT_COLUMN,
                "clean_text",
                "kategori"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


# =========================================================
# 20. MENYIMPAN SEMUA HASIL
# =========================================================

df = df.reset_index(drop=True)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# =========================================================
# 21. MEMBUAT FILE KHUSUS DATA RELEVAN
# =========================================================

relevant_output = os.path.join(
    BASE_DIR,
    "tweets-data",
    "data_relevan_pajak_marketplace.csv"
)

df_relevan = df[
    df["kategori"] == "RELEVAN"
].copy()

df_relevan.to_csv(
    relevant_output,
    index=False,
    encoding="utf-8-sig"
)


# =========================================================
# 22. MEMBUAT FILE SPAM
# =========================================================

spam_output = os.path.join(
    BASE_DIR,
    "tweets-data",
    "data_spam_pajak_marketplace.csv"
)

df_spam = df[
    df["kategori"] == "SPAM"
].copy()

df_spam.to_csv(
    spam_output,
    index=False,
    encoding="utf-8-sig"
)


# =========================================================
# 23. MEMBUAT FILE TIDAK RELEVAN
# =========================================================

irrelevant_output = os.path.join(
    BASE_DIR,
    "tweets-data",
    "data_tidak_relevan_pajak_marketplace.csv"
)

df_tidak_relevan = df[
    df["kategori"] == "TIDAK_RELEVAN"
].copy()

df_tidak_relevan.to_csv(
    irrelevant_output,
    index=False,
    encoding="utf-8-sig"
)


# =========================================================
# 24. RINGKASAN AKHIR
# =========================================================

print("\n" + "=" * 70)
print("PROSES SELESAI")
print("=" * 70)

print("Total data akhir :", len(df))

print(
    "\nDistribusi kategori:"
)

print(
    df["kategori"].value_counts()
)

print("\nFile hasil:")
print(
    "1. Semua data      :",
    OUTPUT_FILE
)

print(
    "2. Data relevan    :",
    relevant_output
)

print(
    "3. Data spam       :",
    spam_output
)

print(
    "4. Tidak relevan   :",
    irrelevant_output
)

print("\nCleaning + Filtering + Klasifikasi selesai!")