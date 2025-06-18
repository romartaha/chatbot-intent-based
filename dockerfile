# Dockerfile-llama

FROM ubuntu:latest

RUN apt update && apt install -y git-lfs wget build-essential cmake libopenblas-dev

WORKDIR /app

RUN git clone https://github.com/ggerganov/llama.cpp  && \
    cd llama.cpp && \
    make

COPY Qwen3-8B-Q4_K_M.gguf /app/llama.cpp/

EXPOSE 8080

CMD ["./server", "-m", "Qwen3-8B-Q4_K_M.gguf", "--host", "0.0.0.0", "--port", "8080"]