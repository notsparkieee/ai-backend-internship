# 🤖 AI-Powered RAG Backend System

A production-ready **Retrieval-Augmented Generation (RAG)** backend built with FastAPI, featuring intelligent document processing, user-specific semantic search, and hybrid routing with LangGraph agents.

## 📋 Overview

This system combines modern NLP techniques with traditional databases to provide intelligent document retrieval and question answering. It processes documents (PDF/images), chunks them per-user, embeds them using sentence-transformers, and routes queries through a multi-agent system powered by Azure OpenAI.

### Key Features

- **🔐 User Management**: Complete user CRUD operations with MySQL storage
- **📄 Document Processing**: OCR support for PDFs and images using Tesseract
- **✂️ Smart Chunking**: User-specific document chunking with configurable chunk sizes
- **🧠 Semantic Embeddings**: Sentence-transformers for high-quality vector representations
- **🔍 Hybrid Search**: FAISS vector store with semantic similarity search
- **🤖 Multi-Agent System**: LangGraph-powered routing with intent classification
- **☁️ Azure OpenAI Integration**: Production-ready LLM connectivity
- **🐳 Docker Support**: Fully containerized with Docker Compose

## 🏗️ Architecture

```
┌─────────────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │
   ┌───┴────┐
   │ Routes │
   └───┬────┘
       │
   ┌───┴──────────────────┐
   │                      │
┌──▼───────┐     ┌───────▼────┐
│  MySQL   │     │   FAISS    │
│ Database │     │   Vector   │
│ (Users & │     │   Store    │
│   Docs)  │     │            │
└──────────┘     └─────┬──────┘
                       │
                ┌──────▼───────┐
                │  LangGraph   │
                │    Agents    │
                │              │
                │ ┌──────────┐ │
                │ │ Intent   │ │
                │ │Classifier│ │
                │ └────┬─────┘ │
                │      │       │
                │   ┌──┴───┐   │
                │   │Route │   │
                │   └──┬───┘   │
                │      │       │
                │ ┌────▼─────┐ │
                │ │Retrieval │ │
                │ │  Answer  │ │
                │ └──────────┘ │
                └──────────────┘
                       │
                ┌──────▼───────┐
                │ Azure OpenAI │
                │  (GPT-4)     │
                └──────────────┘
```

## 🛠️ Tech Stack

**Backend Framework**
- FastAPI 0.109.0
- Uvicorn with async support

**Database & Storage**
- MySQL (via SQLAlchemy 2.0.25)
- FAISS (CPU) for vector search

**AI & ML**
- Azure OpenAI (GPT-4)
- Sentence-Transformers 2.3.1
- LangChain 0.1.6
- LangGraph 0.0.20

**Document Processing**
- Tesseract OCR
- Pillow (PIL) for image processing
- pdf2image for PDF conversion

## 📦 Installation

### Prerequisites

- Python 3.11+
- MySQL Server
- Tesseract OCR ([Download](https://github.com/UB-Mannheim/tesseract/wiki))
- Docker Desktop (for containerized deployment)

### Local Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-backend-internship
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
# Database Configuration
DATABASE_URL=mysql+mysqlconnector://root:your_password@localhost:3306/your_database

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Tesseract Path (Windows)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

5. **Initialize the database**
```bash
python app/create_tables.py
```

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Ensure Docker Desktop is running**

2. **Build and start the container**
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Docker Configuration

The setup uses:
- **Base Image**: Python 3.11-slim
- **Tesseract OCR**: Pre-installed in container
- **MySQL**: Connects to host machine via `host.docker.internal`
- **FAISS Index**: Volume-mounted for persistence

For detailed Docker setup and troubleshooting, see [DOCKER_SETUP.md](DOCKER_SETUP.md)

### Common Docker Issues

**Corporate Proxy TLS Errors**
If you encounter "TLS handshake timeout" or similar proxy issues, create `~/.docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
Then restart Docker Desktop.

## 📚 API Endpoints

### Users

- **POST** `/users` - Create a new user
- **GET** `/users` - List all users
- **GET** `/users/{user_id}` - Get user by ID

### Documents

- **POST** `/documents` - Create document metadata
- **POST** `/upload/{user_id}` - Upload and process document
- **GET** `/documents/{user_id}` - Get user's documents
- **DELETE** `/documents/{doc_id}` - Delete document

### Vector Store

- **POST** `/index/{user_id}/{doc_id}` - Index document chunks
- **POST** `/search/{user_id}` - Search similar chunks

### RAG Agent

- **POST** `/ask` - Ask a question with intelligent routing
  ```json
  {
    "user_id": 1,
    "question": "What is the main topic of my documents?"
  }
  ```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 📁 Project Structure

```
ai-backend-internship/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application
│   ├── database.py              # Database connection
│   ├── vector_store.py          # FAISS operations
│   ├── agents/                  # LangGraph agent system
│   │   ├── graph.py            # Agent orchestration
│   │   ├── intent_classifier.py # Intent detection
│   │   ├── retrieval_node.py   # Vector retrieval
│   │   └── answer_node.py      # Answer generation
│   ├── llm/                    # Azure OpenAI clients
│   │   ├── azure_client.py     # Client initialization
│   │   └── embedding.py        # Embedding generation
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   └── document.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   └── document.py
│   ├── services/               # Business logic
│   │   └── document_system.py
│   └── utils/                  # Helper functions
│       └── chunking.py
├── tests/                      # Test suite
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### Chunk Size Configuration

Modify chunk sizes in [app/utils/chunking.py](app/utils/chunking.py):
```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    # Adjust chunk_size and overlap as needed
```

### Vector Store Settings

Configure FAISS in [app/vector_store.py](app/vector_store.py):
```python
dimension = 384  # Sentence-transformer embedding size
index = faiss.IndexFlatL2(dimension)
```

### Agent Routing

Customize intent classification in [app/agents/intent_classifier.py](app/agents/intent_classifier.py)

## 🚀 Deployment

### Production Checklist

- [ ] Update `.env` with production credentials
- [ ] Configure proper MySQL host (not localhost)
- [ ] Enable HTTPS with reverse proxy (nginx/Caddy)
- [ ] Set up persistent volume for FAISS index
- [ ] Configure logging and monitoring
- [ ] Enable CORS for frontend domains
- [ ] Set up CI/CD pipeline
- [ ] Configure backup strategy for MySQL and vector store

### Environment Variables for Production

```env
# Production MySQL
DATABASE_URL=mysql+mysqlconnector://user:pass@prod-db:3306/database

# Azure OpenAI (Production)
AZURE_OPENAI_API_KEY=prod_key_here
AZURE_OPENAI_ENDPOINT=https://prod-resource.openai.azure.com/

# Security
SECRET_KEY=your_secret_key_for_jwt
```

## 🐛 Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'email_validator'"**
- Solution: `pip install email-validator==2.1.0.post1`

**Issue: "TypeError: Client.__init__() got an unexpected keyword argument 'proxies'"**
- Solution: Update openai library: `pip install openai>=2.14.0`

**Issue: FAISS index not persisting**
- Solution: Check volume mounts in docker-compose.yml

**Issue: MySQL connection refused**
- Solution: Verify MySQL is running and credentials are correct

## 📝 License

This project is part of an internship assignment. All rights reserved.

## 👥 Contributing

This is an internship project. For questions or suggestions, please contact the maintainer.

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Docs](https://python.langchain.com/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

---

**Built with ❤️ using FastAPI, LangChain, and Azure OpenAI**
