#!/usr/bin/env python3
import os
import sys

# Warna ANSI untuk terminal
WARNA_RESET = "\033[0m"
WARNA_BIRU = "\033[94m"
WARNA_HIJAU = "\033[92m"
WARNA_CYAN = "\033[96m"
WARNA_MERAH = "\033[91m"
WARNA_KUNING = "\033[93m"
WARNA_PUTIH = "\033[97m"
WARNA_KUNING_TEBAL = "\033[93;1m"
WARNA_MERAH_TEBAL = "\033[91;1m"

def dapatkan_warna(jalur_item):
    if os.path.islink(jalur_item):
        return WARNA_CYAN if os.path.exists(jalur_item) else WARNA_MERAH
    elif os.path.isdir(jalur_item):
        return WARNA_BIRU
    elif os.path.isfile(jalur_item):
        if sys.platform != "win32" and os.access(jalur_item, os.X_OK):
            return WARNA_HIJAU
        return WARNA_RESET
    else:
        return WARNA_KUNING

def cetak_pohon_direktori(jalur_utama, awalan="", akhir=True, root=False):
    if root:
        warna = dapatkan_warna(jalur_utama)
        nama = os.path.basename(jalur_utama)
        print(warna + nama + WARNA_RESET)
        awalan_baru = ""
    else:
        konektor = "└── " if akhir else "├── "
        warna = dapatkan_warna(jalur_utama)
        nama = os.path.basename(jalur_utama)
        print(awalan + konektor + warna + nama + WARNA_RESET)
        awalan_baru = awalan + ("    " if akhir else "│   ")

    if os.path.islink(jalur_utama):
        return

    try:
        daftar_item = os.listdir(jalur_utama)
    except (PermissionError, OSError) as e:
        print(awalan_baru + "└── [" + str(e) + "]")
        return

    # Pisahkan direktori dan file
    direktori = []
    file = []
    for item in daftar_item:
        jalur_item = os.path.join(jalur_utama, item)
        if os.path.isdir(jalur_item) and not os.path.islink(jalur_item):
            direktori.append(item)
        else:
            file.append(item)

    # Urutkan: direktori dulu, lalu file
    item_terurut = sorted(direktori) + sorted(file)
    total_item = len(item_terurut)
    
    for i, item in enumerate(item_terurut):
        jalur_item = os.path.join(jalur_utama, item)
        item_akhir = (i == total_item - 1)
        
        if os.path.isdir(jalur_item) and not os.path.islink(jalur_item):
            cetak_pohon_direktori(jalur_item, awalan_baru, item_akhir)
        else:
            konektor_item = "└── " if item_akhir else "├── "
            warna = dapatkan_warna(jalur_item)
            print(awalan_baru + konektor_item + warna + item + WARNA_RESET)

def tampilkan_error_dan_bantuan():
    """Tampilkan pesan error dan cara penggunaan tools"""
    nama_tools = os.path.basename(sys.argv[0])
    
    print(f"\n{WARNA_MERAH_TEBAL}ERROR:{WARNA_RESET} {WARNA_MERAH}Argumen direktori tidak ditemukan!{WARNA_RESET}")
    print(f"\n{WARNA_KUNING_TEBAL}Penggunaan:{WARNA_RESET}")
    print(f"  {WARNA_PUTIH}{nama_tools} <direktori>{WARNA_RESET}")
    print()

def utama():
    # Aktifkan warna di Windows
    if sys.platform == "win32":
        os.system("color")

    # Cek argumen - HARUS ada tepat 1 argumen (direktori)
    if len(sys.argv) != 2:
        tampilkan_error_dan_bantuan()
        sys.exit(1)

    direktori_target = sys.argv[1]
    direktori_target = os.path.expanduser(direktori_target)

    # Cek apakah direktori ada
    if not os.path.exists(direktori_target):
        print(f"\n{WARNA_MERAH}Kesalahan:{WARNA_RESET} Direktori '{direktori_target}' tidak ditemukan!")
        sys.exit(1)

    # Cek apakah itu direktori
    if not os.path.isdir(direktori_target):
        print(f"\n{WARNA_MERAH}Kesalahan:{WARNA_RESET} '{direktori_target}' bukan direktori!")
        sys.exit(1)

    jalur_absolut = os.path.abspath(direktori_target)
    print(f"\n{WARNA_KUNING}Struktur direktori: {WARNA_PUTIH}{jalur_absolut}{WARNA_RESET}\n")
    cetak_pohon_direktori(jalur_absolut, root=True)

if __name__ == "__main__":
    utama()
