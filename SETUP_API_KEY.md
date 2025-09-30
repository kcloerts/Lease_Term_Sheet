# Setting Up Gemini API Key

This Flask application supports two methods for configuring your Gemini API key:

## Method 1: Environment Variable (Recommended)

Set the `GEMINI_API_KEY` environment variable:

### Linux/Mac:
```bash
export GEMINI_API_KEY="your-actual-gemini-api-key-here"
```

### Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your-actual-gemini-api-key-here
```

### Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your-actual-gemini-api-key-here"
```

### Using a .env file:

Create a `.env` file in the project root directory:
```
GEMINI_API_KEY=your-actual-gemini-api-key-here
SECRET_KEY=your-secret-key-for-flask-sessions
```

Note: The `.env` file is automatically excluded from git (in `.gitignore`) to keep your API key secure.

## Method 2: Web Interface

If you prefer not to set an environment variable, you can enter your API key directly in the web application:

1. Start the Flask app
2. Navigate to the home page
3. Enter your API key in the "API Key Configuration" section
4. Click "Set API Key"

The API key will be stored in your session (not saved to disk) and will persist until you close your browser or clear the session.

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and use one of the methods above to configure it

## Security Notes

- Never commit API keys to version control
- The `.env` file is already listed in `.gitignore`
- API keys entered via the web interface are stored only in the session and are not saved to disk
- Use environment variables for production deployments
- Always keep your API key secure and never share it publicly
