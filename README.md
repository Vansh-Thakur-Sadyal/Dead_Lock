# Dead_Lock: AI Faculty Matching System

## Overview

Dead_Lock is an intelligent AI-powered platform designed to connect students with the most suitable faculty members for academic guidance and research collaboration. The system uses advanced natural language processing and machine learning algorithms to analyze student queries, match them with faculty expertise, and facilitate seamless communication through an integrated chat system.

## Features

### 🤖 AI-Powered Query Processing
- **Intelligent Query Refinement**: Uses Llama3 LLM to understand and refine student queries into clear, academic-focused questions
- **Domain Classification**: Automatically categorizes queries by academic domain (Machine Learning, NLP, Cloud Computing, etc.)
- **Difficulty Assessment**: Determines query complexity level (beginner/intermediate/advanced)

### 👥 Smart Faculty Matching
- **Expertise-Based Matching**: Matches students with faculty based on research domains, projects, and publications
- **Scoring Algorithm**: Employs sophisticated scoring mechanisms to find the best faculty-student pairs
- **Load Balancing**: Distributes queries efficiently across available faculty members

### 📚 Research Paper Integration
- **RAG (Retrieval-Augmented Generation)**: Integrates relevant research papers into responses
- **Paper Recommendations**: Suggests academic papers related to student queries
- **Citation Support**: Provides direct links and summaries of research materials

### 💬 Real-Time Chat System
- **Student-Faculty Communication**: Direct messaging between matched pairs
- **Session Management**: Organized chat sessions with topic tracking
- **Status Tracking**: Monitors chat request status (pending/accepted/declined/expired)

### 🔐 Authentication & Security
- **Role-Based Access**: Separate authentication for students and faculty
- **Secure Password Hashing**: Industry-standard password security
- **Session Management**: Secure user sessions with proper validation

### 📊 Analytics & Feedback
- **Response Time Tracking**: Monitors faculty response times
- **Rating System**: Students can rate faculty responses
- **Feedback Collection**: Continuous improvement through user feedback

## Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Robust relational database
- **Ollama + Llama3**: Local LLM for AI processing
- **httpx**: Async HTTP client for external API calls

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: Lightweight client-side interactions
- **Custom CSS Variables**: Consistent theming system

### AI/ML Components
- **Query Processor**: NLP-based query analysis
- **Faculty Matcher**: ML-powered matching algorithm
- **RAG Controller**: Research paper retrieval system
- **Response Builder**: Intelligent response generation

## Project Structure

```
├── app/
│   ├── api/                 # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   ├── chat.py         # Chat functionality
│   │   ├── faculty.py      # Faculty management
│   │   ├── health.py       # Health checks
│   │   └── student.py      # Student operations
│   ├── core/               # Core business logic
│   │   ├── auth_deps.py    # Authentication dependencies
│   │   ├── matcher.py      # Faculty matching algorithm
│   │   ├── scoring.py      # Scoring mechanisms
│   │   └── chatbot/        # AI chatbot components
│   ├── db/                 # Database layer
│   │   ├── crud.py         # Database operations
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   └── seed.py         # Database seeding
│   ├── services/           # External services
│   │   ├── embeddings.py   # Text embeddings
│   │   ├── faculty_service.py # Faculty operations
│   │   ├── llm.py          # LLM integration
│   │   └── papers.py       # Research paper service
│   ├── system/             # System utilities
│   │   ├── feedback.py     # Feedback system
│   │   ├── routing.py      # Request routing
│   │   └── tracker.py      # Analytics tracking
│   └── utils/              # Utilities
│       ├── constants.py    # Application constants
│       ├── helpers.py      # Helper functions
│       └── logger.py       # Logging configuration
├── scripts/                # Utility scripts
│   ├── generate_data.py    # Data generation
│   ├── init_db.py          # Database initialization
│   └── seed_data.py        # Data seeding
├── index (1).html          # Frontend interface
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Ollama with Llama3 model
- Node.js (optional, for frontend development)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vansh-Thakur-Sadyal/Dead_Lock.git
   cd Dead_Lock
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3
   ```

5. **Configure database**
   - Create a PostgreSQL database
   - Update database URL in `app/config.py`

6. **Initialize database**
   ```bash
   python scripts/init_db.py
   python scripts/seed_data.py
   ```

7. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Open the HTML file**
   - The frontend is served as a static file
   - Access via `http://localhost:8000/index (1).html` when backend is running

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Student Operations
- `POST /student/query` - Submit academic query
- `GET /student/history` - Query history
- `POST /student/rate` - Rate faculty response

### Faculty Operations
- `GET /faculty/profile` - Get faculty profile
- `PUT /faculty/profile` - Update faculty profile
- `GET /faculty/queries` - Assigned queries

### Chat System
- `POST /chat/request` - Request chat with faculty
- `GET /chat/sessions` - Get chat sessions
- `POST /chat/message` - Send message
- `GET /chat/messages/{session_id}` - Get messages

### Health Check
- `GET /health` - System health status

## Usage

1. **Student Workflow**:
   - Register/Login as student
   - Submit academic query
   - Receive faculty match with research papers
   - Engage in chat for detailed guidance
   - Rate the interaction

2. **Faculty Workflow**:
   - Register/Login as faculty
   - Update profile with expertise areas
   - Receive and respond to student queries
   - Participate in chat sessions

## Configuration

Key configuration options in `app/config.py`:
- Database connection string
- Ollama model settings
- JWT secret key
- CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- [ ] Mobile application
- [ ] Video conferencing integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Integration with academic databases
- [ ] Automated scheduling system

## Contact

For questions or support, please open an issue on GitHub or contact the development team.