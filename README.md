# Dev Assist: Project Overview
A personal development assistant built with the following features:
- Maintains complete privacy by running locally
- Can understand your entire codebase's context
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
- Customizable responses and behavior
- Choice of interfaces (Web UI or API)
- Built with Go and Python for performance and flexibility

# dev_assist: planned project structure

dev-assistant/  
├── docker/  
│   ├── api/  
│   │   └── Dockerfile        # Go API Dockerfile  
│   ├── llm/  
│   │   └── Dockerfile        # Python LLM service Dockerfile  
│   ├── web-react/  
│   │   └── Dockerfile        # React frontend Dockerfile  
│   └── docker-compose.yml  
│  
├── api/                      # Go API service  
│   ├── cmd/  
│   │   └── main.go          # Entry point  
│   ├── internal/  
│   │   ├── auth/            # Authentication logic  
│   │   ├── handlers/        # HTTP handlers  
│   │   ├── models/          # Data models  
│   │   └── service/         # Business logic  
│   └── web/                 # Go-served web interface  
│       ├── static/          # Static assets  
│       │   ├── css/  
│       │   └── js/  
│       └── templates/       # Go HTML templates  
│  
├── web-react/               # React frontend  
│   ├── src/  
│   │   ├── components/  
│   │   ├── pages/  
│   │   └── App.tsx  
│   └── package.json  
│  
├── llm/                     # Python LLM service  
│   ├── app/  
│   │   ├── __init__.py  
│   │   ├── inference.py     # LLM inference logic  
│   │   └── security.py      # Security utilities  
│   └── requirements.txt  
│  
├── README.md  
└── .gitignore  