# AutoChef

Welcome to our AutoChef repository! This project aims to provide users with personalized recipe recommendations based on their input ingredients. 

## Team Members

- **John Bailey**: Developed and implemented the Streamlit interface.
- **Nithin Kumar**: Identified and preprocessed the training dataset.
- **James Chung**: Established and formatted the project's GitHub repository.
- **Felix Tong**: Authored the model and backend code.

## Project Overview

Right now, AutoChef takes in a list of ingredients from the user and generates Recipes grounded in similar recipes available in our dataset of over 2M+ recipes.

We utilize a Sentence Transformer to encode our ingredients into embeddings. These are used to retrieve similar recipes, which our LLM, Google Gemini, uses to generate relevant recipes containing the ingredients for the user

### Features

- **Streamlit Interface**: Users can input ingredients via a user-friendly Streamlit interface and receive curated recipe recommendations.
- **Preprocessed Dataset**: The training dataset has been preprocessed to ensure optimal model performance.
- **GitHub Repository**: Our project repository is organized and formatted for efficient collaboration and version control.
- **Model and Backend**: The recommendation system's model and backend code have been developed to enable recipe suggestions based on input ingredients.

## Future Enhancements

Moving forward, our team aims to enhance the system's capabilities by training the model to generate entirely new recipes that only use similar recipes as a method to ensure good taste rather than use them as a template to base ground truth upon.

 We will focus on ensuring that the generated recipes are coherent and palatable, avoiding clashing flavors or inedible combinations.

## Getting Started

## 1. Hugging Face

**Free to test Streamlit sandbox:**

https://huggingface.co/spaces/jlayer3/AutoChef
 

## 2. Local

### Prerequisites

- Python 3.11.x is recommended.

### Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/JohnBailey2024/AutoChef.git
    ```

2. Navigate to the project directory:

    ```bash
    cd /path/to/local/autochef
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Run the Streamlit interface:

    ```bash
    streamlit run app.py
    ```

2. Access the interface by opening the following URL in your web browser:

    ```plaintext
    http://localhost:8501
    ```

3. Input ingredients into the interface to receive recipe recommendations.

