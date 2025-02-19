import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import requests
from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

# Vulnerable: Hardcoded credentials (LLM06)
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
MODEL_PATH = "gpt2-large"

class VulnerableLanguageModel:
    def __init__(self):
        # Vulnerable: No validation of model source (LLM05)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        
        # Vulnerable: No rate limiting counter (LLM04)
        self.requests = {}
        
    def preprocess_prompt(self, prompt):
        # Vulnerable: No input validation (LLM01)
        return prompt + " Complete the following:"
    
    def generate_response(self, prompt):
        # Vulnerable: No output validation (LLM02)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.tokenizer.decode(outputs[0])
    
    def train_on_data(self, training_data):
        # Vulnerable: No data validation (LLM03)
        for data in training_data:
            self.model.train()
            loss = self.model(**data).loss
            loss.backward()
