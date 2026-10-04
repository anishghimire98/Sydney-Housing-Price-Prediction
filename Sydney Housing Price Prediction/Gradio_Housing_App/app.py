import argparse
import gradio as gr
from predictor import predict_price, SUBURBS, TYPES

def estimate(*inputs):
    try:
        return predict_price(*inputs)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc

demo = gr.Interface(
    fn=estimate,
    api_name="predict",
    inputs=[
        gr.Dropdown(SUBURBS, value='Blacktown', label='Suburb'),
        gr.Dropdown(TYPES, value='House', label='Property type'),
        gr.Number(value=3, precision=0, minimum=1, maximum=20, label='Bedrooms'),
        gr.Number(value=2, precision=0, minimum=1, maximum=20, label='Bathrooms'),
        gr.Number(value=2, precision=0, minimum=0, maximum=20, label='Parking spaces'),
        gr.Textbox(value='2026-09', label='Sale month (YYYY-MM)')
    ],
    outputs=[gr.Textbox(label='Predicted sale price'), gr.Textbox(label='How to interpret this estimate')],
    title='Sydney Housing Price Estimator',
    description='Enter property details to estimate a sale price using Linear Regression. The model was trained on sales from May–September 2026; it is not a live market valuation service.',
    examples=[['Parramatta','Apartment',2,2,1,'2026-09'], ['Blacktown','House',3,1,1,'2026-09']],
    flagging_mode='never'
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--share', action='store_true', help='Create a temporary public Gradio link.')
    args = parser.parse_args()
    demo.launch(share=args.share)
