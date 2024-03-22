from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from deep_fake_detiction.apps import DeepFakeDetictionConfig
import librosa
from librosa.core.audio import resample,to_mono
import json
import numpy as np
import io
import soundfile as sf
# Create your views here.
model, feature_extractor = DeepFakeDetictionConfig.model, DeepFakeDetictionConfig.feature_extractor
class Predictor(APIView):
    def post(self, request ,*args, **kwargs) :
        def sigmoid(x):
            return 1 / (1+np.exp(-x))
        tmp = io.BytesIO(bytes(request.body))
        arr,sr = sf.read(tmp)
        arr = to_mono(arr.T)
        arr = resample(arr, orig_sr=sr, target_sr=feature_extractor.sampling_rate)
        
        input_voice = feature_extractor(arr.tolist(),
                      truncation=True,
                      padding='max_length',
                      max_length=500,
                      sampling_rate = feature_extractor.sampling_rate,
                      return_tensor = 'tf')
        pred = model(input_voice)
        pred = sigmoid(pred['logits'])[0][0]
        threshold = 0.9
        if pred > threshold:
            return Response(data={'response': "Not a human voice"}, headers={"Access-Control-Allow-Headers":'*',
                                                        'Access-Control-Allow-Origin':'*'})
        else:
            return Response(data={'presponse': "Human voice"}, headers={"Access-Control-Allow-Headers":'*',
                                                        'Access-Control-Allow-Origin':'*'})