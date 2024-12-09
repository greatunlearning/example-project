# LLM-Assisted Development Example: Whisper API

## The Great Unlearning

This project is part of the [Great Unlearning initiative](https://github.com/greatunlearning), which explores new patterns and principles for LLM-assisted software development. We're rethinking traditional software engineering practices in the context of AI pair programming.

### Why This Project?

Traditional software development principles like DRY (Don't Repeat Yourself), information hiding, and deep inheritance hierarchies were designed for human-only development. With LLM-assisted coding, we need to reconsider these patterns. This project serves as a practical example of new approaches like:

- **Prompt-Oriented Architecture (POA)**: Structuring code around natural language descriptions
- **Context Window Optimization (CWO)**: Organizing code to fit LLM context limitations
- **Self-Regenerating Modules (SRM)**: Designing components to be easily recreated
- **LLM-Friendly Documentation Pattern (LFDP)**: Documentation that serves both humans and AI

### Project Structure

Our repository follows these new patterns:
```
├── GUIDELINES.md       # LLM interaction rules
├── HOWTO_LLM.md       # Guide for LLM collaboration
├── JOURNAL.md         # Development decisions & progress
├── PROMPT_TEMPLATE.md # Templates for LLM interaction
├── TODO.md           # Project roadmap
└── src/
    ├── feature/
    │   ├── intent.md        # Purpose in natural language
    │   ├── implementation/  # Actual code
    │   ├── prompts/        # Common modification prompts
    │   └── tests/          # Self-contained tests
```

Each component is designed to be:
- Self-contained with clear context
- Easy to understand by both humans and LLMs
- Regenerable through prompts
- Well-documented with its purpose and boundaries

### Development Philosophy

This project embraces several key principles:
1. **Context Over Reuse**: Prioritizing understandability within context windows
2. **Explicit Over Implicit**: Making intentions and dependencies clear
3. **Natural Language First**: Designing around human communication
4. **Self-Contained Modules**: Each component tells its complete story
5. **AI-Friendly Documentation**: Documentation that serves both human and AI readers

---

# Whisper API Implementation

## Project Overview

This is a REST API service for OpenAI's Whisper speech-to-text model, featuring:

### Core Functionality
- 🎯 Audio transcription using OpenAI's Whisper model
- 🌐 Support for multiple languages
- 🔄 Background processing with progress tracking
- 📊 Multiple output formats (JSON, SRT, VTT, TXT)
- 📝 Word-level timestamps
- 🎛️ Configurable transcription parameters

### Technical Features
- 🚀 FastAPI-based REST API
- 🐳 Docker containerization with multi-stage builds
- 🔒 Secure file handling
- 📈 Progress monitoring
- 💾 Persistent storage for transcripts
- 🎮 GPU support (optional)

## Prerequisites

- Docker
- (Optional) NVIDIA GPU with CUDA support
- At least 2GB of free disk space for models
- Sufficient storage for audio files and transcripts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/greatunlearning/example-project.git
cd whisper-api
```

2. Build the Docker image:
```bash
# CPU version
docker build -t whisper-api .

# GPU version (if you have NVIDIA GPU)
docker build -t whisper-api:gpu .
```

## Running the Service

### Basic Usage
```bash
docker run -d \
  --name whisper-service \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/transcripts:/app/transcripts \
  whisper-api
```

### With GPU Support
```bash
docker run -d \
  --name whisper-service \
  --gpus all \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/transcripts:/app/transcripts \
  whisper-api:gpu
```

## API Endpoints

### Transcription Operations

#### Start Transcription
```http
POST /transcribe
```
Start a new transcription job with customizable parameters.

Parameters:
- `file`: Audio file (multipart/form-data)
- `params`: JSON object with transcription options:
  - `language`: Source language code (optional)
  - `model`: Model size ('tiny', 'base', 'small', 'medium', 'large')
  - `task`: 'transcribe' or 'translate'
  - `output_format`: Array of desired formats ('json', 'srt', 'vtt', 'txt')
  - Additional options (see API documentation)

Example:
```bash
curl -X POST http://localhost:8000/transcribe \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.mp3" \
  -F 'params={"model":"base","language":"en","output_format":["txt","srt"]}'
```

#### List Transcriptions
```http
GET /transcripts
```
Retrieve a list of all transcription jobs.

#### Get Transcription Status
```http
GET /transcripts/{transcript_id}
```
Check the status and progress of a specific transcription.

#### Download Transcript
```http
GET /transcripts/{transcript_id}/download?format={format}
```
Download the completed transcript in the specified format.

#### Delete Transcript
```http
DELETE /transcripts/{transcript_id}
```
Remove a transcription and its associated files.

### System Information

#### List Available Models
```http
GET /models
```
Get information about available Whisper models.

#### List Supported Languages
```http
GET /languages
```
Get a list of supported languages.

## Configuration Options

### Transcription Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|----------|
| language | Source language | auto-detect | ISO language codes |
| model | Whisper model size | "base" | "tiny", "base", "small", "medium", "large" |
| task | Transcription task | "transcribe" | "transcribe", "translate" |
| output_format | Output formats | ["json"] | "json", "srt", "vtt", "txt" |
| word_timestamps | Enable word timing | false | true/false |
| vad_filter | Voice activity detection | true | true/false |
| temperature | Sampling temperature | 0.0 | 0.0-1.0 |
| beam_size | Beam search size | 5 | integer |

## File Storage

The service uses two main directories:
- `/app/uploads`: Temporary storage for uploaded audio files
- `/app/transcripts`: Storage for completed transcriptions

These directories are mounted as Docker volumes to persist data.

## Monitoring and Maintenance

### View Logs
```bash
docker logs -f whisper-service
```

### Stop Service
```bash
docker stop whisper-service
```

### Cleanup
```bash
# Remove container
docker rm whisper-service

# Remove old transcripts
rm -rf ./transcripts/*
rm -rf ./uploads/*
```

## Performance Considerations

- GPU support significantly improves transcription speed
- Large files (>1 hour) may require increased memory allocation
- Model selection affects both speed and accuracy:
  - tiny: Fastest, least accurate
  - base: Good balance for most uses
  - large: Most accurate, slowest

## Security Considerations

- Service runs as non-root user
- Input validation for all parameters
- Secure file handling
- Automatic cleanup of temporary files
- Rate limiting recommended for production deployment

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad request (invalid parameters)
- 404: Resource not found
- 500: Server error

Detailed error messages are provided in the response body.

## Development

### Local Development Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
uvicorn main:app --reload
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and feature requests, please use the GitHub issue tracker.
