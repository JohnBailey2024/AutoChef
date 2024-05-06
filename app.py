import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    st.image('download.jpeg', width = 250)
    st.title("Welcome to the Home of the AutoChef")

    st.subheader("About Our Product")
    st.write("""
        Our automatic recipe generator is a versatile tool designed to provide personalized recipe recommendations based on user's available ingredients.

        Key features of our automatic recipe generator include:
        
        1. **Ingredient-Based Search**: The generator allows users to input available ingredients, and it suggests recipes that utilize those ingredients, reducing food waste and making meal planning more efficient.
        
        2. **Diverse Cuisine Options**: With a vast database of recipes spanning various cuisines, including international and regional dishes, the generator offers a wide range of options to suit different cultural preferences and culinary interests.
        
        3. **Interactive User Interface**: The user-friendly interface makes it easy for users to input their preferences, explore recipe options, and access cooking instructions and ingredient lists.
        
        
        Overall, our automatic recipe generator is a valuable tool for home cooks, food enthusiasts, and anyone looking for inspiration and guidance in the kitchen. Whether you're seeking quick and easy weeknight meals, healthy options for special diets, or adventurous culinary experiments, our generator empowers you to discover and enjoy delicious recipes tailored to your tastes and requirements.
        """)

if __name__ == "__main__":
    main()
