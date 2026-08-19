# Workflow Stages

This document describes the complete workflow for all three generation modes in the Taobao Lookbook Generator.

## Overview

All modes follow the same three-phase structure:
1. **Pre-generation Phase**: Validation, feature extraction, planning, cost estimation
2. **Generation Phase**: Image generation with review and retry loops
3. **Post-generation Phase**: Final tallying, manifest saving, summary display

The specific steps within each phase vary by mode.

---

## Pre-generation Phase

### Step 1: Source Validation

Read [input-contract.md](input-contract.md) and verify:
- Model face references (frontal, and ideally side/back)
- Model body proportion reference
- Product front/back views
- Product detail views
- Complete styling front/back views
- Model authorization confirmed in config

**Stop condition**: If any critical view is missing, blurred, contradictory, or hidden, STOP and request the exact missing view. Use the stop protocol:
```
[Feature category] is not clearly visible.
Visible evidence shows: [what you can see].
Hidden or unclear: [what you cannot confirm].
REQUEST: [exact missing view needed - e.g., "product back view showing hem and zipper"]
```

### Step 2: Mode Configuration

Read [configuration-options.md](configuration-options.md) and load `job-config.json` if present, or use defaults:
- `mode`: standard | premium | custom_scene
- `shot_count`, `studio_count`, `street_count`
- `max_retry_rounds`
- `budget_cap_usd`
- `custom_scenes` (for custom_scene mode)

**Validation**:
- **Standard/Premium**: Verify `shot_count = studio_count + street_count`
- **Custom Scene**: Verify `custom_scenes` array is not empty, each scene has valid `background_image_path`, each `scene_id` is unique, sum of scene `shot_count` ≤ base `shot_count`

### Step 3: Feature Extraction

Apply [feature-extraction-guide.md](feature-extraction-guide.md) to extract detailed prompt-ready descriptors.

**Label each source image with its role**:
- `model_face_primary`, `model_body_primary`
- `model_face_side`, `model_face_back` (if provided)
- `product_front`, `product_back`
- `product_detail_N` (numbered)
- `styling_complete_front`, `styling_complete_back`
- `pose_reference_N` (if provided)

**Extract the three locks**:

1. **`identity_lock`**: Build a detailed prompt-ready paragraph covering:
   - Face geometry: face shape, forehead, eyebrows, eyes with specific color, nose bridge and tip, lips, cheekbones
   - Hair: exact color shade, length, texture, style
   - Skin: tone with undertone, texture
   - Body proportions: height impression, build, shoulder width, limb length
   - Expression range
   - Distinctive markers
   - Angle-specific notes for frontal, side, back views

2. **`product_lock`**: Build a detailed prompt-ready paragraph covering:
   - Exact visible color with undertone
   - Fabric type and weight, texture and drape behavior
   - Construction zone by zone: neckline/collar, shoulder and sleeve, closure type, bodice/torso, waist treatment
   - For bottoms: rise, waistband type, hip fit, pocket details, leg/skirt cut, hem type and exact length position
   - Pattern details if present: type, scale, density, color palette, orientation
   - Embellishments if present: type, motif, placement, scale
   - Hardware and trims: buttons, zippers, other hardware with material, count, size, color
   - Distinctive features that must appear in every shot
   - Note: natural folds are allowed but must not alter core attributes like length, color, and key construction

3. **`styling_lock`**: Build a detailed prompt-ready paragraph covering:
   - Every supporting garment and accessory visible in complete styling references
   - Supporting top/bottom/outerwear with type, color, fit, material
   - Footwear with type, color, material, finish, style details
   - Accessories with full description
   - Default removal instructions (e.g., "Remove handbags and bag straps; repair hands/arms/background naturally")
   - Never-add list (items that must not appear unless explicitly in a reference)

**Conflict resolution**: Use the hierarchy:
1. Product front/back/detail references → define the product
2. Complete-styling front/back references → define the outfit
3. Model face/body references → define the person only
4. Prior generated images → continuity aids only, never override original sources

### Step 4: Shot Plan

Read [shot-plan.md](shot-plan.md) or load `custom_shot_plan` if specified.

Assign shot IDs and coverage groups based on mode:
- **Standard**: 12 studio shots + 4 street shots = 16 total
- **Premium**: 14-20 shots (configurable studio/street ratio)
- **Custom Scene**: 16 studio shots only (base set)

### Step 5: Cost Estimation

Calculate estimated cost based on mode and configuration:

**Standard Mode**:
```
Estimated = shot_count × 1.5 (avg with retries) × cost_per_generation
Example: 16 × 1.5 × $1.00 = $24.00
```

**Premium Mode**:
```
Estimated = shot_count × 1.5 × cost_per_generation
Example: 20 × 1.5 × $1.00 = $30.00
```

**Custom Scene Mode**:
```
Base studio: 16 × 1.5 × $1.00 = $24.00
Each scene: scene_shot_count × 1.3 × $1.00
Example (2 scenes, 8 shots each): $24 + (8 × 1.3) + (8 × 1.3) = $44.80
```

Display the estimate. If `budget_cap_usd` is set and estimate exceeds it, request user approval before proceeding.

---

## Generation Phase

### Standard/Premium Modes

For each shot in the shot plan:

**1. Pose Selection**

Draw a pose from [pose-library.md](pose-library.md) that matches:
- Shot's camera angle (frontal, side, back, 3/4)
- Coverage group (full body, half body, detail)

Record the `pose_id` in the manifest. Avoid reuse within the same coverage group where possible.

**2. Prompt Construction**

Build the full generation prompt using:
- `identity_lock.detailed_descriptors` (unchanged across all shots)
- Angle-specific notes from `identity_lock.angle_notes` matching the current shot's view direction
- `product_lock.detailed_descriptors` (unchanged)
- `styling_lock.detailed_descriptors` (unchanged)
- Shot-specific variables:
  - Shot ID
  - Pose ID and pose description
  - Camera distance (full body / half body / detail)
  - Small natural expression variation within the locked range
  - Studio treatment (for studio shots): Apply [high-key-minimal-studio.md](high-key-minimal-studio.md) unchanged
  - Street treatment (for street shots): Clean modern city street parameters

**Output format constraints** (insert on every call):
- "Output must be a single portrait 3:4 ratio image (1536×2048px) containing one full-body model in one clean scene"
- "Do not generate a collage, grid, contact sheet, multi-panel layout, before/after comparison, side-by-side comparison, repeated model, duplicate views, split-screen, or any page design"
- "Do not include borders, frames, labels, captions, arrows, UI marks, watermarks, logos, brand names, or reference thumbnails"

**Photographic realism requirements**:
- Natural skin pores and texture
- Anatomically correct hands and limbs
- Real fabric behavior
- Plausible gravity and folds
- Coherent lens perspective
- Restrained retouching
- Physically consistent lighting

**3. Generate Image**

Call the built-in image-generation tool with:
- Full prompt
- Labeled reference images with explicit roles (attach all source images)
- Configured resolution (default 1536×2048)
- Quality setting (default: highest)

**4. Review**

Invoke `$taobao-lookbook-reviewer` with:
- The generated candidate image
- The three lock blocks from the job manifest
- The original labeled source images

The reviewer returns:
- Grade: A | B | C
- Targeted feedback (for B/C grades)

**5. Handle Grade**

- **A (approved)**:
  - Move or copy the approved JPG into `final/` using its shot ID as filename (e.g., `ST-FRONT-01.jpg`)
  - Record success in manifest
  - Proceed to next shot

- **B (minor issues) or C (major issues)**:
  - Parse the reviewer's targeted repair instruction
  - Increment `retry_counter` for this shot
  - If `retry_counter <= max_retry_rounds`: proceed to step 6
  - If `retry_counter > max_retry_rounds`: proceed to step 7

**6. Retry Loop**

Regenerate the shot with:
- Original prompt (all three locks unchanged)
- Add the reviewer's repair instruction as a supplementary directive
- Same pose_id and camera parameters

Review the retry independently. If it earns A, move to `final/` immediately. If it earns B/C and retries remain, repeat step 6.

**7. Max Retries Reached**

If round `max_retry_rounds` still receives B or C:
- Place the latest candidate image in `human-review/` with filename `[shot_id]_round[N]_[grade].jpg`
- Save the full review record in the manifest under this shot's entry
- Record the failure reason
- Continue with remaining shots

**Do not**:
- Put failed images in `final/`
- Substitute a different shot to hide the missing deliverable
- Stop the entire job due to one failed shot

### Custom Scene Mode

Custom scene mode has two stages:

#### Stage 1: Base Studio Image Generation

Generate 16 studio shots exactly as in Standard mode:
- All shots use seamless white/light gray background
- Apply high-key minimal studio treatment
- Review and retry as described above (up to `max_retry_rounds`)
- Move A-grade images to `final/studio/`

Record which shots succeeded and which failed. Scene versions can only be generated from A-grade base images.

#### Stage 2: Scene Version Generation

Read [custom-scene-workflow.md](custom-scene-workflow.md) for complete details.

For each custom scene in `custom_scenes` array:

**1. Load Scene Configuration**

Extract from the scene object:
- `scene_id`: unique identifier
- `scene_name`: human-readable name
- `background_image_path`: path to scene background image
- `shot_count`: number of shots to generate in this scene
- `lighting_direction`: main light source direction and quality
- `atmosphere`: overall mood and lighting characteristics
- `ground_surface`: type of ground/floor for shadow generation
- `depth_cues`: background blur, bokeh, or other depth indicators
- `shadow_type`: how model shadow should appear
- `color_temperature`: warm/cool/neutral color cast

Verify the `background_image_path` exists and is readable.

**2. Select Base Images**

**Default strategy**: Evenly distribute across the 16 base studio images.
- Example: If scene requests 8 shots, select base images 1, 3, 5, 7, 9, 11, 13, 15

**User override**: If config specifies exact base image IDs for this scene, use those instead.

**3. Generate Scene Versions**

For each selected base image:

**a. Load Base Image**

Load the A-grade base image from `final/studio/[base_shot_id].jpg` as the primary reference.

**b. Construct Scene Integration Prompt**

Use the template from [custom-scene-workflow.md](custom-scene-workflow.md):

```
Composite the model from the base reference image into the provided scene background.

PRESERVE EXACTLY:
- Model identity: [identity_lock.detailed_descriptors]
- Model pose: [exact pose from base image, reference pose_id: {pose_id}]
- Garment: [product_lock.detailed_descriptors]
- Styling: [styling_lock.detailed_descriptors]
- Camera angle and framing: [match base image exactly]
- Model expression: [match base image]

INTEGRATE NATURALLY:
- Background: Use the provided scene background image
- Lighting: {scene.lighting_direction}
- Atmosphere: {scene.atmosphere}
- Ground surface: {scene.ground_surface}
- Depth cues: {scene.depth_cues}
- Shadow: {scene.shadow_type}, cast on {scene.ground_surface}
- Color temperature: {scene.color_temperature}
- Light interaction: Model should receive ambient light and color cast from the scene
- Edge blending: Natural integration between model and background, no hard cutout edges
- Perspective match: Model scale and viewing angle must match scene perspective

OUTPUT CONSTRAINTS:
- Single 3:4 portrait image (1536×2048px)
- No collage, grid, or multi-panel layout
- No text, watermarks, or UI elements
- Photorealistic integration
```

**c. Generate Scene-Integrated Image**

Call image-generation tool with:
- Scene integration prompt
- Base studio image as reference
- Scene background image as reference
- All original labeled source images (for identity/product/styling reference)
- Configured resolution

**d. Review Scene Version**

Invoke `$taobao-lookbook-reviewer` with:
- The scene-integrated candidate image
- The base studio image (for consistency check)
- The three lock blocks
- The original labeled source images

**Review focus for scene versions**:
- Model identity match with base image
- Garment accuracy (color, construction, length, details)
- Pose consistency with base image
- Natural scene integration (lighting, shadows, perspective)
- No visible cutout edges or compositing artifacts
- Appropriate depth of field and background blur
- Color temperature consistency

**e. Handle Grade**

- **A**: Move to `final/{scene_id}/` with filename `SCENE-{scene_id}-{sequential_number}.jpg`
- **B/C**: Regenerate with targeted repair instruction, up to `max_retry_rounds`
- **After max retries**: Move to `human-review/{scene_id}/` with review record

**4. Scene Completion**

After all shots for this scene are processed, move to the next scene in `custom_scenes`.

---

## Post-generation Phase

### Step 1: Final Count

Tally A-grade images delivered vs target by category:

**Standard/Premium Modes**:
- Target: `shot_count`
- Actual: count of files in `final/`
- Report as: "16/16 delivered" or "14/16 delivered (2 in human-review)"

**Custom Scene Mode**:
- Base studio: Target 16, actual count in `final/studio/`
- For each scene: Target `scene.shot_count`, actual count in `final/{scene_id}/`
- Report as: "16 studio + 8 cafe_interior + 6 city_plaza (2 plaza shots in human-review)"

### Step 2: Cost Log

Write `cost-log.json` with:
```json
{
  "mode": "standard | premium | custom_scene",
  "estimated_cost_usd": 24.00,
  "actual_cost_usd": 28.50,
  "total_generation_calls": 19,
  "breakdown": {
    "base_studio": {"calls": 19, "cost": 19.00},
    "scene_cafe_interior": {"calls": 9, "cost": 9.00},
    "scene_city_plaza": {"calls": 10, "cost": 10.50}
  }
}
```

### Step 3: Job Manifest

Save complete job record to `job-manifest.json` including:

```json
{
  "job_id": "...",
  "mode": "standard | premium | custom_scene",
  "sku": "...",
  "color": "...",
  "product_type": "dress | top | bottom | set | outerwear",
  "created_at": "2026-08-19T10:30:00Z",
  
  "source_images": [
    {"path": "...", "role": "model_face_primary"},
    {"path": "...", "role": "product_front"},
    ...
  ],
  
  "identity_lock": {
    "quick_summary": "...",
    "detailed_descriptors": "[full prompt-ready paragraph]",
    "distinctive_markers": ["...", "...", "..."],
    "angle_notes": {
      "frontal": "...",
      "side": "...",
      "back": "..."
    }
  },
  
  "product_lock": {
    "quick_summary": "...",
    "detailed_descriptors": "[full prompt-ready paragraph]",
    "distinctive_features": ["...", "...", "..."],
    "per_angle_visibility": "..."
  },
  
  "styling_lock": {
    "quick_summary": "...",
    "detailed_descriptors": "[full prompt-ready paragraph]",
    "removal_list": ["handbag", "bag_strap"],
    "never_add_list": ["..."]
  },
  
  "base_studio_shots": [
    {
      "shot_id": "ST-FRONT-01",
      "pose_id": "pose_12",
      "status": "approved | failed",
      "grade": "A | B | C",
      "attempts": [
        {
          "round": 0,
          "grade": "B",
          "feedback": "...",
          "generation_prompt": "..."
        },
        {
          "round": 1,
          "grade": "A",
          "feedback": "Approved",
          "generation_prompt": "..."
        }
      ],
      "used_in_scenes": ["cafe_interior", "city_plaza"]
    },
    ...
  ],
  
  "custom_scenes": [
    {
      "scene_id": "cafe_interior",
      "scene_name": "Cozy Cafe Interior",
      "background_image_path": "scenes/cafe_bg.jpg",
      "requested_shot_count": 8,
      "base_images_used": ["ST-FRONT-01", "ST-SIDE-02", ...],
      "scene_shots": [
        {
          "shot_id": "SCENE-cafe_interior-01",
          "base_image_id": "ST-FRONT-01",
          "status": "approved | failed",
          "grade": "A | B | C",
          "attempts": [...]
        },
        ...
      ],
      "approved_count": 8,
      "failed_count": 0
    }
  ],
  
  "delivery_summary": {
    "base_studio_approved": 16,
    "base_studio_failed": 0,
    "scene_totals": {
      "cafe_interior": {"approved": 8, "failed": 0},
      "city_plaza": {"approved": 6, "failed": 2}
    }
  }
}
```

### Step 4: Summary Display

Show the user:

**Mode used**:
- "Standard mode: 12 studio + 4 street"
- "Premium mode: 20 shots (14 studio + 6 street)"
- "Custom scene mode: 16 base studio + 2 custom scenes"

**Delivery counts**:
- Standard/Premium: "16/16 delivered" or "14/16 delivered"
- Custom Scene: "16 studio + 8 cafe_interior + 8 city_plaza"

**If fewer than target**:
- List missing shot IDs with failure reasons from manifest
- Example: "Missing: ST-BACK-03 (max retries, anatomy issues), SCENE-plaza-07 (max retries, lighting mismatch)"

**Cost**:
- "Estimated: $24.00 | Actual: $28.50"
- "19 total generation calls"

**Human review directory** (if any shots failed):
- "2 shots require manual inspection in human-review/"
- List the directory structure

**Directory structure**:

Standard/Premium:
```
job_folder/
├── final/
│   ├── ST-FRONT-01.jpg
│   ├── ST-FRONT-02.jpg
│   └── ... (14-20 total)
├── human-review/
│   └── ST-BACK-03_round3_C.jpg
├── job-manifest.json
└── cost-log.json
```

Custom Scene:
```
job_folder/
├── final/
│   ├── studio/
│   │   ├── ST-FRONT-01.jpg
│   │   └── ... (16 total)
│   ├── cafe_interior/
│   │   ├── SCENE-cafe_interior-01.jpg
│   │   └── ... (8 total)
│   └── city_plaza/
│       ├── SCENE-city_plaza-01.jpg
│       └── ... (6 approved)
├── human-review/
│   ├── studio/
│   └── city_plaza/
│       ├── SCENE-city_plaza-07_round3_B.jpg
│       └── SCENE-city_plaza-08_round3_C.jpg
├── job-manifest.json
└── cost-log.json
```

---

## Automatic Flow

The entire workflow runs automatically with no user intervention required unless:

1. **Source material is insufficient**: Stop at pre-generation phase and request exact missing view
2. **Budget cap is exceeded**: Display estimate and wait for user approval
3. **All shots have been processed**: Display final summary

User does NOT need to:
- Approve each image individually (handled by automatic reviewer)
- Confirm retry decisions (handled by automatic retry loop)
- Intervene during generation (unless budget cap is hit)

User only reviews:
- The final summary showing delivery counts
- Contents of `human-review/` folder if any shots failed after max retries
