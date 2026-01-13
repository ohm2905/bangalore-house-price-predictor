import pickle
import pandas as pd
import os
from django.shortcuts import render

# Base directory (outer houseprice folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model
model_path = os.path.join(BASE_DIR, 'model', 'RidgeModel.pkl')
model = pickle.load(open(model_path, 'rb'))

# Get location categories from model
locations = model.named_steps['columntransformer'] \
    .transformers_[0][1] \
    .categories_[0]


def home(request):
    prediction = None

    if request.method == "POST":
        location = request.POST.get('location')
        total_sqft = float(request.POST.get('total_sqft'))
        bath = int(request.POST.get('bath'))
        bhk = int(request.POST.get('bhk'))

        input_df = pd.DataFrame(
            [[location, total_sqft, bath, bhk]],
            columns=['location', 'total_sqft', 'bath', 'bhk']
        )

        raw_price = model.predict(input_df)[0]  # price in Lakhs

        if raw_price < 100:
            prediction = f"₹ {raw_price:.2f} Lakhs"
        else:
            prediction = f"₹ {raw_price/100:.2f} Crore"


    return render(request, 'index.html', {
    'prediction': prediction,
    'locations': locations,
    'selected_location': location if request.method == "POST" else "",
    'total_sqft': request.POST.get('total_sqft', ''),
    'bath': request.POST.get('bath', ''),
    'bhk': request.POST.get('bhk', '')
})


