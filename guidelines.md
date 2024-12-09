# LLM Guidelines for Code Management

## Core Principles

1. **Code Completeness**
   - Always provide complete, runnable source code
   - Never use ellipsis (...) or "rest remains the same"
   - Include all necessary imports
   - Show full function implementations

2. **Code Preservation**
   - Never modify working code without explicit validation
   - Preserve existing functionality when adding features
   - Wrap changes in new functions/classes when uncertain
   - Always keep existing tests passing

3. **Code Cleanliness**
   - Remove unused imports immediately
   - Delete deprecated functions when replaced
   - Clean up redundant variables
   - Remove commented-out code
   - Delete unused files

4. **Consistency**
   - Double-check function names match across codebase
   - Ensure consistent naming conventions
   - Maintain consistent code style
   - Use consistent return types

## Response Rules

1. **Always Provide**
   - Complete file contents after changes
   - All affected files
   - Explanation of changes
   - Migration steps if needed

2. **Never**
   - Leave partial implementations
   - Skip error handling
   - Assume code exists without checking
   - Reference undefined variables/functions

## Code Quality Guidelines

1. **Avoid Duplication**
   - Check for existing similar functions
   - Refactor common code into shared utilities
   - Use inheritance/composition appropriately
   - Maintain DRY (Don't Repeat Yourself) principle

2. **Function Design**
   - Keep functions focused and single-purpose
   - Validate all input parameters
   - Handle edge cases
   - Document return values

3. **Error Handling**
   - Always include appropriate error handling
   - Use specific exception types
   - Provide meaningful error messages
   - Log errors appropriately

4. **Type Safety**
   - Use type hints consistently
   - Validate type conversions
   - Check nullable values
   - Document type constraints

## Validation Requirements

1. **Before Changes**
   - Confirm existing functionality
   - Identify dependent code
   - Check for side effects
   - Review existing tests

2. **During Implementation**
   - Maintain existing interfaces
   - Preserve backward compatibility
   - Follow established patterns
   - Add necessary validation

3. **After Changes**
   - Verify all tests pass
   - Check for regressions
   - Validate edge cases
   - Ensure documentation accuracy

## Documentation Rules

1. **Code Comments**
   - Explain complex logic
   - Document non-obvious decisions
   - Update docstrings
   - Remove obsolete comments

2. **Function Documentation**
   - Document parameters
   - Describe return values
   - List exceptions
   - Provide usage examples

## Testing Guidelines

1. **Test Coverage**
   - Add tests for new functionality
   - Update affected tests
   - Remove obsolete tests
   - Maintain test consistency

2. **Test Quality**
   - Test edge cases
   - Include error scenarios
   - Verify error messages
   - Test async behavior

## File Management

1. **New Files**
   - Create with proper headers
   - Include necessary imports
   - Add type hints
   - Document purpose

2. **File Cleanup**
   - Remove unused files
   - Clean up temporary files
   - Update import references
   - Remove empty files

## Code Review Checklist

1. **Before Submitting**
   - Check naming consistency
   - Verify import organization
   - Confirm error handling
   - Validate type hints

2. **Quality Checks**
   - No duplicate code
   - Proper encapsulation
   - Consistent style
   - Clear documentation

## Response Format

When making changes, structure responses as:

```
[CHANGES]
- List of specific changes made
- Files affected
- Functions modified

[VALIDATION]
- Tests affected
- Edge cases considered
- Potential issues

[COMPLETE SOURCE]
- Full source code of all modified files
```

## Version Control Guidelines

1. **Commits**
   - Group related changes
   - Write clear commit messages
   - Reference issues/tickets
   - Include test changes

2. **Branches**
   - Create for features
   - Name descriptively
   - Keep focused
   - Clean up after merge

## Maintenance Rules

1. **Regular Checks**
   - Review unused code
   - Check for duplicates
   - Validate dependencies
   - Update documentation

2. **Code Health**
   - Monitor complexity
   - Check for antipatterns
   - Review error handling
   - Verify logging

## Error Prevention

1. **Common Pitfalls**
   - Undefined references
   - Type mismatches
   - Missing error handling
   - Incomplete implementations

2. **Best Practices**
   - Use linters
   - Follow style guides
   - Implement safeguards
   - Document assumptions

---

*Note: These guidelines should be followed for all code changes and responses. Regular updates to these guidelines are encouraged as new patterns or issues emerge.*