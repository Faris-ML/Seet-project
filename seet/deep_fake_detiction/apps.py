from django.apps import AppConfig
from transformers import AutoFeatureExtractor
import tensorflow as tf
from seet.settings import BASE_DIR
import os
from whatsappcloudapi.whatsappcloudapi_client import WhatsappcloudapiClient
from whatsappcloudapi.configuration import Environment

class DeepFakeDetictionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
    model = tf.saved_model.load(os.path.join(BASE_DIR,'Models','dfd_20_1024_256'))
    client = WhatsappcloudapiClient(access_token='AccessToken')
    name = "deep_fake_detiction"
