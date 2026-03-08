---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: StageState & Orchestrator Hardening

## Objective
Implement stable pipeline state management using the StageState schema and harden agent communication with retries and timeouts.

## Context
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- backend/app/services/pipeline_orchestrator.py
- backend/app/services/pipeline_service.py
- backend/app/models.py

## Tasks

<task type="auto">
  <name>Align PipelineService with Orchestrator</name>
  <files>
    <file>backend/app/services/pipeline_service.py</file>
  </files>
  <action>
    - Refactor run_pipeline to use PipelineOrchestrator for execution.
    - Ensure candidate and job data are prepared correctly before passing to orchestrator.
  </action>
  <verify>Check that run_pipeline calls orch.execute_pipeline.</verify>
  <done>PipelineService delegates execution to Orchestrator.</done>
</task>

<task type="auto">
  <name>Implement StageState in Orchestrator</name>
  <files>
    <file>backend/app/services/pipeline_orchestrator.py</file>
  </files>
  <action>
    - Initialize self.state with the StageState schema.
    - Implement _ensure_stage and _stage_ok helpers.
    - Update execute_pipeline to save state after every stage.
    - Fix AgentRunStatus mapping to enums.
  </action>
  <verify>Inspect database for StageState JSON structure.</verify>
  <done>Pipeline state is granular and persistent.</done>
</task>

<task type="auto">
  <name>Harden Agent Communication</name>
  <files>
    <file>backend/app/services/pipeline_orchestrator.py</file>
  </files>
  <action>
    - Add retry logic (3 attempts) with backoff in call_agent.
    - Add per-agent timeouts.
    - Implement Pause semantics for ATS/Skill agent results.
  </action>
  <verify>Run pipeline and check logs for retry attempts on failed connectivity.</verify>
  <done>Agent calls are resilient and flow control is respected.</done>
</task>

## Success Criteria
- [ ] Pipeline is idempotent (safe to re-run).
- [ ] StageState JSON is correctly persisted in credentials table.
- [ ] AgentRun statuses match database enums.
- [ ] Pipeline stops correctly on "Review Required" or "Test Required".
