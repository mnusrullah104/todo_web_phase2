# Acceptance Criteria Verification

## Overview

Acceptance criteria define the conditions that a software product must satisfy to be accepted by the user, customer, or other system. Verification against acceptance criteria ensures that implementations meet specified requirements.

## Verification Process

### 1. Identify Acceptance Criteria
- Locate the acceptance criteria in the specification document
- Understand the context and scope of each criterion
- Determine the phase or milestone to which criteria apply
- Identify success and failure conditions

### 2. Create Verification Checklist
- List all acceptance criteria to be verified
- Assign priority levels to each criterion
- Define specific test scenarios for each criterion
- Identify required test data and environment

### 3. Execute Verification Steps
- Set up the testing environment
- Prepare test data and configurations
- Execute each verification step systematically
- Document results and observations
- Capture evidence (screenshots, logs, etc.)

### 4. Evaluate Results
- Compare actual results with expected outcomes
- Determine pass/fail status for each criterion
- Identify any deviations or anomalies
- Assess impact of any failures

## Acceptance Criteria Format

### Good Acceptance Criteria Characteristics
- Specific and measurable
- Observable and testable
- Unambiguous and clear
- Achievable and realistic
- Relevant to user needs

### Example Format
```
Given [initial context]
When [specific action occurs]
Then [expected outcome]
And [additional conditions if applicable]
```

## Verification Techniques

### Manual Verification
- Step-by-step execution of user stories
- Visual inspection of UI elements
- Functional testing of features
- Cross-browser/device compatibility testing

### Automated Verification
- Unit tests for individual components
- Integration tests for system interactions
- API tests for endpoint validation
- End-to-end tests for complete workflows

## Common Verification Scenarios

### REST API Verification
- Verify HTTP status codes match expectations
- Validate response formats and structures
- Test error conditions and error responses
- Confirm authentication and authorization requirements
- Check rate limiting and other constraints

### MCP Tool Verification
- Validate tool discovery and registration
- Test tool invocation with various parameters
- Verify response formats and error handling
- Confirm proper authentication and authorization
- Check resource access patterns

### Security Verification
- Verify authentication requirements (401 Unauthorized)
- Test authorization controls (403 Forbidden)
- Validate input sanitization and validation
- Check for proper session management
- Verify secure communication protocols

## Documentation Requirements

### Test Evidence
- Screenshots of successful operations
- Console logs and error messages
- API response captures
- Performance metrics
- Security scan results

### Defect Reporting
- Clear reproduction steps
- Expected vs. actual behavior
- Severity assessment
- Supporting evidence
- Environmental information

## Phase-Specific Verification

### Red Phase (Implementation)
- Verify basic functionality implementation
- Confirm code compiles and runs
- Test minimal viable functionality
- Validate basic error handling

### Green Phase (Enhancement)
- Verify enhanced functionality
- Test additional features
- Confirm backward compatibility
- Validate improved error handling

### Refactor Phase (Optimization)
- Verify refactored code maintains functionality
- Test performance improvements
- Confirm no regression in existing features
- Validate code quality metrics

## Verification Checklist Template

### For Each Acceptance Criterion:
- [ ] Requirement clearly understood
- [ ] Test scenario defined
- [ ] Test data prepared
- [ ] Test environment ready
- [ ] Verification executed
- [ ] Results documented
- [ ] Status recorded (Pass/Fail/Blocked)
- [ ] Evidence captured
- [ ] Issues reported if applicable

## Common Verification Pitfalls

### Missing Scenarios
- Edge cases and boundary conditions
- Invalid input combinations
- Concurrent user scenarios
- Network interruption cases

### Insufficient Coverage
- Happy path only testing
- Single data point testing
- Limited environment testing
- No performance consideration

### Poor Documentation
- Incomplete test records
- Missing evidence
- Unclear defect reports
- No traceability to requirements

## Quality Gates

### Before Proceeding to Next Phase
- All critical acceptance criteria passed
- All high-priority defects resolved
- Test coverage meets minimum thresholds
- Performance benchmarks achieved
- Security requirements satisfied