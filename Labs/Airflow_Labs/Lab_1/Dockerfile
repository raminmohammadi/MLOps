FROM apache/airflow:2.5.1-python3.7

# Install as airflow user (not root)
USER airflow

# Install packages with --user flag to ensure they go to the right location
RUN pip install --user \
    pandas \
    scikit-learn \
    numpy \
    matplotlib \
    seaborn
    # Any additional packages that might be needed.

# Verify installations
RUN python -c "import pandas; print('pandas:', pandas.__version__)" && \
    python -c "import sklearn; print('sklearn:', sklearn.__version__)" && \
    python -c "import numpy; print('numpy:', numpy.__version__)"