# Import necessary libraries
from flask import Flask, request, render_template, send_file  # Import Flask and related functions for web development
from PIL import Image  # Import the Python Imaging Library (PIL)
import os  # For os operations

# Define a configuration class for local development
class LocalDevelopmentConfig:
    debug = True  # Set debug mode to True for easier debugging during development

# Define a function to create the Flask application
def create_app():
    # Create a new Flask application instance with a specified template folder
    app = Flask(__name__, template_folder="templates")
    app.secret_key = b'jitesh'  # Set a secret key for session management and security

    # Check the environment variable to determine the configuration
    if os.getenv('ENV', "development") == "production":
        # If the environment is set to production, raise an exception
        raise Exception("Currently no production config is setup.")
    else:
        # If in development mode, print a message to the console
        print("Starting Local Development")
        
        # Load the local development configuration settings
        app.config.from_object(LocalDevelopmentConfig)
    
    # Push the application context to make it available for the app
    app.app_context().push()
    return app  # Return the created Flask application instance

# Create the Flask application instance by calling the create_app function
app = create_app()

# Function to hide a secret message in an image
def hide_message(normal_image, secret_text):
    # Open the image file specified by normal_image
    image = Image.open(normal_image)
    
    # Convert the image into a list of binary data (bytes)
    binary_data = list(image.tobytes())
    
    
    # Convert the secret message into binary format (a string of bits)
    message_binary = ''.join(format(ord(char), '08b') for char in secret_text)
    print(message_binary)

    # Loop through each bit of the message and hide it in the image
    for i, bit in enumerate(message_binary):
        # Modify the least significant bit of the image data to store the message bit
        binary_data[i] = (binary_data[i] & ~1) | int(bit)

    # Convert the modified binary data back into an image
    hidden_image = Image.frombytes(image.mode, image.size, bytes(binary_data))
    
    # Define the path where the hidden image will be saved
    hidden_image_path = r'static\hidden_image.png'
    
    # Save the new image with the hidden message
    hidden_image.save(hidden_image_path)
    
    # Return the path of the saved hidden image
    return hidden_image_path

# Main block to execute the code when the script is run directly
if __name__ == "__main__":
    # Specify the path of the original image where the message will be hidden
    normal_image_path = r'\monalisa.png'  # Change this to your image path
    
    # Define the secret message that you want to hide in the image
    secret_message = "Hello, this is a secret message!"
    
    try:
        # Call the hide_message function to hide the secret message in the image
        result_path = hide_message(normal_image_path, secret_message)
        # Print the path where the hidden image is saved
        print(f"Hidden image saved at: {result_path}")
    except Exception as e:
        # If an error occurs, print the error message
        print(f"An error occurred: {e}")

        


'''
def extract_message(hidden_image):
    # Open the hidden image
    image = Image.open(hidden_image)             # Open the image
    binary_secret_text = ""                      # empty string to  store the extracted message 
    pixels = image.load()
    
    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j][:3]  # Get RGB values (ignore alpha if present)
 '''