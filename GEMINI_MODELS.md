# Gemini API Model Information

## Supported Models

This application uses Google's Gemini API for AI-powered lease analysis. The following models are supported:

### Free Tier Models
- **gemini-1.5-flash** (Recommended) - Fast and efficient, ideal for most use cases
- **gemini-1.5-pro** - More powerful model (may have rate limits on free tier)
- **gemini-pro** - Legacy model, still supported

## Common Issues

### Model Not Found Error

If you receive an error like:
```
Error generating term sheet: 404 models/gemini-1.5-flash-latest is not found for API version v1beta
```

This means the model name is incorrect. The application has been updated to use the correct model name: `gemini-1.5-flash` (without the `-latest` suffix).

### Solution
The latest version of the application uses the correct model name. Make sure you're running the latest version of the code.

### Checking Available Models

If you encounter model-related errors, the application will automatically try to list available models for your API key and display them in the error message.

## API Key Requirements

- Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- The free tier supports all the models listed above
- Rate limits apply based on your tier

## More Information

For more details about Gemini models and their capabilities, visit:
- [Google AI for Developers](https://ai.google.dev/)
- [Gemini API Documentation](https://ai.google.dev/docs)
