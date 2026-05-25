# Kalkulator Canggih Pro - Dreamy Sunset
Aplikasi web **Kalkulator Canggih Pro** dirancang menggunakan arsitektur modular yang memisahkan antara pengendali rute (Routes) dan logika perhitungan (Services). Aplikasi ini mengadopsi prinsip desain *Mobile-First*, mendukung perubahan tema *Dark & Light Mode* secara dinamis, dan menggunakan sesi (Flask Session) untuk mengelola riwayat perhitungan pengguna tanpa menggunakan basis data eksternal.

---

## Fitur Utama

### 1. Operasi Aritmatika
Mendukung berbagai operasi perhitungan matematika lengkap beserta rumus penulisan dan langkah penyelesaian rinci:
*   Penjumlahan (`+`)
*   Pengurangan (`-`)
*   Perkalian (`×`)
*   Pembagian (`÷`) dengan validasi pembagian nol secara aman.
*   Perpangkatan (`a^b`)
*   Akar Kuadrat (`√a`) dengan validasi angka negatif.
*   Modulus (Sisa Hasil Bagi `%`)
*   Floor Division (Pembagian Bulat `//`)

### 2. Operator Logika (Bitwise)
Menyediakan kalkulator bitwise interaktif untuk operasi logika biner:
*   Operasi: `AND`, `OR`, `NOT` (A saja), `XOR`, `NAND`, `NOR`.
*   Visualisasi biner lengkap dari input dan hasil dengan padding bit dinamis (minimal 8-bit).
*   Tabel Kebenaran (*Truth Table*) interaktif yang sesuai dengan operator yang sedang aktif.
*   Langkah penjelasan operasi logika bit-demi-bit dari bit terpenting hingga terkecil.

### 3. Transformasi & Konversi Bilangan
Modul serbaguna untuk konversi angka, suhu, kurs, dan kalkulasi deret:
*   **Konversi Basis**: Mengonversi basis desimal (DEC), biner (BIN), oktal (OCT), dan heksadesimal (HEX) secara simultan beserta langkah pembagian berulang.
*   **Konversi Suhu**: Konversi timbal balik antar Celsius (°C), Fahrenheit (°F), Kelvin (K), dan Reamur (°R) lengkap dengan rumusnya.
*   **Konversi Mata Uang**: Mengonversi nominal Rupiah (IDR) ke USD, EUR, SGD, MYR, JPY menggunakan kurs konversi statis yang aman.
*   **Bonus (Faktorial & Fibonacci)**: Perhitungan Faktorial ($n!$) dengan visualisasi deret perkalian, serta deret barisan Fibonacci sampai ke-n beserta langkah penjumlahan sukunya (dibatasi hingga maksimal 100 suku demi keamanan performa).

---

## Stack Teknis
*   **Backend**: Python 3.x + Flask (Mikroframework)
*   **Frontend**: HTML5 + Tailwind CSS CDN (v3) + Vanilla JavaScript
*   **Penyimpanan Sesi**: Flask Session (berbasis cookie terenkripsi dengan SECRET_KEY FIFO maksimal 20 item)
*   **Desain**: Tema gelap/terang otomatis (sinkronisasi dengan preferensi sistem operasi & disimpan permanen di `localStorage`)

---

## Struktur Folder

```text
kalkulator/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── arithmetic.py
│   │   ├── logic.py
│   │   └── transform.py
│   ├── services/
│   │   ├── arithmetic.py
│   │   ├── logic.py
│   │   └── transform.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── arithmetic.html
│   │   ├── logic.html
│   │   └── transform.html
│   └── static/
│       ├── css/
│       │   └── custom.css
│       └── js/
│           └── theme.js
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Cara Install & Persiapan

1.  **Klon Repositori**
    ```bash
    git clone <url-repositori-anda>
    cd kalkulator
    ```

2.  **Buat Virtual Environment (Opsional tetapi Direkomendasikan)**
    ```bash
    python -m venv venv
    # Aktifkan di Windows:
    venv\Scripts\activate
    # Aktifkan di macOS/Linux:
    source venv/bin/activate
    ```

3.  **Pasang Dependensi**
    Aplikasi ini hanya membutuhkan Flask versi terbaru:
    ```bash
    pip install -r requirements.txt
    ```

---

## Cara Menjalankan Aplikasi

Jalankan server Flask lokal dengan mengeksekusi file entry point `run.py`:

```bash
python run.py
```

Setelah server aktif, buka peramban (browser) Anda dan akses alamat lokal berikut:
```text
http://127.0.0.1:5000
```
