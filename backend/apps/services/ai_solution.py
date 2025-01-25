from transformers import pipeline
import re
from translate import Translator

class SolutionService:
    def __init__(self):
        self.generator = pipeline('text-generation', model='gpt2-large')  # Replace with your OpenAI API key
        self.solution = "No reponses available"
        self.translator = Translator(to_lang='en') 

    def get_solution_suggestion(self, description, category, lang):
        prompt = f"You are an expert you provide the solution for different grievanance. Please provide a suitable solution or suggestion based on past similar grievances and best practices for Grievance Description: {description}\nCategory: {category}"
        # Translate prompt to the target language if it's not English
        if lang != 'en':
            translator = Translator(to_lang=lang)
            translated_prompt = translator.translate(prompt)
        else:
            translated_prompt = prompt
        response = self.generator(translated_prompt, max_length=200, num_return_sequences=1)
        self.solution = response[0]['generated_text'].strip()

        # Clean the response to remove the prompt and keep only the generated text
        # Remove the prompt from the generated text using regex
        #self.solution = re.sub(re.escape(prompt), '', self.solution).strip()
        # print(response)
        # print(self.solution)
        return self.solution
