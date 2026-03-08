# ROADMAP.md

> **Current Phase**: 1 (Agent Completion)
> **Milestone**: v1.0 — Production Ready

## Must-Haves (from SPEC)

- [ ] All 10 agent services fully functional
- [ ] Pipeline handles 100+ applications/hour
- [ ] ATS fraud detection 95%+ accuracy
- [ ] Skill passports verifiable by third parties

---

## Phases

### Phase 1: Agent Completion
**Status**: ⬜ Not Started
**Objective**: Replace mock implementations with fully functional agents

**Deliverables**:
- [ ] Skill Agent — Real evidence aggregation and confidence scoring
- [ ] Bias Agent — Actual pattern detection and fairness metrics
- [ ] Matching Agent — Semantic job-candidate matching
- [ ] Evidence Graph Builder — Complete signal processing

**Priority**: HIGH — Blocks all pipeline functionality

---

### Phase 2: Pipeline Hardening
**Status**: ⬜ Not Started
**Objective**: Make the 10-stage pipeline production-ready

**Deliverables**:
- [ ] Retry logic for all agent HTTP calls
- [ ] Caching layer for repeated API calls (GitHub, LeetCode)
- [ ] Graceful degradation when agents fail
- [ ] Parallel execution for independent stages
- [ ] Progress tracking and status updates

**Priority**: HIGH — Critical for reliability

---

### Phase 3: Security & Performance
**Status**: ⬜ Not Started
**Objective**: Harden the system for production use

**Deliverables**:
- [ ] Rate limiting for external APIs
- [ ] Audit logging for all pipeline decisions
- [ ] Enhanced ATS fraud detection rules
- [ ] Database query optimization
- [ ] Connection pooling improvements

**Priority**: MEDIUM — Required before production

---

### Phase 4: Frontend Polish
**Status**: ⬜ Not Started
**Objective**: Improve user experience and add missing features

**Deliverables**:
- [ ] Real-time pipeline status updates (WebSocket)
- [ ] Mobile-responsive dashboard improvements
- [ ] Skill passport sharing/export functionality
- [ ] Company analytics dashboard
- [ ] Admin review queue UI

**Priority**: MEDIUM — User-facing improvements

---

### Phase 5: Testing & Documentation
**Status**: ⬜ Not Started
**Objective**: Ensure quality and maintainability

**Deliverables**:
- [ ] Integration tests for full pipeline
- [ ] Unit tests for agent core logic
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Deployment guide
- [ ] Runbook for common issues

**Priority**: LOW — Final polish before release

---

## Progress Legend

- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ⏸️ Blocked

---

*Last updated: 2026-02-09 by /new-project workflow*
