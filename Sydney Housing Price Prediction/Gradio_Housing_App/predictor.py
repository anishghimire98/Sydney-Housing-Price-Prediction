from pathlib import Path
import math
import joblib
import pandas as pd

MODEL = joblib.load(Path(__file__).with_name('housing_model.joblib'))
SUBURBS = ['Blacktown', 'Parramatta', 'Chatswood']
TYPES = ['Apartment', 'House', 'Townhouse', 'Semi-detached']

def predict_price(suburb, property_type, bedrooms, bathrooms, parking, sale_month):
    if suburb not in SUBURBS or property_type not in TYPES:
        raise ValueError('Choose a suburb and property type from the lists.')
    values = [bedrooms, bathrooms, parking]
    for value, low in zip(values, [1, 1, 0]):
        if value is None or not math.isfinite(float(value)) or float(value) != int(value) or not low <= int(value) <= 20:
            raise ValueError('Enter whole room counts from 1 to 20 and parking spaces from 0 to 20.')
    date = pd.to_datetime(str(sale_month), format='%Y-%m', errors='coerce')
    if pd.isna(date):
        raise ValueError('Enter a sale month as YYYY-MM, for example 2026-09.')
    beds, baths, cars = map(int, values)
    features = pd.DataFrame([{
        'suburb': suburb, 'property_type': property_type,
        'bedrooms': beds, 'bathrooms': baths, 'parking_spaces': cars,
        'bed_bath_interaction': beds * baths,
        'sale_month_index': (date.year - 2025) * 12 + date.month - 10
    }])
    price = float(MODEL.predict(features)[0])
    notes = ['Educational estimate based on 96 training sales from three suburbs. Missing size, condition and exact-location details can cause large errors. This is not a professional valuation.']
    if not pd.Timestamp('2026-05-01') <= date <= pd.Timestamp('2026-09-01'):
        notes.append('This month is outside the training period (May–September 2026). The model has not been validated for forecasting future market prices.')
    if property_type == 'Semi-detached':
        notes.append('Semi-detached properties were very rare in the collected data.')
    if price <= 0:
        return 'No reliable estimate', ' '.join(notes + ['The model returned a non-positive price for these inputs.'])
    return f'AUD ${price:,.0f}', ' '.join(notes)
