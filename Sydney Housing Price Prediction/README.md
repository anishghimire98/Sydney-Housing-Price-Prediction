# Sydney Housing Price Prediction and Decision Support

A machine learning project investigating housing sale prices in **Blacktown, Parramatta and Chatswood, Sydney**. The project covers data collection, exploratory analysis, feature engineering, regression modelling, prediction failures, comparison with human and large language model (LLM) estimates, and a **Gradio web application**.

The application provides educational price estimates. It is not a professional valuation or a validated forecast of current market prices.

## Project files

Use the following layout when uploading the project to this repository:

| File | Purpose |
|---|---|
| `Sydney_Housing_Collected_Data.xlsx` | Collected property records, source URLs and collection notes; data are in the `Properties` sheet. |
| `House Price Prediction.ipynb` | Analysis, feature engineering, model evaluation and comparison experiments. |
| `app.py` | Gradio property-entry form and prediction display. |
| `predictor.py` | Input validation, feature creation and model prediction. |
| `housing_model.joblib` | Saved Linear Regression pipeline, including fitted preprocessing. |
| `requirements.txt` | Application dependencies and model-compatible package versions. |
| `README.md` | Project documentation and instructions. |

Keep the application files together. Include the final PDF report in the repository if you want readers to access the written discussion alongside the code.

## Dataset

The dataset contains **120 properties**, with **40 properties per suburb**, collected from Domain and realestate.com.au. Records include sale price, sale date, property type, room counts, parking, and source information. The collected sales cover May–September 2026.

Data quality limitations include:

- Land area is missing for 92.5% of records; floor area is entirely missing.
- Some reported area values do not identify whether they represent land or internal floor area.
- Property types and sale dates are unevenly represented across suburbs.
- The sample is small and is not representative of the entire Sydney housing market.

Source URLs and verification notes are retained in the spreadsheet. Source material remains subject to the original providers' rights and terms.

## Workflow

1. Audit missing values, duplicates and invalid prices.
2. Reserve 20% of records for testing using a suburb-stratified split with `random_state=42`.
3. Explore prices, suburb differences, sales over time, numeric relationships and potential outliers using the training set.
4. Create features and compare three regression approaches using five-fold cross-validation.
5. Evaluate the selected model on held-out data and investigate its five largest absolute errors.
6. Compare ML, LLM and personal estimates for ten selected test properties.
7. Serve the saved model through Gradio.

### Features and preprocessing

The model uses suburb, property type, bedrooms, bathrooms, parking spaces, and two engineered features:

- **Bedroom–bathroom interaction:** bedrooms × bathrooms.
- **Sale-month index:** `(year - 2025) * 12 + month - 10`, where October 2025 is zero.

Numeric features use median imputation and standardisation. Categorical features use most-frequent imputation and one-hot encoding. These transformations are fitted inside each cross-validation pipeline to reduce data leakage. IDs, addresses, source links and sale prices are not predictors.

## Model evaluation

The training set contains **96 properties**, and the held-out test set contains **24**. The models use the same shuffled five-fold cross-validation splits. RMSE is the primary selection metric; MAE and R² provide additional perspectives.

| Model | Mean CV RMSE (AUD) | Mean CV MAE (AUD) | Mean CV R² |
|---|---:|---:|---:|
| Linear Regression | 411,586.71 | 298,901.95 | 0.69 |
| Random Forest | 441,250.12 | 236,792.77 | 0.66 |
| Decision Tree | 498,591.96 | 257,782.25 | 0.55 |

**Linear Regression** was selected for its lowest CV RMSE. Random Forest had a lower CV MAE, so the preferred model depends partly on how heavily large errors are penalised. The CV RMSE differences should also be interpreted alongside the substantial variation between folds.

The selected model achieved:

| Held-out metric | Result |
|---|---:|
| MAE | AUD 286,929 |
| RMSE | AUD 435,303 |
| R² | 0.837 |

The saved application model uses the original 96 training records. Test records were not added to training. The largest individual test error was approximately AUD 1.42 million, illustrating why overall scores do not guarantee accurate individual valuations.

### ML, LLM and human comparison

| Approach | MAE (AUD) | RMSE (AUD) | MAPE |
|---|---:|---:|---:|
| Linear Regression | 187,348 | 227,082 | 22.37% |
| Personal estimates | 193,100 | 277,136 | 18.96% |
| LLM estimates | 266,700 | 344,317 | 25.39% |

These results apply only to the ten selected cases. Selection excluded the five largest ML errors examined earlier, which favours a sample without the model's known worst failures. Personal estimates were recorded after seeing LLM estimates, creating possible anchoring. The comparison is exploratory rather than an independent test of human or LLM valuation ability.

## Install and run the application

Use **Python 3.11 or 3.12**. A separate virtual environment is recommended.

From the project directory, run:

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```bat
.venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the application dependencies and start Gradio:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open the local URL printed in the terminal. Keep the terminal running while using the application.

### Enter a property

1. Select the suburb and property type.
2. Enter bedrooms, bathrooms and parking spaces.
3. Enter a sale month in `YYYY-MM` format.
4. Click **Submit**.
5. Review the predicted price in AUD and the interpretation notes.

For example, a **Parramatta apartment with two bedrooms, two bathrooms and one parking space**, using **2026-09**, produces an estimate of approximately **AUD 710,724**.

The application checks room counts and the month format, and flags dates outside the training period. Changing an input explores a model association; it does not establish the causal value of a renovation or added parking space.

### Temporary public demonstration

```bash
python app.py --share
```

Gradio prints a temporary public URL. The application process and internet connection must remain active. This is not persistent hosting. Do not assume a public deployment exists simply because the source code is available on GitHub.

For persistent hosting, the application files can be deployed to a Gradio-compatible service such as a Hugging Face Space. Add a tested live application link to this README after deployment.

## Reproduce the notebook

Install the additional analysis dependencies:

```bash
python -m pip install matplotlib openpyxl notebook
python -m notebook
```

Open `House Price Prediction.ipynb`. If its first cell still contains the original local Windows dataset path, replace that read statement with:

```python
df = pd.read_excel(
    "Sydney_Housing_Collected_Data.xlsx",
    sheet_name="Properties"
)
```

Launch Jupyter from the project directory, then restart the kernel and run all cells in order. The stored human and LLM estimates reproduce the recorded experiment; rerunning the notebook does not contact an LLM service.

To export the selected fitted pipeline again after Part 3:

```python
import joblib
joblib.dump(best_model, "housing_model.joblib")
```

Use matching scikit-learn versions when saving and loading models, and load only trusted joblib files. Changing features or retraining the model requires updating and checking the application accordingly.

## Limitations and responsible use

- Missing size, condition, exact-location, building and strata information can cause substantial errors.
- Rare property types, luxury homes and unusual feature combinations have limited comparable training examples.
- Predictions outside the training period or market coverage are not validated forecasts.
- Historical prices and uneven sampling may produce biased or unequal errors across property groups. Overall accuracy does not demonstrate fairness.
- No validated prediction interval is supplied; RMSE is not an individual error bound.
- Predictions should be checked against verified property information and comparable sales before informing decisions.

Future work should prioritise representative data, verified property characteristics, later-period evaluation, building-aware splitting where appropriate, subgroup error analysis and calibrated prediction intervals.

## References and tools

- [Domain](https://www.domain.com.au/)
- [realestate.com.au](https://www.realestate.com.au/)
- [scikit-learn documentation](https://scikit-learn.org/stable/)
- [pandas documentation](https://pandas.pydata.org/docs/)
- [Gradio documentation](https://www.gradio.app/docs)
- [Gradio sharing and hosting guide](https://www.gradio.app/guides/sharing-your-app)

Generative AI assisted with code development, application creation, interpretation and report wording. The separate LLM valuation experiment is documented in the project. Any submission acknowledgement should accurately describe the assistance used and follow the unit's requirements.
