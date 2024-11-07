# RAG Dockerfile (rag.Dockerfile)
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy the environment file for Conda
COPY rag_environment.yml .

# Install dependencies using the Conda environment
RUN conda env create -f rag_env.yml

# Ensure the Conda environment is activated
RUN echo "source activate rag_env" > ~/.bashrc
ENV PATH /opt/conda/envs/rag_env/bin:$PATH

# Copy the RAG application code
COPY . .

# Expose the port that the RAG service will run on
EXPOSE 8001

# Run the RAG service (with FastAPI and Uvicorn)
CMD ["uvicorn", "rag_app.main:app", "--host", "0.0.0.0", "--port", "8001"]
