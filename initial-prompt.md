I want to create a REST API for Whisper (openai-whisper) with the following features:

Core Requirements:
- FastAPI-based REST API for audio transcription
- File upload endpoint with configurable parameters (language, model size, output format)
- Background processing with progress tracking
- Multiple output formats (JSON, SRT, VTT, TXT)
- Status checking endpoint
- Download endpoint for completed transcripts
- List endpoint for all transcriptions
- Progress tracking with duration estimation

Technical Requirements:
- Multi-stage Dockerfile
- Non-root user for security
- Volume mounts for persistence
- Background task processing
- Proper error handling
- File cleanup after processing

Configuration Options:
- Multiple whisper models (tiny, base, small, medium, large)
- Language selection
- Output format selection
- Word-level timestamps option
- VAD filtering option

Please create this step by step:
1. First, create the FastAPI application with all endpoints
2. Then, create a Dockerfile for the service
3. Add a comprehensive README
4. Create a TODO.md for future enhancements
