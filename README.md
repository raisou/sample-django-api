# sample-api

Example of fast prototyping api

[![Build Status](https://travis-ci.org/raisou/sample-api.svg?branch=master)](https://travis-ci.org/raisou/sample-api)

## Main points

- /api/ : Rest Api
- /admin/ : Path to django admin (need to be superuser)
- /docs/swagger/ : Swagger doc api (main points need to have an authenticated user)
- /docs/redoc/ : Redoc doc api (main points need to have an authenticated user)

## LOCAL ENV WITH DOCKER (Linux)

### **1. Install Docker and Docker-compose**

On Ubuntu pay attention on user rights, it is not recommended to run it as root
<https://docs.docker.com/engine/installation/linux/linux-postinstall/>

The first time you'll use docker-compose it will build and download docker images, it can take a long time.

### **2. Clone this repository**

```bash
git clone git@github.com:raisou/sample-api.git
```

### **3. Set local config files**

create a file local.py in /path/to/project/sample_api/settings/ following the example local.py.example.

A simple copy should work with sane defaults

### **4. To run env in background**

<!-- this command can take some time  -->
```bash
cd /path/to/project/
docker-compose pull && docker-compose up --build -d
```

### **5. Set initial database and data (for dev purpose)**

```bash
cd /path/to/project/
docker exec -it sample_api_back python manage.py reset_db -f
```

### **To stop env**

```bash
docker-compose stop
```
