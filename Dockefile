FROM n8nio/n8n:latest

USER root

# Install Python and required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    musl-dev \
    libffi-dev

# Install Python packages globally
RUN pip3 install --break-system-packages --no-cache-dir \
    openpyxl \
    pillow

# Create scripts directory and copy script
RUN mkdir -p /home/node/scripts
COPY extract_excel_images.py /home/node/scripts/
RUN chmod +x /home/node/scripts/extract_excel_images.py
RUN chown -R node:node /home/node/scripts

USER node

WORKDIR /home/node