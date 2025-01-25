from google.cloud import speech_v1p1beta1 as speech
import pyttsx3

class SpeechService:
    def __init__(self):
        self.client = speech.SpeechClient()
        self.tts_engine = pyttsx3.init()

    def transcribe_audio(self, file_path):
        with open(file_path, 'rb') as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(language_code="en-IN")
        response = self.client.recognize(config=config, audio=audio)
        for result in response.results:
            return result.alternatives[0].transcript

    def synthesize_speech(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
