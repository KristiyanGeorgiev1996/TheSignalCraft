# Configuration

## Overview

TheSignalCraft uses environment-based configuration to manage sensitive data and runtime settings.

This approach improves security, portability, and overall project hygiene by keeping secrets outside the source code.

---

## Required Environment Variables

The project currently requires the following environment variable:

```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

This token is required to initialize and run the Telegram bot.

---

## Local Setup

Create a `.env` file in the root of the project:

```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

A template file is also provided:
```
.env.example
```

---

## How Configuration Works

- The application reads environment variables at runtime  
- Sensitive values are not stored directly in the codebase  
- The `.env` file is used locally but should not be committed  

---

## Security Best Practices

The following should **not** be committed to the repository:

- `.env` (with real values)  
- API keys or tokens  
- local logs containing sensitive data  

Only `.env.example` should be included as a template.

---

## Running the Application

After setting the required environment variables, start the bot with:

```bash
py app/main.py
```

---

## Future Improvements

Possible configuration improvements include:

- support for multiple environments (development / production)  
- validation of required variables at startup  
- centralized configuration management  
- optional feature flags  

---

## Summary

The current configuration approach is simple, secure, and aligned with common software development practices.

It ensures that sensitive data is separated from the codebase while keeping setup straightforward.
