# Prompt Template

Copy and paste this template when making requests:

```
[Task]
I need to {describe your task here}.

[Context]
- This is part of the Whisper API project
- Current implementation uses {describe current state}
- Related files: {list relevant files}

[Requirements]
- {List specific requirements}
- {List any constraints}
- {List any special considerations}

[Guidelines]
Please follow these guidelines for your response:
1. Read and follow GUIDELINES.md for code quality and responses
2. Update TODO.md with completed and new tasks
3. Update JOURNAL.md with new decisions and progress
4. Provide complete source code for all changes
5. Validate against existing functionality
6. Remove any unnecessary code
7. Check for code duplication
8. Ensure consistent naming and style
9. Include proper error handling
10. Update documentation as needed

[Expected Updates]
- Code changes in: {list files}
- TODO.md updates
- JOURNAL.md updates
- Any new files needed
- Any files to be removed

Please structure your response as follows:
1. Explanation of changes
2. Complete source code updates
3. Updated TODO.md entries
4. Updated JOURNAL.md entries
5. Any migration steps needed
```

## Example Usage

```
[Task]
I need to add S3 storage support to the Whisper API.

[Context]
- This is part of the Whisper API project
- Current implementation uses local filesystem storage
- Related files: main.py, storage.py

[Requirements]
- Support both S3 and local storage
- Allow configuration via environment variables
- Maintain existing file structure
- Handle large file uploads efficiently

[Guidelines]
Please follow these guidelines for your response:
1. Read and follow GUIDELINES.md for code quality and responses
2. Update TODO.md with completed and new tasks
3. Update JOURNAL.md with new decisions and progress
4. Provide complete source code for all changes
5. Validate against existing functionality
6. Remove any unnecessary code
7. Check for code duplication
8. Ensure consistent naming and style
9. Include proper error handling
10. Update documentation as needed

[Expected Updates]
- Code changes in: main.py, storage.py
- New file: s3_storage.py
- TODO.md updates
- JOURNAL.md updates
```