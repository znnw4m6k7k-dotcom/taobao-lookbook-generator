# Custom Scene Workflow

This document describes the workflow for `custom_scene` mode, which generates base studio images and then creates additional versions with user-provided scene backgrounds.

## Overview

**Custom Scene Mode** allows you to:
1. Generate a complete set of 16 high-quality studio images (white background)
2. Create additional versions of selected images with custom scene backgrounds
3. Maintain perfect consistency of model, garment, pose, and styling across all scenes
4. Support multiple different scenes in a single job

## Workflow Stages

### Stage 1: Base Studio Image Generation

Identical to standard mode:
1. Extract identity/product/styling locks from source references
2. Generate 16 studio shots (1536×2048px, 3:4 portrait)
3. Apply high-key minimal studio treatment (seamless white/light gray background)
4. Review each image with `$taobao-lookbook-reviewer`
5. Retry B/C grades up to max_retry_rounds
6. Move A-grade images to `final/studio/`

**Output**: 16 A-grade studio images with consistent model, garment, and poses

### Stage 2: Scene Selection

For each custom scene defined in `custom_scenes` array:
1. Read scene configuration (background image, lighting, atmosphere, shot_count)
2. Select base images to use for this scene:
   - **Default strategy**: Evenly distribute across the 16 base images
   - **Example**: If scene requests 8 shots, select images 1, 3, 5, 7, 9, 11, 13, 15
   - **User override**: Allow user to specify exact base image IDs to use

### Stage 3: Scene Integration Generation

For each selected base image + scene combination:

**Input to generation**:
1. **Base image** (as image reference): The approved A-grade studio shot
2. **Scene background image**: User-provided background
3. **Scene integration prompt** (constructed from):
   - Original identity/product/styling locks (unchanged)
   - Base image's pose_id and camera parameters (unchanged)
   - Scene-specific parameters:
     - `lighting_direction`
     - `atmosphere`
     - `ground_surface`
     - `depth_cues`
     - `shadow_type`
     - `color_temperature`

**Generation instruction template**:
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

### Stage 4: Scene Version Review

Each scene-integrated image is reviewed with `$taobao-lookbook-reviewer`:

**Review focus for scene versions**:
- ✓ Model identity match with base image
- ✓ Garment accuracy (color, construction, length, details)
- ✓ Pose consistency with base image
- ✓ Natural scene integration (lighting, shadows, perspective)
- ✓ No visible cutout edges or compositing artifacts
- ✓ Appropriate depth of field and background blur
- ✓ Color temperature consistency

**Grading**:
- **A**: Perfect integration, move to `final/{scene_id}/`
- **B/C**: Regenerate with targeted repair instruction, up to 3 retries
- **After 3 retries**: Move to `human-review/{scene_id}/`

### Stage 5: Delivery

**Directory structure**:
```
job_folder/
├── final/
│   ├── studio/
│   │   ├── ST-FRONT-01.jpg
│   │   ├── ST-FRONT-02.jpg
│   │   └── ... (16 total)
│   ├── cafe_interior/
│   │   ├── SCENE-cafe_interior-01.jpg
│   │   ├── SCENE-cafe_interior-02.jpg
│   │   └── ... (8 total)
│   └── city_plaza/
│       ├── SCENE-city_plaza-01.jpg
│       ├── SCENE-city_plaza-02.jpg
│       └── ... (8 total)
├── human-review/
│   ├── studio/
│   ├── cafe_interior/
│   └── city_plaza/
├── job-manifest.json
└── cost-log.json
```

**Job manifest additions**:
```json
{
  "mode": "custom_scene",
  "base_studio_shots": [
    {
      "shot_id": "ST-FRONT-01",
      "status": "approved",
      "grade": "A",
      "pose_id": "pose_12",
      "used_in_scenes": ["cafe_interior", "city_plaza"]
    }
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
          "status": "approved",
          "grade": "A",
          "attempts": 1
        }
      ],
      "approved_count": 8,
      "failed_count": 0
    }
  ]
}
```

## Scene Background Image Requirements

User-provided scene background images should meet these criteria:

### Technical Requirements
- **Resolution**: Minimum 2000px width, ideally 2400px+
- **Aspect ratio**: Preferably 3:4 or 4:5 portrait orientation (can be cropped/adapted)
- **Format**: JPG or PNG
- **Quality**: High resolution, sharp focus on the background area where model will be placed

### Content Requirements
- **Clear foreground space**: Adequate empty space for a full-body model figure
- **Appropriate depth**: Background should have some depth cues (not a flat wall)
- **Consistent lighting**: Identifiable light direction and quality
- **No people**: Background should not contain visible people or human figures
- **Clean composition**: Avoid busy or cluttered backgrounds that compete with the model
- **Appropriate context**: Background should be contextually appropriate for apparel showcase

### Lighting Requirements
- **Identifiable light source**: Window light, overhead light, or natural outdoor light
- **Consistent direction**: Light should come from a consistent direction
- **Moderate contrast**: Avoid extremely high contrast or very dark shadows
- **Color neutrality**: Avoid extreme color casts unless intentional for brand aesthetic

### Examples of Good Scene Backgrounds
- Modern cafe interior with large windows (soft window light)
- Clean urban street with building backdrop (natural daylight)
- Minimalist retail space with neutral walls (controlled ambient light)
- Garden or park with soft foliage background (dappled natural light)
- Contemporary office lobby with glass walls (bright indirect light)

### Examples of Problematic Backgrounds
- Dark nightclub or bar interiors (too dark, complex lighting)
- Busy markets or crowded spaces (too cluttered)
- Extreme wide-angle architectural shots (perspective mismatch)
- Very shallow depth of field backgrounds (depth inconsistency)
- Backgrounds with visible people (compositing conflicts)

## Cost Implications

**Custom scene mode costs more** than standard mode due to additional generations:

**Example cost breakdown** (assuming $1.00 per generation):
- 16 base studio images: 16 × 1.5 (avg with retries) = $24.00
- Scene 1 (8 shots): 8 × 1.3 = $10.40
- Scene 2 (8 shots): 8 × 1.3 = $10.40
- **Total**: $44.80

**Cost factors**:
- Base image generation: ~$24 (same as standard mode)
- Each additional scene shot: ~$1.30 (slightly lower retry rate than base)
- More scenes = proportionally higher cost

**Budget planning**:
- 1 scene (8 shots): Add ~$10-12 to base cost
- 2 scenes (8 shots each): Add ~$20-24 to base cost
- 3 scenes (6 shots each): Add ~$23-28 to base cost

Set `budget_cap_usd` to enforce hard cost limits.

## Best Practices

### Scene Selection
- **2-3 scenes maximum** per job for cost efficiency
- Group related scenes (e.g., all indoor, all outdoor)
- Ensure scenes have compatible lighting and atmosphere

### Shot Allocation
- **6-8 shots per scene** provides good coverage without excessive cost
- Prioritize front-facing and 3/4 poses over back views for scene versions
- Consider product type: dresses need more coverage than simple tops

### Background Preparation
- Test scenes with 2-3 shots before committing to full set
- Prepare multiple background angle/crop variations
- Ensure brand consistency across all scene choices

### Quality Control
- Review scene integration samples before generating full set
- Check shadow direction consistency
- Verify color temperature matches scene
- Confirm perspective and scale look natural

## Troubleshooting

### Common Issues

**Issue**: Scene integration looks like a cutout, not natural
- **Cause**: Lighting direction mismatch or color temperature inconsistency
- **Fix**: Revise scene lighting description, specify edge light interaction

**Issue**: Model scale doesn't match scene perspective
- **Cause**: Background perspective conflicts with model camera angle
- **Fix**: Crop background to reduce extreme perspective, or select different base poses

**Issue**: Shadows look wrong or missing
- **Cause**: Shadow description doesn't match scene lighting
- **Fix**: Specify shadow direction, intensity, and ground surface texture

**Issue**: Color cast makes garment color look wrong
- **Cause**: Scene color temperature too strong
- **Fix**: Reduce scene color temperature intensity in description, or choose more neutral scene

**Issue**: Too many retries needed for scene shots
- **Cause**: Complex or problematic background image
- **Fix**: Simplify background, choose clearer foreground space, or use different scene

## Scene Library Recommendations

Build a reusable library of approved scene backgrounds:

**Versatile scenes** (work for most products):
- Clean modern cafe with window light
- Minimalist urban street
- Neutral interior with soft light
- Contemporary retail space

**Product-specific scenes**:
- **Casual wear**: Park, street, cafe
- **Formal wear**: Hotel lobby, office, elegant interior
- **Sportswear**: Gym, outdoor trail, modern fitness space
- **Outerwear**: Urban street, outdoor景观, city architecture

Keep approved scene backgrounds in a `scenes/` library with metadata for reuse across multiple SKUs.