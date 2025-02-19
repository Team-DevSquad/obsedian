import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import numpy as np

# Function to load sensitive keywords and patterns from a file
def load_sensitive_patterns(file_path):
    with open(file_path, "r") as file:
        patterns = [line.strip() for line in file if line.strip()]
    return patterns

# Function to check if a response contains sensitive keywords or matches patterns
def is_vulnerable_rule_based(response, sensitive_patterns):
    response_lower = response.lower()
    for pattern in sensitive_patterns:
        # Check for simple keywords
        if ":" not in pattern and pattern in response_lower:
            return True
        # Check for regex patterns
        if ":" in pattern and re.search(pattern, response_lower):
            return True
    return False

# Function to extract features from responses using TF-IDF
def extract_features(responses):
    vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
    features = vectorizer.fit_transform(responses).toarray()
    return features, vectorizer

# Function to classify responses using clustering
def classify_with_clustering(responses, features, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features)
    return clusters

# Function to classify responses using anomaly detection
def classify_with_anomaly_detection(responses, features):
    iso_forest = IsolationForest(contamination=0.1, random_state=42)  # Adjust contamination as needed
    anomalies = iso_forest.fit_predict(features)
    return anomalies

# Function to classify payloads and identify vulnerable ones
def classify_vulnerable_payloads(responses_file, sensitive_patterns_file, output_file):
    # Load sensitive patterns
    sensitive_patterns = load_sensitive_patterns(sensitive_patterns_file)

    # Load the logged responses
    with open(responses_file, "r") as file:
        data = json.load(file)

    # Extract payloads and responses
    payloads = [item["payload"] for item in data]
    responses = [item["response"] for item in data]

    # Step 1: Rule-based filtering
    rule_based_flags = [is_vulnerable_rule_based(response, sensitive_patterns) for response in responses]

    # Step 2: Extract features using TF-IDF
    features, vectorizer = extract_features(responses)

    # Step 3: Classify using clustering
    clusters = classify_with_clustering(responses, features, n_clusters=2)

    # Step 4: Classify using anomaly detection
    anomalies = classify_with_anomaly_detection(responses, features)

    # Combine results
    vulnerable_payloads = []
    for i in range(len(payloads)):
        if rule_based_flags[i] or clusters[i] == 1 or anomalies[i] == -1:
            vulnerable_payloads.append(payloads[i])

    # Save vulnerable payloads to a file
    with open(output_file, "w") as file:
        for payload in vulnerable_payloads:
            file.write(payload + "\n")

    print(f"Found {len(vulnerable_payloads)} potentially vulnerable payloads.")
    print(f"Vulnerable payloads saved to '{output_file}'.")

# Main function
if __name__ == "__main__":
    # File paths
    responses_file = "responses.json"  # Path to the logged responses
    sensitive_patterns_file = "sensitive_patterns.txt"  # Path to the sensitive patterns file
    output_file = "vulnerable_payloads.txt"  # Path to save the vulnerable payloads

    # Classify and save vulnerable payloads
    classify_vulnerable_payloads(responses_file, sensitive_patterns_file, output_file)