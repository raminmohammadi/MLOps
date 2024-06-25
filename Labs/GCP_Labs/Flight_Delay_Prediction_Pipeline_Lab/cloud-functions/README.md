
# Setting Up a Cloud Function from Google Cloud Console

1. **Navigate to Cloud Functions:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Select **Cloud Functions** from the navigation menu.

2. **Create a New Function:**
   - Click on **Create Function**.

3. **Configure Function Basics:**
   - Enter a name for your function (e.g., `trigger_dag`).
   - Select the **region** where you want to deploy your function.
   - Choose the **runtime** (e.g., Python 3.9).
   - Setup a timeout of more than 5 mins
   - Configure the ENV variables - PROJECT_ID, COMPOSER_ENVIRONMENT, LOCATION, DAG_ID

4. **Set Up the Trigger:**
   - In the **Trigger** section, select **Cloud Pub/Sub**.
   - Choose the Pub/Sub topic you want to trigger the function.

5. **Configure the Function Code:**
   - In the **Source code** section, choose **Inline editor**.
   - Ensure your function code is entered correctly. Use the code in [trigger-dag.py](trigger-dag.py) file.


6. **Specify Dependencies:**
   - Add the dependencies from [requirements.txt](requirements.txt) file.

7. **Set Environment Variables:**
   - In the **Environment variables, networking, timeouts and more** section, add the following environment variables:
     - `PROJECT_ID`: Your Google Cloud project ID
     - `LOCATION`: The location of your Composer environment
     - `COMPOSER_ENVIRONMENT`: Your Composer environment name

8. **Deploy the Function:**
   - Click on **Deploy** to create and deploy your Cloud Function.

### Verifying the Function

1. **Upload a File:**
   - Upload a file to the specified Cloud Storage bucket to trigger the function.

2. **Check Logs:**
   - Go to the **Cloud Functions** section in the Google Cloud Console.
   - Select your function and navigate to the **Logs** tab to see the output and ensure it is working correctly.