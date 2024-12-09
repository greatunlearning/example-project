from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
import whisper
import uuid
import os
import json
import time
from enum import Enum
from datetime import datetime
from pathlib import Path
import torch

app = FastAPI(title="Whisper Transcription API")

# Constants
UPLOAD_DIR = "uploads"
TRANSCRIPT_DIR = "transcripts"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# Enums and Models
class TranscriptionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class WhisperModel(str, Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class OutputFormat(str, Enum):
    JSON = "json"
    SRT = "srt"
    VTT = "vtt"
    TXT = "txt"

class TranscriptionRequest(BaseModel):
    # Basic parameters
    language: Optional[str] = Field(None, description="Source language code (e.g., 'en', 'fr', 'de')")
    task: Optional[str] = Field("transcribe", description="Task type: 'transcribe' or 'translate'")
    model: WhisperModel = Field(WhisperModel.BASE, description="Whisper model size to use")
    output_format: List[OutputFormat] = Field(
        default=[OutputFormat.JSON],
        description="Output format(s) for the transcription"
    )

    # Advanced parameters
    initial_prompt: Optional[str] = Field(None, description="Optional text to provide as initial prompt")
    temperature: Optional[float] = Field(0.0, description="Temperature for sampling")
    beam_size: Optional[int] = Field(5, description="Beam size for beam search")
    patience: Optional[float] = Field(None, description="Beam search patience factor")
    suppress_tokens: Optional[List[int]] = Field(None, description="List of tokens to suppress")
    condition_on_previous_text: bool = Field(True, description="Whether to condition on previous text")
    fp16: bool = Field(True, description="Use fp16 for model computation")
    
    # Timestamp options
    word_timestamps: bool = Field(False, description="Enable word-level timestamps")
    vad_filter: bool = Field(True, description="Use voice activity detection to filter out non-speech")
    vad_threshold: float = Field(0.5, description="VAD threshold (0.0-1.0)")

class ProgressInfo(BaseModel):
    segments_processed: int = 0
    total_segments: Optional[int] = None
    estimated_time_remaining: Optional[float] = None
    processing_speed: Optional[float] = None  # seconds of audio processed per second

class TranscriptionResponse(BaseModel):
    id: str
    status: TranscriptionStatus
    filename: str
    filesize: int  # in bytes
    duration: Optional[float] = None  # in seconds
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: Optional[ProgressInfo] = None
    error: Optional[str] = None
    model: WhisperModel
    output_formats: List[OutputFormat]
    language: Optional[str] = None

# In-memory storage for transcription status and progress
transcriptions: Dict[str, dict] = {}

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT/VTT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace(".", ",")

def save_transcript_formats(transcript_id: str, result: dict, formats: List[OutputFormat]):
    """Save transcription in multiple formats"""
    base_path = os.path.join(TRANSCRIPT_DIR, transcript_id)
    
    # Save JSON (original format)
    if OutputFormat.JSON in formats:
        with open(f"{base_path}.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    # Save plain text
    if OutputFormat.TXT in formats:
        with open(f"{base_path}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join([segment["text"] for segment in result["segments"]]))
    
    # Save SRT
    if OutputFormat.SRT in formats:
        with open(f"{base_path}.srt", "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                f.write(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n\n")
    
    # Save VTT
    if OutputFormat.VTT in formats:
        with open(f"{base_path}.vtt", "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in result["segments"]:
                start = format_timestamp(segment["start"]).replace(",", ".")
                end = format_timestamp(segment["end"]).replace(",", ".")
                f.write(f"{start} --> {end}\n{segment['text'].strip()}\n\n")

def update_progress(transcript_id: str, segments_processed: int, total_segments: int = None):
    """Update progress information for a transcription"""
    if transcript_id in transcriptions:
        transcriptions[transcript_id]["progress"] = {
            "segments_processed": segments_processed,
            "total_segments": total_segments,
            "processing_speed": None,  # Calculate based on time elapsed and audio processed
            "estimated_time_remaining": None  # Calculate based on speed and remaining segments
        }
        save_transcript_metadata(transcript_id, transcriptions[transcript_id])

async def process_transcription(
    transcript_id: str,
    audio_path: str,
    params: TranscriptionRequest
):
    """Background task to process the transcription"""
    try:
        # Update status to processing and record start time
        transcriptions[transcript_id]["status"] = TranscriptionStatus.PROCESSING
        transcriptions[transcript_id]["started_at"] = datetime.utcnow()
        save_transcript_metadata(transcript_id, transcriptions[transcript_id])

        # Load model with specified parameters
        model = whisper.load_model(
            params.model,
            device="cuda" if torch.cuda.is_available() and params.fp16 else "cpu"
        )

        # Perform transcription
        result = model.transcribe(
            audio_path,
            language=params.language,
            task=params.task,
            initial_prompt=params.initial_prompt,
            temperature=params.temperature,
            beam_size=params.beam_size,
            patience=params.patience,
            suppress_tokens=params.suppress_tokens,
            condition_on_previous_text=params.condition_on_previous_text,
            fp16=params.fp16,
            word_timestamps=params.word_timestamps,
            vad_filter=params.vad_filter,
            vad_threshold=params.vad_threshold
        )

        # Save in all requested formats
        save_transcript_formats(transcript_id, result, params.output_format)

        # Update final status
        transcriptions[transcript_id].update({
            "status": TranscriptionStatus.COMPLETED,
            "completed_at": datetime.utcnow(),
            "duration": result.get("duration", None),
            "language": result.get("language", params.language)
        })
        save_transcript_metadata(transcript_id, transcriptions[transcript_id])

        # Clean up audio file
        os.remove(audio_path)

    except Exception as e:
        transcriptions[transcript_id]["status"] = TranscriptionStatus.FAILED
        transcriptions[transcript_id]["error"] = str(e)
        save_transcript_metadata(transcript_id, transcriptions[transcript_id])

def save_transcript_metadata(transcript_id: str, metadata: dict):
    """Save transcription metadata to a JSON file"""
    filepath = os.path.join(TRANSCRIPT_DIR, f"{transcript_id}_metadata.json")
    with open(filepath, "w") as f:
        json.dump(metadata, f, default=str)

def load_transcript_metadata(transcript_id: str) -> dict:
    """Load transcription metadata from JSON file"""
    filepath = os.path.join(TRANSCRIPT_DIR, f"{transcript_id}_metadata.json")
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Transcript not found")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def create_transcription(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    params: TranscriptionRequest
):
    """Upload audio file and start transcription"""
    # Generate unique ID for this transcription
    transcript_id = str(uuid.uuid4())
    
    # Save uploaded file and get its size
    audio_path = os.path.join(UPLOAD_DIR, f"{transcript_id}_{file.filename}")
    file_size = 0
    with open(audio_path, "wb") as buffer:
        while chunk := await file.read(8192):
            file_size += len(chunk)
            buffer.write(chunk)
    
    # Create transcription metadata
    transcription_data = {
        "id": transcript_id,
        "status": TranscriptionStatus.PENDING,
        "filename": file.filename,
        "filesize": file_size,
        "created_at": datetime.utcnow(),
        "started_at": None,
        "completed_at": None,
        "progress": None,
        "error": None,
        "model": params.model,
        "output_formats": params.output_format,
        "language": params.language
    }
    
    # Store in memory and save to disk
    transcriptions[transcript_id] = transcription_data
    save_transcript_metadata(transcript_id, transcription_data)
    
    # Start background processing
    background_tasks.add_task(
        process_transcription,
        transcript_id,
        audio_path,
        params
    )
    
    return TranscriptionResponse(**transcription_data)

@app.get("/transcripts", response_model=List[TranscriptionResponse])
async def list_transcripts():
    """List all transcriptions"""
    transcript_list = []
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith("_metadata.json"):
            transcript_id = filename.replace("_metadata.json", "")
            metadata = load_transcript_metadata(transcript_id)
            transcript_list.append(TranscriptionResponse(**metadata))
    
    return transcript_list

@app.get("/transcripts/{transcript_id}", response_model=TranscriptionResponse)
async def get_transcript_status(transcript_id: str):
    """Get status of specific transcription"""
    metadata = load_transcript_metadata(transcript_id)
    return TranscriptionResponse(**metadata)

@app.get("/transcripts/{transcript_id}/download")
async def download_transcript(
    transcript_id: str,
    format: OutputFormat = Query(OutputFormat.JSON, description="Format to download")
):
    """Download completed transcription in specified format"""
    # Check if transcription exists and is completed
    metadata = load_transcript_metadata(transcript_id)
    if metadata["status"] != TranscriptionStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Transcription is not yet completed"
        )
    
    # Check if requested format was generated
    if format not in metadata["output_formats"]:
        raise HTTPException(
            status_code=400,
            detail=f"Transcription not available in {format.value} format"
        )
    
    # Return transcription file
    filepath = os.path.join(TRANSCRIPT_DIR, f"{transcript_id}.{format.value}")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Transcript file not found")
    
    return FileResponse(
        filepath,
        filename=f"transcript_{metadata['filename']}.{format.value}"
    )

@app.delete("/transcripts/{transcript_id}")
async def delete_transcript(transcript_id: str):
    """Delete a transcription and its associated files"""
    try:
        # Remove metadata file
        metadata_path = os.path.join(TRANSCRIPT_DIR, f"{transcript_id}_metadata.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
        
        # Remove all format variations
        base_path = os.path.join(TRANSCRIPT_DIR, transcript_id)
        for format in OutputFormat:
            format_path = f"{base_path}.{format.value}"
            if os.path.exists(format_path):
                os.remove(format_path)
        
        # Remove from memory if exists
        transcriptions.pop(transcript_id, None)
        
        return {"message": "Transcription deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_available_models():
    """List available Whisper models and their properties"""
    return {
        "models": [
            {
                "name": model.value,
                "parameters": whisper.load_model(model.value).dims.n_vocab,
                "multilingual": True,
                "size_mb": os.path.getsize(whisper._download(model.value, "", "")) / (1024 * 1024)
                if os.path.exists(whisper._download(model.value, "", "")) else None
            }
            for model in WhisperModel
        ]
    }

@app.get("/languages")
async def list_supported_languages():
    """List all supported languages"""
    return {"languages": whisper.tokenizer.LANGUAGES}