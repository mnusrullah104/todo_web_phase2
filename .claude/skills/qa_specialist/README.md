# QA Specialist Skill

This skill provides expertise in ensuring code quality, running tests, and verifying that implementations meet the acceptance criteria defined in the specs.

## Overview

The QA Specialist skill transforms Claude into an expert for quality assurance tasks, particularly for:
- Verifying implementations against acceptance criteria
- Testing REST endpoints and MCP tools for correctness
- Checking for proper error handling (e.g., 401 Unauthorized for missing JWTs)
- Running automated tests and analyzing results
- Performing quality assurance reviews

## Components

### SKILL.md
Main skill definition with capabilities and guidelines

### References
- `acceptance_criteria_verification.md` - Guidelines for verifying implementations against acceptance criteria
- `api_endpoint_testing.md` - Best practices for API endpoint testing
- `error_handling_validation.md` - Methods for validating proper error handling

### Scripts
- `automated_qa_runner.py` - Automated QA testing framework for API validation

### Assets
- `sample_test_config.yaml` - Sample configuration file for QA testing

### Tests
- `test_qa_processes.py` - Validation tests for QA processes

## Usage

This skill should be invoked when performing:
- Quality assurance on implementations
- Verification against acceptance criteria
- REST API endpoint testing
- MCP tool validation
- Error handling verification
- Test execution and analysis

## Key Guidelines

1. Verify every implementation against the specific Phase's Acceptance Criteria [cite: 795]
2. Ensure all REST endpoints and MCP tools are tested for correctness [cite: 797, 815]
3. Check for proper error handling (e.g., 401 Unauthorized for missing JWTs) [cite: 724, 792]
4. Always verify against written acceptance criteria
5. Test both positive and negative scenarios
6. Validate proper error responses and status codes
7. Ensure security measures are in place

## Automated Testing

The QA Specialist includes an automated testing framework:

### Running Tests
```bash
python automated_qa_runner.py --config test_config.yaml
```

### Creating a Sample Configuration
```bash
python automated_qa_runner.py --create-sample
```

### Direct API Testing
```bash
python automated_qa_runner.py --base-url http://localhost:8000 --auth-token your_token
```

## Testing Categories

### Acceptance Criteria Testing
- Given/When/Then scenarios
- Phase-specific verification
- Functional requirement validation

### API Endpoint Testing
- HTTP method validation
- Status code verification
- Response format validation
- Error condition testing

### Error Handling Testing
- Authentication (401 Unauthorized)
- Authorization (403 Forbidden)
- Input validation (400 Bad Request)
- Resource not found (404 Not Found)
- Server errors (500 Internal Server Error)

### MCP Tool Testing
- Tool discovery validation
- Tool invocation testing
- Parameter validation
- Response format verification