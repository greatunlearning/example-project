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

This is a REST API service for OpenAI's Whisper speech-to-text model, built as an example of LLM-assisted development patterns. It demonstrates how to create a production-ready service while following new AI-friendly development principles.

### Features

- 🎯 Audio transcription using OpenAI's Whisper
- 🌐 Multiple language support
- 🔄 Background processing with progress tracking
- 📊 Multiple output formats (JSON, SRT, VTT, TXT)
- 📝 Word-level timestamps
- 🎛️ Configurable parameters

[Rest of the original README content follows...]
