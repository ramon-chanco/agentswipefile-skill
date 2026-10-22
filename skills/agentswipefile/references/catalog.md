# Public catalog contract

Primary origin: `https://agentswipefile.com`. Fetch `/catalog.json` without authentication. A resource page is `/resources/{slug}/`; the equivalent Markdown is `/resources/{slug}.md`. `/llms.txt` lists the public entry points. The catalog's `schemaVersion` identifies its data contract.

## Resource fields

| Field | Meaning |
| --- | --- |
| `slug`, `name`, `url`, `outboundUrl` | Stable directory key, display name, original vendor address, and tracked referral link |
| `description`, `kind`, `bestFor`, `editorialNote` | Original editorial purpose and fit guidance |
| `categories` | Asset types covered, not platform integrations |
| `subcategories` | Secondary topic keys, such as hooks or design context. These describe the reference content, not a native integration. |
| `image` | Source-page screenshot preview relative to the catalog origin |
| `checkedAt`, `sourceStatus` | Public source review date and scope |
| `access` | Documented entry points; `status` states what was actually checked |
| `workflow.primaryJob` | Evidence-based workflow classification |
| `workflow.integrations` | Documented MCP, API, plugin, extension, or Markdown access with source URL, evidence excerpt, and verification state |
| `workflow.platforms` | Named supported clients/platforms backed by explicit source evidence, not brands featured in a gallery |
| `workflow.capabilities` | Capability states: `documented`, `not_established`, or `needs_review` |
| `workflow.pricing` | Model/access label, available published plan tiers, pricing URL, date, and information still to verify |
| `workflow.included` | Original concise description of what this library/tool provides; plan-specific entitlements belong in the pricing excerpt |
| `workflow.limitations` | Practical access and verification boundaries |
| `agentPrompt` | Starting research brief, to adapt to the user's actual task |
| `featured` | Promotional/editorial placement, not evidence of suitability |

## Interpreting evidence

`documented` means a public vendor source establishes the capability. It does not mean the connection was authenticated or run. `not_established` means the reviewed evidence does not settle the question, not that the capability is absent. `needs_review` means the classifier or evidence was inconclusive; do not recommend it for a hard requirement without checking the official source.

Source excerpts can contain navigation or multiple plans. Read them with the linked source, preserve the billing period and free-tier limits, and avoid converting them into a numerical offer unless the amount, currency, plan, and billing terms are clear. The directory does not sell or authenticate the listed tools.

`workflow.pricing.freeAccess` describes library access. It does not establish that an MCP, API or plugin is free. `capabilities.{kind}.freeAccess` and the corresponding platform `freeAccess` distinguish known free connector access from paid or unknown access. The helper's combined `--free --requires ...` filter requires explicit free access for that capability. Unknown values fail hard requirements.

Optional pricing refinements are additive to schema version 2.0:

- `model`: for example `freemium`, when the source establishes both free and paid access.
- `freeAccessType`: `limited_preview` distinguishes a restricted preview from full access. Missing means the extent of free access is not established.
- `paidPlansAvailable`: explicit evidence of paid options. Missing is unknown.
- `display`: concise `headline` and `detail` for human display; use the plan facts for a budget decision.
- `plans[].planType`, `billingCycle`, `sourceUrl`, `checkedAt`, `status`: plan type, actual billing cycle and plan-level evidence. Preserve `price`, `billing`, `included` and `limits` together. A minimum volume price is not a one-seat price.

Read every relevant plan. Never report the first `$0` plan as the cost of the complete product. Do not invent a currency code or numerical offer when only a displayed price string is established. These are editorial pricing facts, not offers sold by this directory.

## Asset values

`ads`, `ugc`, `emails`, `sms`, `websites`, `apps`, `social`, `presentations`, `context`, `design`.

## Secondary topics

The catalog exposes `taxonomy.categories` and `taxonomy.subcategories` as key-to-label maps. Resources retain the ten primary asset categories and can also have zero or more secondary topics:

- `design-context`: Design context / DESIGN.md.
- `agent-skills`: Agent skills and tool directories.
- `prompts`: Reusable prompts.
- `video-motion`: Video and motion references.
- `hooks`: Opening hooks.
- `branding-type`: Branding and typography.
- `sections-components`: Website sections and UI components.
- `product-flows`: Paywalls, onboarding and pricing-page references.

Use `--subcategory` together with `--asset`, `--requires`, `--platform` and `--free`. These filters intersect; never silently relax a hard requirement. A resource in `agent-skills` does not automatically offer MCP. A resource with a pricing-page topic does not automatically have verified subscription pricing. The homepage supports shareable `?topic=hooks` filters; these retain the collection canonical and do not create additional thin SEO pages.

Read `workflow.screenshot.kind`: a vendor social preview is different from a captured source page. Neither establishes access to authenticated content.

If older catalog fields are missing, use the editorial fields for discovery and verify requirements against official sources. Never infer a native integration from a generic Browser entry.
