# Build with: docker build -f Dockerfile -t my_blog:latest .
# Run with: docker run --rm -it -p 8080:8080 my_blog:latest
FROM python:latest

COPY . /tmp
WORKDIR /tmp
RUN python setup.py bdist_wheel

WORKDIR /my_blog
RUN mv /tmp/dist/my_blog*.whl .

# NOTE: . venv/bin/activate will not work as expected
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV /my_blog/venv
RUN python -m venv $VIRTUAL_ENV
# Sets the virtual env path first
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install my_blog*.whl
RUN pip install waitress
ENV FLASK_APP my_blog
RUN flask init-db
# NOTE: Looks like /venv/var is not the directory for the instance
RUN python -c 'import os; print(f"SECRET_KEY = {os.urandom(16)}")' > /my_blog/venv/lib/python3.7/site-packages/instance/config.py
# https://stackoverflow.com/questions/22111060/what-is-the-difference-between-expose-and-publish-in-docker
EXPOSE 8080

# The ENTRYPOINT specifies a command that will always be executed when
# the container starts
ENTRYPOINT [ "waitress-serve" ]
# The CMD specifies arguments that will be fed to the ENTRYPOINT
CMD [ "--call", "my_blog:create_app" ]
