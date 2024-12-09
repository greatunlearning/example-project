# How to Work with LLMs for Code Development

## Overview

This guide explains how to effectively collaborate with Large Language Models (LLMs) for code development, using our project's established workflow and templates.

## Basic Workflow

1. **Project Setup**
   ```
   1. Use initial project prompt from PROMPT.md
   2. Review and adjust generated code
   3. Establish project structure
   4. Create documentation files
   ```

2. **Development Cycle**
   ```
   Define Task → Use Prompt Template → Review Output → Iterate → Update Documentation
   ```

## Effective Prompting Strategies

### 1. Start Broad, Then Refine
```
✅ Good:
"Create a basic FastAPI endpoint for file upload with these requirements: {list}"
Then: "Now add error handling for these cases: {list}"

❌ Bad:
"Create a complete FastAPI app with all error handling, validation, etc."
```

### 2. Use the Standard Template
Always use PROMPT_TEMPLATE.md:
```
[Task]
[Context]
[Requirements]
[Guidelines]
[Expected Updates]
```

### 3. Provide Clear Context
```
✅ Good:
"The upload endpoint currently uses local storage (in storage.py). 
We need to add S3 support while maintaining the existing interface."

❌ Bad:
"Add S3 support to the upload function."
```

## Iterative Development

### 1. Initial Implementation
```
1. Use template for initial request
2. Review generated code
3. Test basic functionality
4. Identify gaps
```

### 2. Refinement
```
[Task]
Please refine the upload endpoint to:
- Add better error handling
- Include input validation
- Add retry logic

[Context]
Current implementation is in upload.py...
```

### 3. Integration
```
[Task]
Integrate the upload endpoint with:
- New S3 storage backend
- Authentication middleware
- Logging system
```

## Common Scenarios

### 1. Bug Fixes
```
[Task]
Fix the file upload timeout issue

[Context]
- Error occurs in upload.py, line 123
- Current timeout is 30 seconds
- Affects large files only

[Requirements]
- Implement chunked upload
- Add progress tracking
- Maintain existing interface
```

### 2. Feature Addition
```
[Task]
Add rate limiting to API endpoints

[Context]
- No current rate limiting
- Using FastAPI framework
- Need to protect all endpoints

[Requirements]
- Configure limits per endpoint
- Add Redis backend
- Include bypass for admin keys
```

### 3. Refactoring
```
[Task]
Refactor storage handling into separate module

[Context]
- Currently mixed in main.py
- Need to support multiple backends
- Maintain existing interface

[Requirements]
- Create storage interface
- Implement local and S3 backends
- Add factory pattern for backend selection
```

## Best Practices

### 1. Code Review Requests
```
[Task]
Review this implementation for:
- Error handling completeness
- Edge cases
- Performance issues
- Security concerns

[Context]
{paste relevant code}
```

### 2. Documentation Updates
```
[Task]
Update documentation for new S3 features

[Context]
- Added S3 storage support
- New configuration options
- Changed file handling

[Expected Updates]
- README.md
- JOURNAL.md
- API documentation
```

### 3. Testing Requests
```
[Task]
Create tests for the upload endpoint

[Requirements]
- Unit tests for validation
- Integration tests for S3
- Performance tests
- Error case coverage
```

## Handling Common Issues

### 1. Incomplete Responses
If the LLM provides incomplete code:
```
Please provide the complete implementation, including:
- All imports
- Full function definitions
- Error handling
- Type hints
```

### 2. Consistency Issues
If you notice inconsistencies:
```
Please review for consistency:
- Function naming
- Error handling patterns
- Type usage
- Documentation style
```

### 3. Missing Updates
If documentation updates are missing:
```
Please also update:
- TODO.md (mark completed items)
- JOURNAL.md (add decisions made)
- README.md (new features)
```

## Project Maintenance

### 1. Regular Reviews
```
[Task]
Review current codebase for:
- Unused code
- Inconsistencies
- Technical debt
- Documentation gaps
```

### 2. Dependency Updates
```
[Task]
Update project dependencies:
- Review requirements.txt
- Check for security issues
- Test compatibility
- Update documentation
```

### 3. Performance Optimization
```
[Task]
Optimize {feature} performance:
- Profile current behavior
- Identify bottlenecks
- Propose improvements
- Maintain functionality
```

## Tips for Success

1. **Be Specific**
   - List exact requirements
   - Provide current context
   - Specify expected outcomes

2. **Iterate Gradually**
   - Start with basic functionality
   - Add features incrementally
   - Test at each step

3. **Maintain Context**
   - Reference existing code
   - Explain recent changes
   - Highlight constraints

4. **Review Thoroughly**
   - Check complete implementation
   - Verify documentation updates
   - Test edge cases

5. **Keep History**
   - Update JOURNAL.md
   - Maintain TODO.md
   - Document decisions

---

*Remember: The LLM is a tool to assist development. Always review, test, and validate its output.*