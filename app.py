import gradio as gr
from dotenv import load_dotenv
import os
from Database import Database
from LLM import LLMManager, LlamaModel, GPTModel, MistralModel
from usecase_text import (Usecase_description_samenvatten,
                          Usecase_description_vereenvoudigen,
                          samenvatten_prompt,
                          vereenvoudigen_prompt)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Instantiate models
groq_model = LlamaModel(GROQ_API_KEY)
gpt_model = GPTModel(OPENAI_API_KEY)
mistral_model = MistralModel(GROQ_API_KEY)

# Add models to LLMManager, the LLMManager generates output from 2 random models
llm_manager = LLMManager([groq_model, gpt_model, mistral_model])

# Initiate database
db = Database()

# Global variable to store the user's input and model responses
stored_user_input = None
prompt = None
stored_model_a_name = None
stored_model_b_name = None
stored_model_a_response = None
stored_model_b_response = None
feedback = None
stored_user_feedback = None

# Function to set the use case
def set_usecase(value):
    global prompt
    if value == "samenvatten":
        prompt = samenvatten_prompt
        return prompt
    elif value == "vereenvoudigen":
        prompt = vereenvoudigen_prompt
        return prompt
    else:
        raise ValueError("Invalid use case value")

# Function to handle the submit action by passing the user input to generate responses
def handle_submit(user_message):
    global stored_user_input, stored_model_a_name, stored_model_b_name, stored_model_a_response, stored_model_b_response, prompt
    model_a_name, model_b_name, model_a_response, model_b_response = llm_manager.chat_with_models(user_message, prompt, history=None)

    stored_user_input = user_message
    stored_model_a_response = model_a_response
    stored_model_a_name = model_a_name
    stored_model_b_response = model_b_response
    stored_model_b_name = model_b_name

    return model_a_response, model_b_response

# Function to set feedback
def set_feedback(value):
    global feedback
    feedback = value
    print(f"Feedback set to: {feedback}")

# Function to handle feedback submission
def handle_feedback(feedback_motivation):
    global stored_user_input, stored_model_a_name, stored_model_b_name, stored_model_a_response, stored_model_b_response, feedback

    if stored_user_input and stored_model_a_name and stored_model_b_name and stored_model_a_response and stored_model_b_response and feedback and feedback_motivation:
        db.log_feedback(stored_user_input, stored_model_a_name, stored_model_b_name, stored_model_a_response, stored_model_b_response, feedback, feedback_motivation)
        print("Feedback logged successfully.")

# Create interface with two large output textboxes placed side by side
with (gr.Blocks() as demo):
    gr.Markdown("## UWV Lineaus")

    with gr.Tab("Use case"):
        # Two use cases
        with gr.Row():
            gr.Textbox(label="Usecase samenvatten", lines=5, interactive=False, value=Usecase_description_samenvatten)
            gr.Textbox(label="Usecase vereenvoudigen", lines=5, interactive=False, value=Usecase_description_vereenvoudigen)


        # Buttons to select use case
        with gr.Row():
            select_samenvatten_button = gr.Button("Selecteer 'Samenvatten' use case")
            select_vereenvoudigen_button = gr.Button("Selecteer 'Vereenvoudigen' use case")

        # Output textbox to display selected prompt
        selected_prompt = gr.Textbox(label="Selected prompt", lines=2, interactive=False)

        # Button actions to update the selected prompt textbox
        select_samenvatten_button.click(fn=lambda: set_usecase('samenvatten'), inputs=[], outputs=selected_prompt)
        select_vereenvoudigen_button.click(fn=lambda: set_usecase('vereenvoudigen'), inputs=[], outputs=selected_prompt)

    with gr.Tab("Test"):
        with gr.Row():
            model_a_output = gr.Textbox(label="Model A Output", lines=10, interactive=False)
            model_b_output = gr.Textbox(label="Model B Output", lines=10, interactive=False)

        user_input = gr.Textbox(label="Your Message", lines=2, placeholder="Type message hier...")

        # Define the button
        submit_button = gr.Button("Submit")
        # Set the function to be called on button click
        submit_button.click(fn=handle_submit, inputs=[user_input], outputs=[model_a_output, model_b_output])

        # Add the feedback buttons
        with gr.Row():
            model_a_better_button = gr.Button("Model A is better")
            model_b_better_button = gr.Button("Model B is better")
            tie_button = gr.Button("Tie")
            both_bad_button = gr.Button("Both are bad")

        # Feedback button actions
        model_a_better_button.click(fn=lambda: set_feedback("Model A is better"), inputs=[], outputs=[])
        model_b_better_button.click(fn=lambda: set_feedback("Model B is better"), inputs=[], outputs=[])
        tie_button.click(fn=lambda: set_feedback("Tie"), inputs=[], outputs=[])
        both_bad_button.click(fn=lambda: set_feedback("Both are bad"), inputs=[], outputs=[])

        # Feedback text field
        user_feedback_motivation = gr.Textbox(label="Feedback", lines=2, placeholder="Type feedback hier...")
        submit_feedback_button = gr.Button("Submit feedback")
        submit_feedback_button.click(fn=handle_feedback, inputs=[user_feedback_motivation], outputs=[])

    with gr.Tab("Leader board"):
        leader_board_button = gr.Button("Leader board")

# Launch the interface
demo.launch(share=True)
