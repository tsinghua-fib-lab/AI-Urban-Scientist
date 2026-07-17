# Paper Planner Output Template

Use this compact template when creating `plans/paper-plan/paper_plan.md`.

```markdown
# {Working Title}

## Source And Scope
- Source type:
- Domain:
- Study design family:
- Unit of observation:
- Main contribution type:
- Pipeline branch:
- Known unknowns:

## Central Claim
- Claim:
- Claim strength:
- Inferential target:
- Falsification condition:

## Research Questions
1.
2.
3.

## Subclaims
| ID | Subclaim | Observable implication | Minimum evidence | Primary analysis | Main alternative explanation | Weakening pattern |
| --- | --- | --- | --- | --- | --- | --- |

## Data And Measurement Plan
| Dataset | Role | Unit | Coverage | Key variables | Linkage | Preprocessing | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |

| Variable | Construct | Source fields | Transformation | Unit/scale | Missingness handling | Validation |
| --- | --- | --- | --- | --- | --- | --- |

## Method-Library Calibration
- Category files read:
- Matched entries:
- Adapted method patterns:
- Adapted validation patterns:
- No-match notes:

## Identification Or Modeling Strategy
Primary strategy:

Primary model/procedure:

Assumptions:

Why this strategy matches the claim:

Unsuitable conditions or failure triggers:

## Evidence Chain
| Evidence | Supports | Type | Data/variables | Analysis | Decision rule | Threat | Placement |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Main Analyses
| Analysis | Purpose | Model/procedure | Inputs | Outputs | Acceptance criteria | Failure action |
| --- | --- | --- | --- | --- | --- | --- |

## Analysis Execution DAG
Dependency summary:

### T1: {Task Name}
- Depends on:
- Purpose:
- Inputs:
- Method/model:
- Implementation notes:
- Outputs:
- Validation/diagnostics:
- Acceptance criteria:
- Failure action:
- Downstream consumers:

## Figures And Tables
| Item | Role | Linked evidence | Panels/columns | Type | Key comparison | Takeaway | Placement rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Figure Design Spec
Set-wide style: palette family / font family / base font size / format / dpi.

| Figure | Palette type | Named palette + hex/version | Colorblind-safe? | Redundant (non-color) encoding | Uncertainty shown | Format/dpi/width |
| --- | --- | --- | --- | --- | --- | --- |

## Robustness Matrix
| Check | Threat addressed | Implementation | Expected output | Claim affected | Required/optional |
| --- | --- | --- | --- | --- | --- |

## Risk Register
| Risk | Likelihood | Impact | Affected claim | Mitigation | If unresolved |
| --- | --- | --- | --- | --- | --- |

## Reviewer Defense
| Reviewer concern | Response in analysis | Response in writing |
| --- | --- | --- |

## Interpretation Framework
| Result pattern | Interpretation | Claim/title change | Figure/discussion change |
| --- | --- | --- | --- |
| Primary |
| Null |
| Heterogeneous |
| Mechanism |
| Fragile |

## Quality Gates
| Gate | Status | Notes |
| --- | --- | --- |
| Claim-design fit |
| Data sufficiency |
| Execution readiness |
| Evidence coverage |
| Mechanism discipline |
| Robustness adequacy |
| Figure economy |
| Visual design |
| No invention |
```

## Optional agent_plan.json Skeleton

Create this only when the user asks for a machine-readable plan.

```json
{
  "metadata": {
    "working_title": "",
    "source_type": "",
    "domain": "",
    "study_design_family": "",
    "pipeline_branch": "",
    "plan_version": "1.0"
  },
  "central_claim": {
    "claim_text": "",
    "claim_strength": "",
    "inferential_target": "",
    "falsification_condition": ""
  },
  "research_questions": [],
  "subclaims": [],
  "datasets": [],
  "variables": [],
  "method_library_calibration": {
    "matched_entries": [],
    "category_files_read": [],
    "adapted_method_patterns": [],
    "adapted_validation_patterns": [],
    "no_match_notes": ""
  },
  "identification_or_modeling_strategy": {},
  "evidence_items": [],
  "analysis_tasks": [],
  "figure_style_guide": {
    "palette_family": "",
    "font_family": "",
    "base_font_size_pt": null,
    "format": "",
    "dpi": null,
    "colorblind_safe": true
  },
  "figures": [],
  "tables": [],
  "robustness_checks": [],
  "risk_register": [],
  "interpretation_framework": [],
  "quality_gates": []
}
```
