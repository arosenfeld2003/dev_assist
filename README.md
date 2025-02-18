# Dev Assist: Project Overview
A personal development assistant built with the following features:
- Maintains complete privacy by running locally
- Can understand your entire codebase's context locally
- Optional integration with commercial LLMs for general development questions
- Provides fully customizable responses and behavior
- Integrates with your local development environment
- Costs nothing to run (after initial setup)
- Can be extended with your own tools and workflows

## Purpose
Most devs now regularly use tools like GitHub Copilot, Cursor, or web-based interactions with Claude or ChatGPT.
While these are powerful tools, they come with limitations:
- Your code is sent to external servers
- You can't customize their behavior
- They can be expensive for heavy use
- They don't maintain context between sessions
- They can't access your local development environment

This project gives you the power of modern AI assistance while keeping you in control of your data and workflow.

## Key Features (Planned)

- Local LLM integration (Deepseek)
    - Full codebase understanding
    - Local code analysis and processing
- Hybrid LLM approach:
  - Local models for code analysis and sensitive data
  - Optional commercial LLM integration (OpenAI, etc.) for general queries
- Customizable responses and behavior
- Choice of interfaces (Web UI or API)
- Built with Go and Python for performance and flexibility

# dev_assist: planned project structure

dev-assistant/  
├── docker-compose.yml      # Main compose file at root  
├── api/                    # Go API service  
│   ├── Dockerfile  
│   └── ...
├── llm/                    # Python LLM service  
│   ├── Dockerfile  
│   ├── requirements.txt  
│   └── app/  
│       └── ...  
├── web-react/              # React frontend (if we add it later)  
│   ├── Dockerfile  
│   └── ...  
└── README.md  