from transformers import pipeline

class ConversationalAIService:
    def __init__(self):
        self.nlp_pipeline = pipeline("text-generation", model="gpt2-large")
        self.solution = "No responses available"
    def generate_response(self, prompt):
        response = self.nlp_pipeline(prompt, max_length=100, do_sample=True)
        
        self.solution = response[0]['generated_text'].strip()
        # Clean the response to remove the prompt and keep only the generated text
        # if self.solution.startswith(prompt):
        #     self.solution = self.solution[len(prompt):].strip()
        return self.solution
