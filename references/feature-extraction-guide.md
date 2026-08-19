# Feature Extraction Guide

This guide instructs how to automatically extract detailed, prompt-ready descriptors from user-supplied reference images for the three locks: `identity_lock`, `product_lock`, and `styling_lock`.

## Purpose

Transform abstract feature categories into concrete, specific, prompt-ready text that can be inserted directly into generation calls. The extracted descriptors must be precise enough that different AI runs using the same locks produce consistent results across all 16 images.

---

## Identity Lock Extraction

For every model reference image provided, extract these detailed features and write them as continuous natural-language descriptors, not as a checklist.

### Core Identity Traits

**Analyze and describe:**

- **Overall impression**: age range (young adult 20-25, mature 30s, etc.), ethnicity/regional features, general demeanor (calm, energetic, confident, reserved)
- **Body type and proportions**: height impression (tall/medium/petite), build (slim/athletic/curvy), shoulder width (narrow/medium/broad), limb length (long-limbed/proportionate), waist definition, overall body silhouette
- **Skin**: tone (fair/light/medium/tan/deep), undertone (cool/neutral/warm), texture visibility (smooth/natural pores visible), any distinctive features (freckles, moles, beauty marks - describe location)
- **Hair**: color (specific shade: platinum blonde, honey blonde, ash brown, jet black, auburn, etc.), length (exact: chin-length, shoulder-length, mid-back, etc.), texture (straight/wavy/curly/coily, fine/medium/thick), style (loose, tucked behind ears, center part, side part), volume, natural vs styled appearance
- **Makeup level**: none/minimal/natural/moderate/editorial, specific notes (bare lips, nude lip, defined brows, subtle eyeliner, etc.)

### Face Geometry (Multiple Angles)

**Extract from frontal view:**

- **Face shape**: oval/round/square/heart/diamond/oblong, jaw definition, chin shape (pointed/rounded/square)
- **Forehead**: height (high/medium/low), width, hairline shape
- **Eyebrows**: color, thickness (thin/medium/full), arch shape (straight/soft arch/high arch), spacing
- **Eyes**: color (specific: light blue, hazel-green, dark brown, etc.), shape (almond/round/hooded/monolid), size relative to face, eye spacing (close-set/average/wide-set), eyelid visibility, lash length/density
- **Nose**: bridge width and height, nose tip shape (small/bulbous/refined), nostril width, overall nose length
- **Mouth**: lip fullness (thin/medium/full), lip shape (bow-shaped/straight/curved), mouth width, resting expression (neutral/slight upturn/slight downturn)
- **Cheekbones**: prominence (flat/subtle/defined/high), placement
- **Facial proportions**: eye-to-nose distance, nose-to-lip distance, overall balance

**Extract from side/three-quarter views if available:**

- **Profile**: forehead slope, brow ridge, nose bridge curve, nose tip projection, chin projection, jaw angle
- **Neck**: length (short/medium/long), thickness, visible structure
- **Head shape from side**: back of head curve, ear placement and size

**Extract from back view if available:**

- **Hair from back**: length confirmation, volume at nape, how hair falls on shoulders/back
- **Shoulder blade visibility**, upper back width, posture

### Expression and Demeanor Lock

- **Resting expression**: neutral/calm/confident/serious/gentle/approachable
- **Gaze direction tendency**: direct eye contact/slightly away/downward/upward
- **Mouth resting state**: closed/slightly parted/relaxed/tense
- **Expression intensity**: minimal/subtle/expressive/animated
- **Allowed variation**: "Expression may shift naturally between neutral calm and gentle微笑, but always understated and realistic; avoid exaggerated smile, overly serious face, or theatrical expression"

### Prompt-Ready Identity Block Template

Compile the above into a continuous paragraph:

```
[Age impression] [ethnicity/regional features] model with [demeanor]. [Body type and proportions in one sentence]. Skin is [tone with undertone], [texture description]. Hair is [specific color], [length], [texture and volume], [style details]. [Makeup level and specific elements].

Face shape is [shape] with [jaw and chin details]. Forehead is [height and width]. Eyebrows are [color], [thickness], [shape]. Eyes are [specific color], [shape], [size and spacing], [eyelid and lash details]. Nose has [bridge description], [tip shape], [nostril width]. Lips are [fullness], [shape], [mouth width]. Cheekbones are [prominence and placement].

From profile: [nose bridge curve], [chin projection], [neck length and thickness]. From back: [hair length and volume], [shoulder width].

Expression is consistently [resting expression], gaze [direction tendency], [mouth state]. Allow only [allowed variation].

Across all angles, preserve [list 3-5 most distinctive identity markers that must never change].
```

---

## Product Lock Extraction

For every product reference image (front/back/detail), extract precise construction and material details.

### Category and Silhouette

- **Product type**: dress/top/bottom/set/outerwear - be specific (A-line dress, fitted blouse, wide-leg trousers, bomber jacket, etc.)
- **Overall silhouette**: fitted/slim/regular/relaxed/oversized/boxy/flowy
- **Length**: exact position (above knee 5cm, at knee, mid-calf, ankle-length, cropped above navel, hip-length, etc.)
- **Fit character**: body-hugging/tailored/straight/loose/draped

### Construction Details by Zone

**Upper body products (dress/top/outerwear):**

- **Neckline/Collar**: specific type (crew neck, V-neck depth X cm, scoop neck, boat neck, square neck, turtleneck, Peter Pan collar, notched lapel, shawl collar, hood, etc.), width, depth, finishing (ribbed/bound/raw edge)
- **Shoulders**: natural/dropped/structured/padded, seam placement
- **Sleeves**: length (sleeveless/cap/short/elbow/three-quarter/long/extra-long), cut (set-in/raglan/dolman/kimono), cuff type (ribbed/button/elastic/open), width (fitted/relaxed/wide)
- **Closure**: none/buttons (number, size, spacing, type: flat/domed/decorative)/zipper (front/side/back, length, exposed/concealed)/ties/snaps/hidden placket
- **Bodice/Torso**: darts, seams, panel construction, waist definition (none/elastic/tie/belt loops/fitted seaming)

**Lower body products (dress/bottom):**

- **Waist**: rise (low/mid/high), waistband type (elastic/fitted/fold-over/drawstring/belt loops), width, closure (zipper side/back/button fly)
- **Hip and thigh**: fit through hip, pocket presence and type (none/side seam/patch/welt/invisible), pocket placement and size
- **Leg (trousers) / Skirt body**: cut (straight/tapered/wide/A-line/pleated/gathered/tiered), silhouette through length, seam details
- **Hem**: type (raw/folded/ribbed/elastic/ruffled/scalloped/asymmetric), width, finishing, exact length measurement
- **Back construction**: yoke/seaming/pocket placement/elastic/zipper

### Material and Surface

- **Fabric type**: cotton/linen/wool/silk/polyester/knit/woven/denim - be specific (jersey knit, twill weave, brushed cotton, satin, etc.)
- **Texture**: smooth/textured/ribbed/cable knit/waffle/corduroy/terry/bouclé, surface feel (crisp/soft/stiff/fluid)
- **Weight and drape**: lightweight-fluid/medium-structured/heavyweight-stiff, how it hangs on body
- **Surface treatment**: plain/printed/embroidered/quilted/pleated, describe visible texture detail
- **Sheen level**: matte/slight sheen/satin/glossy

### Color and Pattern

- **Base color**: exact shade (not just "blue" but "soft powder blue" or "deep navy blue"), use specific color names
- **Undertone**: cool/neutral/warm
- **Saturation**: pale/muted/vibrant/deep/dark
- **Pattern if present**: type (stripe/plaid/floral/geometric/abstract/animal print), scale (micro/small/medium/large), density (sparse/moderate/dense), colors involved, pattern direction/orientation, repeat size

### Print/Embellishment Details

If the product has print, embroidery, appliqué, or other surface decoration:

- **Type and technique**: screen print/digital print/embroidery/sequins/beading/appliqué
- **Motif description**: specific (small scattered daisies, vertical pinstripes 0.5cm apart, large abstract brush strokes, etc.)
- **Placement**: all-over/chest only/hem border/asymmetric/panel-specific
- **Scale and density**: measure or estimate (flowers are 3cm diameter, spaced 5cm apart)
- **Color palette**: exact colors in the pattern

### Hardware and Trims

- **Buttons**: count, size (small/medium/large/oversized), material (plastic/metal/wood/covered), color, shape
- **Zippers**: metal/plastic, color (matching/contrast), teeth size, pull style
- **Other hardware**: snaps, grommets, buckles, D-rings - describe material, finish, size
- **Trims**: piping, binding, contrast stitching, lace, fringe, tassels - describe color, width, placement

### Distinctive Features

List any unique selling points that must appear in every shot:

- Asymmetric hem, cut-out detail, wrap construction, layered panels, specific pleat type, visible brand signature (if approved), unusual pocket shape, decorative topstitching pattern, etc.

### Prompt-Ready Product Block Template

```
[Product type with specific silhouette] in [exact color with undertone and saturation]. [Fabric type and weight] with [texture description], [drape behavior].

[Neckline/collar full description with measurements]. [Shoulder and sleeve full description]. [Closure full description with count and placement]. [Torso construction including seams, darts, waist treatment].

[For bottoms: rise, waistband, hip fit, pocket details]. [Leg or skirt cut and silhouette]. [Hem type and exact length position].

[If pattern: pattern type, scale, density, color palette, orientation, repeat].

[If embellishment: type, motif, placement, scale, colors].

[Hardware: buttons/zippers/trims with material, count, size, color].

Distinctive features that must appear in every shot: [list 3-5 critical elements].

Across all angles and poses, the garment must maintain [length], [color], [key construction element], and [distinctive feature]; natural folds and drape are allowed but must not alter these core attributes.
```

---

## Styling Lock Extraction

For every complete styling reference, extract all supporting garments and accessories.

### Layer-by-layer inventory

List every visible item from skin outward:

**If the primary product is a top or dress:**

- **Bottom garment** (if visible): type (skirt/trousers/shorts/jeans), color, length, fit, material impression, any visible details
- **Outerwear** (if layered): type, color, how worn (open/closed/draped)

**If the primary product is a bottom:**

- **Top garment**: type (T-shirt/blouse/sweater/tank), color, neckline, sleeve length, fit, tucked/untucked
- **Outerwear** (if layered): type, color, how worn

**If the primary product is outerwear:**

- **Underlayer top**: type, color, neckline, visibility
- **Underlayer bottom**: type, color, length, fit

**If the primary product is a set:**

- List only the two pieces that comprise the set and confirm they must always appear together

### Footwear

- **Shoe type**: sneakers/boots/sandals/heels/flats/loafers/mules - be specific (ankle boots, platform sandals, ballet flats)
- **Color and material**: exact color, material (leather/canvas/suede/synthetic), finish (matte/glossy/metallic)
- **Style details**: laces/buckles/straps, heel height if applicable, toe shape (round/pointed/square/open), any distinctive features
- **Visible branding**: if a logo or brand mark is visible and approved, note it; otherwise note "no visible branding"

### Accessories

List only what is actually visible in the reference:

- **Bags**: type (tote/crossbody/clutch/backpack), size, color, material, how carried
- **Jewelry**: necklace/earrings/rings/bracelets - type, material (gold/silver/beaded), size, placement
- **Headwear**: hat/scarf/hairband - type, color, material, how worn
- **Other**: belt (width, color, buckle), watch, sunglasses, scarf - describe each specifically

### Removal Instructions

If the user typically wants certain items removed:

```
Default removal: [handbags and bag straps]. When removed, ensure [hands/arms/background] are naturally repaired with no trace of the removed item.

Never add: [list items that should not appear unless explicitly in a reference - e.g., jewelry not supplied, additional bags, props, branded items]
```

### Prompt-Ready Styling Block Template

```
Supporting garments:
[If applicable: bottom is [type], [color], [length], [fit and material], [details]]
[If applicable: top is [type], [color], [neckline], [sleeve length], [fit], [how worn]]
[If applicable: outer layer is [type], [color], [how worn], [details]]

Footwear: [shoe type], [color], [material and finish], [style details], [branding note].

Accessories: [list each visible accessory with full description].

Default removal: [items to remove] with natural repair.

Absolutely do not add: [items that must never appear].

Across all shots, maintain the exact [bottom/top color], [shoe type and color], and [any distinctive accessory]; never swap a piece, recolor it, or introduce an unlisted item.
```

---

## Conflict Resolution Rules

When analyzing multiple reference images, conflicts may appear. Apply this hierarchy:

1. **Product front/back/detail references** define product construction, color, length, texture, and all hard product attributes
2. **Complete styling references** define the outfit combination and supporting garments
3. **Model references** define only the person - face, body, hair, skin tone
4. **If product color differs** between product-only shot and styling shot: use the product-only shot color as truth
5. **If garment length differs**: use the measurement from the clearest unobstructed view, prioritizing product reference over styling reference
6. **If a detail is visible in one reference but hidden in another**: use the visible evidence and note the limitation

### Unknown/Hidden feature protocol

When a critical feature is not visible in any reference:

```
[Feature category] is not clearly visible in supplied references. Visible evidence shows: [what you can see]. Hidden or unclear: [what you cannot confirm].

STOP: Request from user: "[exact missing view needed - e.g., 'product back view with hem and closure visible', 'model face frontal view with clear eye and nose detail', 'garment texture close-up showing print scale']"
```

Do not guess, infer, or use "typical" or "standard" as a substitute for missing visual evidence.

---

## Output Format

After extraction, compile three complete blocks in the job manifest:

```json
{
  "identity_lock": {
    "quick_summary": "[one-sentence overview]",
    "detailed_descriptors": "[full prompt-ready paragraph from template]",
    "distinctive_markers": ["marker1", "marker2", "marker3"],
    "angle_notes": {
      "frontal": "[specific frontal preservation notes]",
      "side": "[specific side preservation notes]",
      "back": "[specific back preservation notes]"
    }
  },
  "product_lock": {
    "quick_summary": "[one-sentence overview]",
    "detailed_descriptors": "[full prompt-ready paragraph from template]",
    "distinctive_features": ["feature1", "feature2", "feature3"],
    "per_angle_visibility": "[which features are visible from which angles]"
  },
  "styling_lock": {
    "quick_summary": "[one-sentence overview]",
    "detailed_descriptors": "[full prompt-ready paragraph from template]",
    "removal_list": ["item1", "item2"],
    "never_add_list": ["item1", "item2"]
  }
}
```

These blocks are then inserted verbatim into every generation prompt.
