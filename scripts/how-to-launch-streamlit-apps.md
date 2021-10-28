**How to launch any Streamlit web app in DEV/showcase mode**

1. Launch Anaconda Prompt
2. Activate the conda environment where your project was created
  ```command
     activate <env-name>
  ```
3. Navigate to the folder where the app script is. After `(env-name) C:\Users\USERNAME>`, type:
  ```command
     cd C:\Users\USERNAME\project-folder\project-name\scripts
  ```
4. After `(env-name) C:\Users\USERNAME\project-folder\project-name\scripts>`, type:
  ```command
     streamlit run <app-filename>.py
  ```
5. This opens up a new tab in your default web browser (mine is Microsoft Edge), where you will see your app.
6. If you can't see your app, go back to Anaconda Prompt, where you will see this:
  ```command
     You can now view your Streamlit app in your browser.
     
     Local URL: http://localhost:8502
     
     Network URL: http://192.168.0.14:8502
  ```
  If you copy and paste the Local URL onto your browser, it should show you your app.
  
  Source: https://towardsdatascience.com/a-quick-tutorial-on-how-to-deploy-your-streamlit-app-to-heroku-874e1250dadd
     


