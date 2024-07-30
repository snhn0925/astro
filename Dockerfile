FROM quay.io/astronomer/astro-runtime:11.7.0
COPY requirements.txt /requirements.txt
RUN python -m pip install --user --upgrade pip
RUN python -m pip install --no-cache-dir --user -r /requirements.txt
