import google.generativeai as genai
import streamlit as st
import re
import os
from dotenv import load_dotenv

class HiringAssistant:
    """
    Hiring Assistant chatbot for TalentScout.
    Handles conversation flow: greeting, info gathering, tech stack, questions, end.
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("Please set GOOGLE_API_KEY in .env file.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')

        self.messages = [
            {"role": "assistant", "content": "Hello! I'm the TalentScout Hiring Assistant. I'll help screen you for tech positions. Let's start with your full name."}
        ]
        self.state = "gathering_info"
        self.candidate_info = {}
        self.questions = []
        self.current_question_index = 0
        self.info_fields = ['name', 'email', 'phone', 'experience', 'position', 'location']
        self.current_field_index = 0

    def process_input(self, user_input):
        """
        Process user input based on current state.
        """
        self.messages.append({"role": "user", "content": user_input})


        if self.check_exit(user_input):
            self.end_conversation()
            return

        if self.state == "gathering_info":
            self.gather_info(user_input)
        elif self.state == "tech_stack":
            self.handle_tech_stack(user_input)
        elif self.state == "answering_questions":
            self.handle_answer(user_input)
        else:
            self.fallback(user_input)

    def check_exit(self, input_text):
        """
        Check if user wants to exit.
        """
        exit_keywords = ['bye', 'exit', 'quit', 'goodbye', 'end']
        return any(keyword in input_text.lower() for keyword in exit_keywords)

    def gather_info(self, user_input):
        """
        Gather candidate information sequentially.
        """
        field = self.info_fields[self.current_field_index]
        self.candidate_info[field] = user_input
        self.current_field_index += 1

        if self.current_field_index < len(self.info_fields):
            next_field = self.info_fields[self.current_field_index]
            prompts = {
                'email': "What's your email address?",
                'phone': "What's your phone number?",
                'experience': "How many years of experience do you have?",
                'position': "What desired position(s) are you applying for?",
                'location': "What's your current location?"
            }
            self.messages.append({"role": "assistant", "content": prompts.get(next_field, f"What's your {next_field}?")})
        else:
            self.state = "tech_stack"
            self.messages.append({"role": "assistant", "content": "Great! Now, please list your tech stack (programming languages, frameworks, databases, tools). Separate by commas."})

    def handle_tech_stack(self, user_input):
        """
        Handle tech stack input and generate questions.
        """
        tech_stack = [tech.strip() for tech in user_input.split(',') if tech.strip()]
        self.candidate_info['tech_stack'] = tech_stack
        self.generate_questions()
        self.state = "answering_questions"
        if self.questions:
            self.messages.append({"role": "assistant", "content": f"Thanks! Here are some technical questions based on your tech stack:\n\n{self.questions[0]}"})
        else:
            self.end_conversation()

    def generate_questions(self):
        """
        Generate technical questions based on tech stack.
        """
        tech_stack = self.candidate_info.get('tech_stack', [])
        if not tech_stack:
            self.questions = []
            return

        # Generate questions for each tech
        question_templates = [
            "Describe your experience with {tech}.",
            "What challenges have you faced when working with {tech}?",
            "How would you explain {tech} to a beginner?",
            "What are the key features of {tech} that you find most useful?",
            "Can you give an example of a project where you used {tech}?"
        ]
        
        self.questions = []
        for i, tech in enumerate(tech_stack):
            if i >= 5:  # Limit to 5 questions
                break
            template = question_templates[i % len(question_templates)]
            self.questions.append(template.format(tech=tech.strip()))

    def handle_answer(self, user_input):
        """
        Handle answer to current question.
        """
        # Store answer (in real app, save to database)
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.messages.append({"role": "assistant", "content": f"Next question:\n\n{self.questions[self.current_question_index]}"})
        else:
            self.end_conversation()

    def end_conversation(self):
        """
        End the conversation gracefully.
        """
        self.state = "ended"
        self.messages.append({"role": "assistant", "content": "Thank you for your time! We'll review your information and get back to you soon. Goodbye!"})
        # Simulate saving data
        self.save_candidate_data()

    def save_candidate_data(self):
        """
        Save candidate data (simulated).
        """
        # In real app, save to secure database
        print("Candidate data:", self.candidate_info)

    def fallback(self, user_input):
        """
        Handle unrecognized input.
        """
        self.messages.append({"role": "assistant", "content": "I'm sorry, I didn't understand that. Please provide the requested information or say 'bye' to exit."})