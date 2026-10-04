# Sydney Housing Price Estimator

## Run locally
Use Python 3.11 in a new virtual environment. Extract this ZIP, open a terminal in its folder, then run:

```
python -m pip install -r requirements.txt
python app.py
```

Open the local URL printed in the terminal. Choose suburb and property type, enter bedrooms, bathrooms and parking, enter a sale month such as 2026-09, then click Submit. The app displays the estimated sale price in AUD and interpretation notes. Edit the inputs and submit again to compare scenarios. These scenarios describe associations, not causal effects of renovations.

## Temporary online demonstration

```
python app.py --share
```

Use the public URL printed by Gradio. Your process and internet connection must remain running. This is a temporary demonstration, not persistent hosting. Do not describe the app as publicly deployed until the URL is live and tested.

## Persistent hosting
Create a Gradio Space on Hugging Face, then upload app.py, predictor.py, requirements.txt and housing_model.joblib to the root of that Space. Follow its current Gradio setup instructions and choose a Python version compatible with the pinned dependencies. After the build succeeds, open its public URL and test a prediction. Public hosting exposes uploaded files, so do not upload your raw dataset or notebook. The bundle includes only the fitted model, not the source sales records.

## Screenshots for Part 6
1. Input form with all six property fields visible.
2. A submitted prediction showing the estimated AUD price and interpretation notes.
3. The live deployment with its URL visible, after hosting or starting a temporary shared demonstration.

## Implementation and verification
The app loads the complete saved Linear Regression pipeline, including numerical imputation/scaling and categorical encoding. predictor.py constructs the same seven features as the notebook, including bedroom-bathroom interaction and sale-month index. The original 80:20 split with seed 42 and suburb stratification was preserved. The model was fitted on the same 96 training records; its held-out RMSE reproduced the notebook value of AUD 435,302.56. No test records were added to training.

The joblib artifact was created for the scikit-learn version pinned in requirements.txt. Only load trusted joblib files. The model was trained on May–September 2026 sales, and is not a current market forecast. It omits reliable land/floor area, condition and exact location. Outputs are educational point estimates; no validated prediction interval is available. Never interpret the overall RMSE as a guaranteed error bound.
