# Configuration Options

This document describes the configurable parameters for the Taobao Lookbook Generator. Settings can be specified in a job configuration file or passed as runtime parameters.

## Job Configuration File

Create a `job-config.json` in the job folder with the following structure:

```json
{
  "sku": "PRODUCT-SKU-001",
  "color": "powder blue",
  "product_type": "dress",
  "mode": "standard",
  "shot_count": 16,
  "studio_count": 12,
  "street_count": 4,
  "max_retry_rounds": 3,
  "budget_cap_usd": null,
  "auto_approve_a_grade": true,
  "batch_pause_points": [],
  "model_authorization_confirmed": true,
  "custom_shot_plan": null,
  "custom_pose_library": null,
  "removal_defaults": ["handbag", "bag_strap"],
  "custom_scenes": [],
  "generation_params": {
    "default_resolution": "1536x2048",
    "quality": "highest",
    "seed": null
  }
}
```

## Parameter Reference

### Required Parameters

**`sku`** (string)  
Product SKU identifier. One job per SKU-color combination.

**`color`** (string)  
The exact color of the product for this job. Use descriptive color names (e.g., "powder blue", "deep burgundy", "off-white"). Multi-color products require separate jobs.

**`product_type`** (enum: `"dress"` | `"top"` | `"bottom"` | `"set"` | `"outerwear"`)  
Primary product category. Determines detail allocation and coverage strategy.

**`mode`** (enum: `"standard"` | `"premium"` | `"custom_scene"`, default: `"standard"`)  
Generation mode:
- `"standard"`: 12 studio + 4 street (default)
- `"premium"`: 16-20 shots, 5 retry rounds, maximum quality
- `"custom_scene"`: Generates base 16 studio images, then creates additional versions with user-provided scene backgrounds

**`model_authorization_confirmed`** (boolean)  
User confirms the model is an adult and authorized for AI generation and commercial use. Must be `true` to proceed.

---

### Shot Configuration

**`shot_count`** (integer, default: `16`)  
Total number of images to generate. 
- **Default**: 16 (standard Taobao lookbook set)
- **Range**: 8–24
- **Recommendation**: Keep at 16 for consistency unless the product complexity requires more or fewer shots

**`studio_count`** (integer, default: `12`)  
Number of studio shots (seamless white/light gray background).
- Must be ≥ `shot_count - street_count`
- Typical split: 12 studio + 4 street = 16 total

**`street_count`** (integer, default: `4`)  
Number of clean modern city street shots.
- Must be ≥ 0 and ≤ `shot_count`
- Set to `0` for studio-only jobs

**`custom_shot_plan`** (string path or null, default: `null`)  
Path to a custom shot plan file that overrides [references/shot-plan.md](shot-plan.md).  
Use when the standard 16-shot plan doesn't fit the product type (e.g., accessories, special editorial requirements).

**`custom_pose_library`** (string path or null, default: `null`)  
Path to a custom pose library that overrides [references/pose-library.md](pose-library.md).  
Use when the standard 12-pose library needs expansion or product-specific poses (e.g., outerwear with hand-in-pocket emphasis).

---

### Retry and Quality Control

**`max_retry_rounds`** (integer, default: `3`)  
Maximum regeneration attempts per shot after the original candidate (round 0).
- **Default**: 3 retries → rounds 0, 1, 2, 3 (4 total attempts)
- **Range**: 1–5
- **Higher values**: More chances to fix issues, but higher cost
- **Lower values**: Faster job completion, but more shots may end up in `human-review/`

**`auto_approve_a_grade`** (boolean, default: `true`)  
Automatically move A-grade images to `final/` without user confirmation.
- `true`: Fully automatic workflow (recommended for precision mode with detailed locks)
- `false`: Pause after each A-grade for user visual confirmation before moving to `final/`

**`batch_pause_points`** (array of integers, default: `[]`)  
Shot indices where the workflow pauses for user review before continuing.
- **Empty array** (default): No pauses, fully automatic
- **Example**: `[4, 8, 12, 16]` pauses after shots 1-4, 5-8, 9-12, 13-16
- **Use case**: When user wants to verify early shots before committing to the full set

---

### Cost Management

**`budget_cap_usd`** (number or null, default: `null`)  
Maximum allowed cost in USD for this job.
- `null`: No cap, proceed regardless of estimated cost
- **Number**: Stop if estimated cost exceeds this value and prompt user for approval
- **Estimation**: Assumes average 1.5 generations per shot (original + partial retries)
- **Actual cost**: Tracked in real-time; job stops if cap is reached mid-generation

---

### Styling Defaults

**`removal_defaults`** (array of strings, default: `["handbag", "bag_strap"]`)  
Items to remove by default from all styling references unless explicitly included in the styling_lock.
- **Common removals**: `"handbag"`, `"bag_strap"`, `"shopping_bag"`, `"phone"`, `"sunglasses_in_hand"`
- **Empty array**: Do not remove any items by default
- **Note**: Only applies when items are in the reference but not part of the intended styling

**`custom_scenes`** (array of objects, default: `[]`)  
Custom scene backgrounds for `custom_scene` mode. Each scene object specifies:
```json
{
  "scene_id": "cafe_interior",
  "scene_name": "Cozy Cafe Interior",
  "background_image_path": "scenes/cafe_bg.jpg",
  "shot_count": 8,
  "lighting_direction": "soft window light from left",
  "atmosphere": "warm, relaxed, natural daylight",
  "ground_surface": "light wood floor",
  "depth_cues": "blurred cafe background with bokeh",
  "shadow_type": "soft natural shadow",
  "color_temperature": "warm (3500K-4500K)"
}
```

- **`scene_id`**: Unique identifier (kebab-case)
- **`scene_name`**: Human-readable name
- **`background_image_path`**: Path to the scene background image (must be high resolution, ideally 2000px+ width)
- **`shot_count`**: Number of shots to generate in this scene (typically 4-8)
- **`lighting_direction`**: Describes the main light source direction and quality
- **`atmosphere`**: Overall mood and lighting characteristics
- **`ground_surface`**: Type of ground/floor for shadow generation
- **`depth_cues`**: Background blur, bokeh, or other depth indicators
- **`shadow_type`**: How model shadow should appear (soft/hard/long/short)
- **`color_temperature`**: Warm/cool/neutral color cast to match scene

**Example multi-scene configuration**:
```json
"custom_scenes": [
  {
    "scene_id": "modern_cafe",
    "scene_name": "Modern Cafe",
    "background_image_path": "scenes/cafe.jpg",
    "shot_count": 6,
    "lighting_direction": "soft window light from left",
    "atmosphere": "warm, natural, casual",
    "ground_surface": "light wood floor",
    "depth_cues": "blurred interior with bokeh",
    "shadow_type": "soft natural shadow",
    "color_temperature": "warm (4000K)"
  },
  {
    "scene_id": "urban_street",
    "scene_name": "Urban Street",
    "background_image_path": "scenes/street.jpg",
    "shot_count": 6,
    "lighting_direction": "natural daylight from above",
    "atmosphere": "bright, clean, modern city",
    "ground_surface": "concrete pavement",
    "depth_cues": "blurred buildings and street",
    "shadow_type": "moderate natural shadow",
    "color_temperature": "neutral (5500K)"
  },
  {
    "scene_id": "garden",
    "scene_name": "Garden Park",
    "background_image_path": "scenes/garden.jpg",
    "shot_count": 4,
    "lighting_direction": "dappled sunlight through trees",
    "atmosphere": "fresh, natural, peaceful",
    "ground_surface": "grass or stone path",
    "depth_cues": "soft green foliage blur",
    "shadow_type": "soft dappled shadow",
    "color_temperature": "slightly cool (5800K)"
  }
]
```

---

### Generation Parameters

**`generation_params.default_resolution`** (string, default: `"1536x2048"`)  
Output image resolution.
- **Default**: 1536×2048 px (3:4 portrait ratio)
- **Alternatives**: `"1200x1600"`, `"1800x2400"` (maintain 3:4 ratio)

**`generation_params.quality`** (enum: `"highest"` | `"high"` | `"standard"`, default: `"highest"`)  
JPG export quality level.
- `"highest"`: Maximum quality, larger file size (~500KB-1MB per image)
- `"high"`: Balanced quality (~300-500KB per image)
- `"standard"`: Acceptable for web preview (~200-300KB per image)

**`generation_params.seed`** (integer or null, default: `null`)  
Fixed random seed for reproducible generation.
- `null`: Random seed per generation (default, recommended)
- **Integer**: Use the same seed for all shots in the job
- **Use case**: Debugging or exact reproduction of a prior job

---

## Runtime Override

Parameters can be overridden at runtime by passing them as arguments to the skill invocation:

```bash
# Example: run with custom retry limit and budget cap
/taobao-lookbook-generator --max-retry-rounds 5 --budget-cap-usd 50
```

Runtime parameters take precedence over job-config.json values.

---

## Preset Configurations

### Standard Mode (Default)

```json
{
  "mode": "standard",
  "shot_count": 16,
  "studio_count": 12,
  "street_count": 4,
  "max_retry_rounds": 3
}
```

12 studio + 4 street shots. Suitable for most apparel products.

---

### Premium Mode (Maximum Quality)

```json
{
  "mode": "premium",
  "shot_count": 20,
  "studio_count": 14,
  "street_count": 6,
  "max_retry_rounds": 5,
  "generation_params": {
    "quality": "highest"
  }
}
```

Expands shot count to 20 and allows 5 retry rounds. Use for complex products, hero SKUs, or campaign launches.

---

### Studio-Only Mode

```json
{
  "mode": "standard",
  "shot_count": 16,
  "studio_count": 16,
  "street_count": 0
}
```

All shots use seamless studio background. Use for products where street context is not needed (e.g., formal wear, intimate apparel).

---

### Custom Scene Mode

```json
{
  "mode": "custom_scene",
  "shot_count": 16,
  "studio_count": 16,
  "street_count": 0,
  "custom_scenes": [
    {
      "scene_id": "brand_cafe",
      "scene_name": "Brand Flagship Cafe",
      "background_image_path": "scenes/brand_cafe.jpg",
      "shot_count": 8,
      "lighting_direction": "large window light from right",
      "atmosphere": "elegant, modern, soft natural light",
      "ground_surface": "polished marble floor",
      "depth_cues": "blurred cafe interior with subtle bokeh",
      "shadow_type": "soft directional shadow",
      "color_temperature": "neutral to slightly warm (5000K)"
    },
    {
      "scene_id": "city_plaza",
      "scene_name": "Modern City Plaza",
      "background_image_path": "scenes/plaza.jpg",
      "shot_count": 8,
      "lighting_direction": "overhead natural daylight",
      "atmosphere": "bright, clean, urban",
      "ground_surface": "light gray stone tiles",
      "depth_cues": "blurred modern architecture",
      "shadow_type": "moderate natural shadow",
      "color_temperature": "neutral (5500K)"
    }
  ]
}
```

**Workflow**:
1. Generate 16 base studio images (white background) first
2. For each custom scene, generate the specified shot_count using selected base images
3. Model, garment, and pose remain identical to base images
4. Only background, lighting integration, and shadows are adapted to match the scene

**Total output**: 16 base studio images + 16 custom scene images (8+8) = 32 images

**Use cases**:
- Brand-specific locations (flagship stores, signature cafes)
- Campaign-specific environments (seasonal, event-based)
- Multi-platform content (different scenes for different social channels)
- A/B testing product in various contexts

---

## Cost Estimation Formula

**Base cost per generation**: Varies by image generation service; assume ~$0.80–$1.50 per 1536×2048 image.

**Standard/Premium Mode Estimated Cost**:
```
Estimated cost = shot_count × average_generations_per_shot × cost_per_generation

Where:
- average_generations_per_shot ≈ 1.5 (assumes 50% of shots need one retry)
- Higher max_retry_rounds increases the worst-case cost but not the average
```

**Example** (16 shots, $1.00 per generation):
```
16 shots × 1.5 avg generations × $1.00 = $24.00 (estimated)
Worst case (all shots use max 3 retries): 16 × 4 = $64.00
Best case (all shots approved on first try): 16 × 1 = $16.00
```

**Custom Scene Mode Estimated Cost**:
```
Base studio images: 16 × 1.5 × $1.00 = $24.00
Custom scene generations: total_custom_scene_shots × 1.3 × $1.00

Example with 2 scenes (8 shots each):
- Base: $24.00
- Scene 1: 8 × 1.3 × $1.00 = $10.40
- Scene 2: 8 × 1.3 × $1.00 = $10.40
- Total: $44.80 (estimated)
```

Note: Custom scene generations typically have slightly lower retry rates (1.3× instead of 1.5×) because the base composition is already approved; only scene integration needs adjustment.

The workflow displays the estimated cost before starting generation and tracks actual cost in real-time.

---

## Validation Rules

On job start, the system validates:

1. `shot_count` = `studio_count` + `street_count` (for standard/premium modes)
2. `max_retry_rounds` ≥ 1 and ≤ 5
3. `product_type` is one of the five allowed values
4. `model_authorization_confirmed` is `true`
5. If `budget_cap_usd` is set, it's > 0
6. If `custom_shot_plan` or `custom_pose_library` is set, the file exists and is readable
7. For `custom_scene` mode:
   - `custom_scenes` array is not empty
   - Each scene has a valid `background_image_path` that exists and is readable
   - Each scene has a `scene_id` (unique within the job)
   - Sum of all `scene.shot_count` ≤ base `shot_count` (cannot request more scene shots than base images)
   - Each scene's `shot_count` ≥ 4 and ≤ 16

If validation fails, the job stops with an error message specifying which parameter is invalid.

---

## Backward Compatibility

Jobs without a `job-config.json` use all default values:
- 16 shots (12 studio + 4 street)
- 3 retry rounds
- No budget cap
- Auto-approve A-grade
- Standard resolution and highest quality

Existing jobs are not affected by configuration changes.
