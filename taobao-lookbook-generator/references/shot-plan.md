# Fixed 16-Shot Plan

All outputs are separate, highest-quality JPG files at 1536 × 2048 px (3:4). Keep the same person, primary product, complete styling, color, hair, makeup, and body proportions throughout. Actions must be materially different; facial expression may change only slightly and naturally.

For the twelve person-centric shots, select a compatible pose from [pose-library.md](pose-library.md), record its `pose_id`, and avoid reuse where evidence allows. The four `ST-DETAIL-*` shots do not use full-body pose prompts. Shot coverage, product truth, and visibility of defining features override pose variety.

| Shot ID | Environment | Coverage | Non-negotiable purpose |
|---|---|---|---|
| `ST-FRONT-01` | studio | full body front | Neutral hero; complete outfit and front construction clear |
| `ST-FRONT-02` | studio | full body front | Different natural pose; no hidden defining features |
| `ST-SIDE-L45` | studio | left 45-degree | Show side silhouette and depth without twisting construction |
| `ST-SIDE-R45` | studio | right 45-degree | Distinct pose; preserve proportions and styling |
| `ST-BACK-01` | studio | full body back | Hair/arms clear of defining back construction |
| `ST-BACK-02` | studio | back three-quarter | Different back action; complete product still readable |
| `ST-HALF-01` | studio | half body | Primary product focus; natural expression |
| `ST-HALF-02` | studio | half body | Different hand placement; do not cover closures or waist |
| `ST-DETAIL-01` | studio | close detail | Product-type feature 1 |
| `ST-DETAIL-02` | studio | close detail | Product-type feature 2 |
| `ST-DETAIL-03` | studio | close detail | Product-type feature 3 |
| `ST-DETAIL-04` | studio | close detail | Product-type feature 4 or supplied special feature |
| `STREET-01` | city street | full body front/mid-step | Clean daylight street hero, no visible brand clutter |
| `STREET-02` | city street | side/three-quarter | Natural movement and silhouette |
| `STREET-03` | city street | back/three-quarter | Back construction readable, hair controlled |
| `STREET-04` | city street | full or half body | Distinct editorial action with product still dominant |

## Detail allocation

- `top`: collar/neckline; placket/chest; sleeve/cuff; fabric or hem.
- `bottom`: waistband/rise; pocket/hip-thigh; fabric; trouser cuff or skirt hem.
- `dress`: collar/neckline; waist/closure; fabric; hem or defining craft.
- `outerwear`: collar; placket/closure; pocket; cuff or fabric.
- `set`: two upper-piece details and two lower-piece details; both pieces remain visible together in all applicable full-body images.

When an authoritative detail image shows embroidery, print, unusual hardware, special buttons, pleats, lace, or another defining selling feature, replace the least informative generic detail shot with that feature. Never fabricate a detail.

## Environment locks

- Studio: light gray-white seamless backdrop, soft even light, restrained natural floor shadow, no furniture or props.
- Street: clean modern city street, natural daylight, uncluttered background, no prominent pedestrians, vehicles, shop signs, advertisements, or visible trademarks.
