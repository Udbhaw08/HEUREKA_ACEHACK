# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision

Build a **Fair Hiring Platform** — an end-to-end AI-powered recruitment system that eliminates bias and fraud in hiring through multi-source skill verification, cryptographically signed credentials, and intelligent job matching.

## Goals

1. **Complete Agent Integration** — Replace mock implementations with fully functional Skill, Bias, and Matching agents
2. **Production-Ready Pipeline** — End-to-end application processing with retry logic, caching, and error handling
3. **Enterprise Security** — Hardened ATS fraud detection, rate limiting, and audit logging
4. **Seamless User Experience** — Real-time status updates, responsive dashboards, and mobile support

## Non-Goals (Out of Scope)

- Mobile native applications (web-only for now)
- Multi-tenant SaaS deployment
- Blockchain-based credential storage
- Video interview integration
- Background check integration

## Users

1. **Candidates** — Apply to jobs, view skill passport, track application status
2. **Companies** — Post jobs, review candidate pipelines, access fairness reports
3. **Administrators** — Review flagged applications, manage bias detection rules

## Constraints

- **Technical**: Must use existing PostgreSQL database, FastAPI backend, React frontend
- **External APIs**: GitHub (5000 req/hr), LeetCode (web scraping), Codeforces (1 req/2s)
- **Security**: Ed25519 signing for credentials, bcrypt for passwords
- **Performance**: Pipeline must complete within 2 minutes per application

## Success Criteria

- [ ] All 10 agent services fully functional (no mocks)
- [ ] Pipeline handles 100+ applications/hour without failures
- [ ] ATS fraud detection catches 95%+ manipulation attempts
- [ ] Match scores correlate with actual job fit (validated by users)
- [ ] Skill passports verifiable by any third party

---

*Last updated: 2026-02-09 by /new-project workflow*
