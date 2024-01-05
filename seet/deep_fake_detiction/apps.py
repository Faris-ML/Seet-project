from django.apps import AppConfig
from transformers import AutoFeatureExtractor
import tensorflow as tf

class DeepFakeDetictionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
    model = tf.saved_model.load('./Models/dfd_20_1024_256')
    name = "deep_fake_detiction"
