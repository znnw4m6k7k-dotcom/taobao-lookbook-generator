# Input Contract

Use one job folder for one SKU and one color. The user must own or be authorized to use all supplied commercial material.

## Required source roles

| Role | Minimum evidence | Authority |
|---|---|---|
| `model` | Clear adult face plus clear full-body proportions | Person only |
| `product` | Primary product front and back | Product construction and color |
| `product_detail` | Clear close-ups of every defining feature | Texture, print, trims, seams, closures |
| `styling` | Complete outfit front and back | Supporting garments and supplied accessories |

The same photograph may fill two roles only when it clearly contains the required evidence. Keep role labels explicit; never let a styling image redefine a product feature that is clearer in the product references.

## Runtime request fields

```yaml
sku: ""
color: ""
product_type: dress | top | bottom | set | outerwear
primary_product: ""
model_authorized_for_ai_and_commercial_use: true
```

## Stop conditions

Stop before generation when:

- adult status or commercial likeness authorization is unconfirmed;
- face or full-body identity evidence is too blurred, obstructed, or inconsistent;
- product front, back, exact color, or a defining detail is missing or contradictory;
- complete styling front/back is missing or conflicts without an authoritative resolution;
- more than one product color is mixed in one job;
- the primary product cannot be distinguished from supporting garments;
- a set's top/bottom membership is unclear.

State the missing role and exact replacement image needed. Do not invent hidden structure or use a plausible substitute.

