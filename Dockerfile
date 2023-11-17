FROM python:3.11

# Copy requirements file.
COPY requirements.txt /tmp/requirements.txt
# COPY requirements-frozen.txt /tmp/requirements-frozen.txt
COPY ./application /var/application

# Run installer commands
RUN pip install -U pip
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /tmp/requirements.txt

WORKDIR /var

CMD ["gunicorn", "-w", "1", "--access-logfile", "-", "-b", ":3000", "-t", "30", "--reload", "application.wsgi:start_app(deploy_as='docker_compose')"]