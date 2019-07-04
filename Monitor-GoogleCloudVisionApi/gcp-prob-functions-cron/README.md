# App Engine Cron with Google Cloud Functions

Google App Engine provides a Cron service. Using this service for scheduling, you can build an application to
reliably schedule tasks which can trigger Google Cloud Functions for prob google vision.

This project contains one components:

* An App Engine application, that uses App Engine Cron Service
    to call Cloud Functions HTTP URLs with a specified Header for validation.


## Configuration

By default this we triggers every 1 minutes. If you want to
customize this schedule for your app then you can modify the [cron.yaml](/appengine/cron.yaml).

For details on configuring this, please see the [cron.yaml Reference](https://cloud.google.com/appengine/docs/standard/python/config/cronref)
in the App Engine documentation.

## Deploying

### 1. Deploy to App Engine

   1. open the `gcloud` cloud shell command-line tool in the desired project or set your project.
        ```
        $ gcloud config set project <your-project-id>
        ```
   2. Create a directory  `appengine/`
        ```
        $ mkdir appengine/
        ```
   3. Upload the appengine/* files to cloud shell
    
   4. Moves the file to appengine directory 
        ```
        mv cron.yaml app.yaml main.py requirements.txt appengine/
        cd appengine
        ```
   5. Deploy the application to App Engine and stop previous version.
        ```
        $ gcloud app deploy --quiet --stop-previous-version app.yaml cron.yaml
        ```

   7. Open [Google Cloud Logging](https://console.cloud.google.com/logs/viewer) and in the right dropdown select "GAE Application". If you don't see this option, it may mean that App Engine is still in the process of deploying.

### Local Testing

Create isolated Python environments using virtualenv

Install virtualenv via pip:

```
pip3 install virtualenv
```

Test your installation


```
virtualenv --version
```

1. Create a virtual environment for a project:

    ```
    mkdir -p ~/virtualenv/
    cd  ~/virtualenv/
    virtualenv appengine
    ```
    
    virtualenv appengine will create a folder in the current directory which will contain the Python executable files,
    and a copy of the pip library which you can use to install other packages. 

2. To begin using the virtual environment, it needs to be activated:

    ```
    source ~/virtualenv/appengine/bin/activate
    ```

    Install packages and export Google API_KEY:
    
    ```
    pip install datadog
    pip install -r requirements.txt
    export API_KEY=xxxxx
    ```

3. If you are done working in the virtual environment for the moment, you can deactivate it:
    
    ```
    deactivate
    ```