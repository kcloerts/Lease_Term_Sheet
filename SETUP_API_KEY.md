# Setting Up Default Gemini API Key

To configure a default Gemini API key for the application:

1. Create a file named `secrets.toml` in the `.streamlit` directory:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml` and add your Gemini API key:
   ```toml
   [gemini]
   api_key = "your-actual-gemini-api-key-here"
   ```

3. The `secrets.toml` file is automatically excluded from git (in `.gitignore`) to keep your API key secure.

4. When the app runs, it will automatically use this default API key, and users won't need to enter one.

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it into your `secrets.toml` file

## Security Notes

- Never commit `secrets.toml` to version control
- The file is already listed in `.gitignore`
- Users can still override the default API key by checking "Use custom API key" in the sidebar
