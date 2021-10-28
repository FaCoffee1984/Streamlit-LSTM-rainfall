This folder contains 6 Keras LSTM models trained using:

- epochs = 500
- 3 hidden layers
- standard scaler
- past_window_size = 120 (10 years)
- future_window_size = 24 (2 years)

The models are serialised using the HDF5 (.h5) format. To load a serialised Keras model, use:

```python
from tensorflow.keras.models import load_model

# load model
model = load_model('model.h5')
```

