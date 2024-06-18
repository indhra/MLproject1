## Us the official Python 3.9 image

FROM python:3.7

## set the working directory to /code 
WORKDIR /code

## COPY the current directory contents in the container at /code 
COPY ./requirements.txt /code/requirements.txt
 

## install the requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# set up a new user named 'user'
RUN useradd user
# switch to the 'user' user
USER user 

# set home to the user's home directory 
ENV HOME=/home/user \
    PATH=home/user/.local/bin:$PATH 

# set the working directory to the user's home directory
WORKDIR $HOME/app 

# copy the current directory contents into the container at $home/app setting the owner to 
COPY --chown=user . $HOME/app 

## start the fastapi app on port 7860
CMD ["uvicorn","app:app", "--host", "0.0.0.0","--port","7860"]