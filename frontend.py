import streamlit as st
import pickle
import re

# Load the logistic regression model and vectorizer
with open("logistic-regression.pkl", "rb") as lr_file:
    lr_model = pickle.load(lr_file)

with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)          # Remove hyperlinks
    text = re.sub(r'[^\w\s]', '', text)          # Remove punctuations
    text = text.lower()                          # Convert to lowercase
    text = re.sub(r'\s+', ' ', text).strip()     # Remove extra spaces
    return text

# Prediction function
def predict_email(email_text):
    # Preprocess the email text
    email_text = preprocess_text(email_text)

    # Vectorize the text
    email_vector = vectorizer.transform([email_text])

    # Make prediction
    prediction = lr_model.predict(email_vector)

    # Interpret the result
    return "Phishing Mail" if prediction[0] == 0 else "Safe Mail"

# Set the page title and layout
st.set_page_config(page_title="Email Phishing Classifier", layout="wide")

# Add custom CSS to increase space below the heading and modify the text area size
st.markdown(
    """
    <style>
        .main-heading {
            text-align: center;
            font-size: 60px;
            font-weight: bold;
            margin-bottom: 50px; /* Adjust the value for desired spacing */
        }

        /* Increase placeholder text size */
        .stTextArea textarea::placeholder {
            font-size: 20px;  /* Adjust the font size */
        }

        /* Make the text area cover 50% of the vertical height */
        .stTextArea textarea {
            height: 30vh;  /* Adjust height to 40% of the viewport height */
            font-size: 18px;  /* Increase the font size of text inside the text area */
        }

        /* Increase size of the submit button */
        .stButton button {
            font-size: 20px;  /* Increase the font size of button text */
            padding: 15px 40px;  /* Increase padding around the button */
        }

        /* Make the text area label appear as a heading */
        .stTextArea label {
            font-size: 28px;  /* Larger font size */
            font-weight: bold; /* Bold */
            text-align: center;
            display: block;
            margin-bottom: 0px; /* Remove space below the label */
        }

        /* Add a black border around col2 */
        .css-1g8c5wi {  /* Streamlit auto-generated class for col2 */
            border: 2px solid black;  /* Black border with 2px thickness */
            padding: 20px;  /* Add some padding inside the border */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a big heading at the top with custom class
st.markdown(
    """
    <h1 class='main-heading'>
        Email Phishing Classifier
    </h1>
    """,
    unsafe_allow_html=True,
)

# Divide the page into two columns
col1, col2 = st.columns(2)

# Left column: Very big image
with col1:
    st.image(
        "https://cdn.prod.website-files.com/6082ee0e95eb6459d78fac06/65282af97ae4be5ae1873a26_65282aca65ccd0bcf0af3995_Phishing-email-examples-lead-image.webp",  # Replace with your image URL or local path
        # caption="Phishing Detection Illustration",
        use_container_width=True,
    )

# Right column: Email classification functionality
with col2:
    # Display the label as a heading
    st.markdown("<h2>Paste the email content here:</h2>", unsafe_allow_html=True)

    # User input for email content
    email_content = st.text_area("", key="email_content")

    if st.button("Classify"):
        if email_content.strip() == "":
            st.warning("Please provide the email content.")
        else:
            # Perform prediction
            classification = predict_email(email_content)
            st.success(f"The email has been classified as: {classification}")
