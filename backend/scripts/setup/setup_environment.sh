#!/bin/bash
echo "Setting up Citizen Zero Environment..."
# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Docker could not be found"
    exit 1
fi
echo "Environment Setup Complete."
