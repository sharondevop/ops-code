### Prerequisite
Build the Docker file and push it to your repository in aws "prob-google-vision"

```
docker build -t probe-google-vision .
docker tag probe-google-vision:latest xxxx.dkr.ecr.eu-west-1.amazonaws.com/probe-google-vision:latest
docker push xxxx.dkr.ecr.eu-west-1.amazonaws.com/probe-google-vision:latest
```

### Cronjob Deployment

```
kubectl apply -f job/cronJob.yml
```

### Check jobs
```
kubectl get cronjob
```

### See the spec for a given object using kubectl explain

```
kubectl explain --api-version="batch/v1beta1" cronjobs.spec
```


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
    virtualenv k8s-docker
    ```
    
    virtualenv k8s-docker will create a folder in the current directory which will contain the Python executable files,
    and a copy of the pip library which you can use to install other packages. 

2. To begin using the virtual environment, it needs to be activated:

    ```
    source ~/virtualenv/k8s-docker/bin/activate
    ```

    Install packages as usual, for example:
    
    ```
    pip install datadog
    pip install -r requirements.txt
    ```

3. If you are done working in the virtual environment for the moment, you can deactivate it:
    
    ```
    deactivate
    ```
