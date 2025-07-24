from fixit_frw.models import Items
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def hitung_kuadrat(value: int) -> int:
    return value ** 2

def hitung_regresi_harga() -> dict:
    # Ambil data dari database sebagai list flat
    price_offered = list(Items.objects.values_list('price_offered', flat=True))

    price_final = list(Items.objects.values_list('price_final', flat=True))

    # Validasi jumlah data
    if len(price_offered) < 2 or len(price_final) < 2:
        raise ValueError("Data tidak cukup untuk analisis regresi")

    if len(price_offered) != len(price_final):
        raise ValueError("Jumlah data price_offered dan price_final tidak sama")

    # Buat DataFrame dari list
    df = pd.DataFrame({
        'price_offered': price_offered,
        'price_final': price_final
    }).dropna()

    if df.shape[0] < 2:
        raise ValueError("Data valid kurang dari 2 baris setelah dibersihkan")

    # Fitur dan target
    X = df[['price_offered']]
    y = df['price_final']

    # Model regresi
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    # Evaluasi
    hasil = {
        'koefisien': float(model.coef_[0]),
        'intercept': float(model.intercept_),
        'r2_score': float(r2_score(y, y_pred)),
        'mean_squared_error': float(mean_squared_error(y, y_pred)),
        'jumlah_data': len(df),
    }

    return hasil
