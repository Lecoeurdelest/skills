# Model Fallback Policy

## Allowed for Fallback Models

- document reading,
- log summarization,
- evidence indexing,
- test-case drafting,
- diff review,
- documentation,
- issue classification,
- read-only inspection,
- low-risk implementation followed by mandatory review and tests.

## Restricted Without Explicit Approval

- production deployment,
- database migration,
- destructive data changes,
- security remediation,
- authentication or authorization changes,
- architecture decisions,
- official root-cause conclusions,
- compliance-sensitive reports,
- evidence-sensitive incident conclusions.

## Requirements Before Switching Models

1. Confirm the fallback model is approved for the task category.
2. Provide the complete handoff package.
3. Require independent repository and artifact validation.
4. Require tests after implementation changes.
5. Record the model transition.
6. Do not overwrite unverified prior results.

If no qualified model exists, pause the task.
