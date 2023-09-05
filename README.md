# Embedding Upsampling Project

## Table of Contents

1. [Overview](#overview)
2. [Prompt](#prompt)
3. [Task](#task)
4. [ML Problem](#ml-problem)
5. [Data Files](#data-files)
6. [Installation and Setup](#installation-and-setup)
7. [Code Structure](#code-structure)
8. [Usage](#usage)
9. [Testing](#testing)

## Overview

Welcome to the Embedding Upsampling project for Connectly. The primary objective is to design, build, train, and ship ML models. You're given a week to complete this take-home assignment. Once you're done, please share your solution and schedule a 1-hour meeting to discuss it.

## Prompt

ML engineers at Connectly handle both modeling and infrastructure work. This project aims to test your skills in these areas.

## Task

Your main task is to go through the full ML lifecycle, starting from ideation all the way to deployment.

## ML Problem

You're provided with 32-dimensional embeddings that have been transformed from their original 1536-dimensional state through a mystery affine transformation. Your job is to upsample these back to 1536 dimensions while preserving the cosine angles between the original vectors.

## Data Files

1. [Training Embeddings](https://cdn.connectly.ai/interview_prompts/ml_embedding_upsample/projected_train_embs.npy)
2. [Cosine Angle Similarity Matrix](https://cdn.connectly.ai/interview_prompts/ml_embedding_upsample/og_train_cos_theta.npy)

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/nturmel/embedding-upsampling.git

# Navigate into the directory
cd embedding-upsampling

# Install required packages
poetry install
```

## Code Structure

- `main.ipynb`: Jupyter notebook containing the main code and logic.
- `requirements.txt`: List of Python packages required for the project.

## Usage

To run the code, simply open `connectly.ipynb` in a Jupyter Notebook environment and execute the cells.

## Testing

The last section of `connectly.ipynb` includes code to test the model on a test dataset.
