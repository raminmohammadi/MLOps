import requests

# URL of your Flask API
url = 'http://0.0.0.0:4000/predict'  # Update with the actual URL

# Function to get user input
def get_user_input():
    sepal_length = float(input("Enter sepal length: "))
    sepal_width = float(input("Enter sepal width: "))
    petal_length = float(input("Enter petal length: "))
    petal_width = float(input("Enter petal width: "))
    
    return {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }

# Main function
def main():
    print("Enter the measurements for the Iris flower:")
    input_data = get_user_input()
     
    # Send a POST request
    response = requests.post(url, data=input_data)  # Use "data" instead of "json" for form data
    
    # Print the response
    print("HTTP Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    main()
