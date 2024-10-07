from abc import ABC, abstractmethod
import openai
import groq
import random


class LLMBase(ABC):
    def prepare_messages(self, message, prompt, history=None):
        messages = [{"role": "system", "content": prompt}]

        if history:
            for human, assistant in history:
                messages.append({"role": "user", "content": human})
                messages.append({"role": "assistant", "content": assistant})

        messages.append({"role": "user", "content": message})
        print(messages) ## TODO remove print statement
        return messages

    @abstractmethod
    def _call_model_api(self, messages):
        pass

    def generate_response(self, message, prompt, history=None):
        """Generates the response by calling the model's API."""
        messages = self.prepare_messages(message, prompt, history)
        response = self._call_model_api(messages)
        return response


class LlamaModel(LLMBase):
    def __init__(self, groq_api_key):
        self.client = groq.Groq(api_key=groq_api_key)

    def _call_model_api(self, messages):
        # Call Groq API and return the response
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            max_tokens=1000
        ).choices[0].message.content
        return response


class GPTModel(LLMBase):
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def _call_model_api(self, messages):
        # Call OpenAI's GPT API and return the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000
        ).choices[0].message['content']
        return response


class MistralModel(LLMBase):
    def __init__(self, groq_api_key):
        self.client = groq.Groq(api_key=groq_api_key)

    def _call_model_api(self, messages):
        # Call Groq API and return the response
        response = self.client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            max_tokens=1000
        ).choices[0].message.content
        return response


class NewModel(LLMBase):
    def __init__(self, api_key):
        self.api_key = api_key  # Initialize new model with its API key

    def _call_model_api(self, messages):
        # Add the unique API call logic for the new model
        return "New Model's response"


class LLMManager:
    def __init__(self, models):
        self.models = models  # List of model instances

    def chat_with_models(self, message, prompt, history=None):
        model_a_name = None
        model_a_response = None
        model_b_name = None
        model_b_response = None

        if len(self.models) < 2:
            raise ValueError("At least two models are required to chat.")

        selected_models = random.sample(self.models, 2)  # Select 2 random models

        for i, model in enumerate(selected_models):
            model_name = model.__class__.__name__
            response = model.generate_response(message, prompt, history)
            print(f'Response for {model_name} was generated')

            # Store the model names and responses in global variables
            if i == 0:
                model_a_name = model_name
                model_a_response = response
            else:
                model_b_name = model_name
                model_b_response = response

        return model_a_name, model_b_name, model_a_response, model_b_response


