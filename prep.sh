#!/usr/bin/env bash

# Install Prerequisites
sudo apt install curl containerd docker.io docker-buildx

# Add user to docker group
sudo usermod -aG docker $USER && newgrp docker
sudo systemctl enable --now docker