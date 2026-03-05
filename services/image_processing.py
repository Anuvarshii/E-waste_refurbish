import numpy as np
from PIL import Image
import tensorflow as tf
from config import DAMAGE_MODEL_PATH

cnn_model = tf.keras.models.load_model(
    DAMAGE_MODEL_PATH,
    compile=False
)

def get_damage_score(img_path):
    img = Image.open(img_path).convert("RGB").resize((224,224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = cnn_model.predict(img_array, verbose=0)[0][0]
    damage_score = round((1 - prediction) * 10, 2)

    return damage_score