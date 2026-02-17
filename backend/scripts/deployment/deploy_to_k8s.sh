#!/bin/bash
echo "Deploying to Kubernetes..."
kubectl apply -f backend/docker/kubernetes/namespaces/
kubectl apply -f backend/docker/kubernetes/deployments/
echo "Deployment initiated."
