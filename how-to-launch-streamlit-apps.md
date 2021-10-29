**How to launch any Streamlit web app in DEV/showcase mode**

1. Launch Anaconda Prompt
2. Activate the conda environment where your project was created
  ```command
     activate <env-name>
  ```
3. Navigate to the folder where the app script is. After `(env-name) C:\Users\USERNAME>`, type:
  ```command
     cd C:\Users\USERNAME\project-folder\project-name
  ```
4. After `(env-name) C:\Users\USERNAME\project-folder\project-name>`, type:
  ```command
     streamlit run <app-filename>.py
  ```
  PS: this will only work if your app.py script is in the project-name folder.</br>
  
5. The command at point 4 will open up a new tab in your default web browser (mine is Microsoft Edge), where you will see your app.
6. If you can't see your app, go back to Anaconda Prompt, where you will see this:
  ```command
     You can now view your Streamlit app in your browser.
     
     Local URL: http://localhost:8502
     
     Network URL: http://192.168.0.14:8502
  ```
  If you copy and paste the Local URL onto your browser, it should show you your app.
  
  Source: https://towardsdatascience.com/a-quick-tutorial-on-how-to-deploy-your-streamlit-app-to-heroku-874e1250dadd

----

**To refresh the app and see any new changes:**</br>
An *i* sign will appear on the top-right. Click on "Rerun" to re-launch the app and see the new changes. 

<img align="left" src="https://user-images.githubusercontent.com/60174218/139415243-eae10eec-4270-4823-8b78-a34999a39e3b.png" width="500" height="100"/></br>
