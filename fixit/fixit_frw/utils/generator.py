import random
import string

def generate_short_id_from_name(name: str) -> str:
    """
    Menghasilkan ID pendek dari nama:
    huruf pertama + huruf tengah + huruf terakhir

    Contoh:
        "jakal" => "jkl"
        "jogja" => "jga"
        "jember" => "jbr"
    """
    name = name.strip().lower()

    if len(name) < 3:
        raise ValueError("Nama harus memiliki setidaknya 3 karakter")

    first = name[0]
    mid_index = (len(name) - 1) // 2  # Pilih tengah ke kiri untuk ganjil/genap
    mid = name[mid_index]
    last = name[-1]

    return f"{first}{mid}{last}"

def generate_custom_id_with_suffix(name: str, length: int = 4) -> str:
    base = generate_short_id_from_name(name)
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{base}-{suffix}"
