# AI-Powered Email Processor

This project contains an AI-powered email processor system, designed to automatically fetch, process and respond to customer emails.

## Overview

The system uses IMAP to fetch unread emails, processes them using an AI model, and automatically sends responses based on the AI's evaluation. The email processor can be useful for automating responses to common customer inquiries or complaints, reducing the load on customer service staff and providing faster responses.

## Main Components

### Main.py

This is the entry point for the application. It orchestrates the whole email fetching and processing mechanism.

### Extraction.py

This module contains the logic for extracting relevant information from emails. It parses the emails and extracts key information such as the sender's name and the issue reported by the customer.

### Support.py

This module interacts with the AI model. It processes the extracted email information and evaluates the appropriate response to be sent to the customer.

## How to Use

1. Clone the repository.
2. Update the `.env` file with your email credentials and AI model API key.
3. Run the `main.py` script.

Please note that the AI model API key must be obtained separately. The email server should support IMAP for fetching the emails.

The system will fetch all unread emails, extract key information, process it with the AI model, and send a response to each email. The emails will be marked as read after processing.
