# Reviewer Specification

This document explains the `$taobao-lookbook-reviewer` agent, its evaluation criteria, grading system, and how it integrates into the generation workflow.

## Purpose

The reviewer is an independent quality assurance agent that evaluates each generated candidate image against the original source references and the three detailed lock blocks. It assigns a grade (A/B/C) and provides targeted repair instructions when issues are detected.

## What the Reviewer Receives

On every invocation:

1. **Original labeled source images**:
   - All model references (face_primary, body_primary, face_side, face_back, etc.)
   - All product references (product_front, product_back, product_detail_N)
   - All styling references (styling_complete_front, styling_complete_back)
   - Any pose references if provided

2. **The three detailed lock blocks** from job manifest:
   - `identity_lock.detailed_descriptors` (the full prompt-ready paragraph)
   - `product_lock.detailed_descriptors` (the full prompt-ready paragraph)
   - `styling_lock.detailed_descriptors` (the full prompt-ready paragraph)
   - Angle-specific notes for the current shot's view direction

3. **The candidate image** to evaluate

4. **Shot metadata**:
   - Shot ID (e.g., ST-FRONT-01, STREET-03)
   - Expected coverage (full body front, side 45-degree, detail, etc.)
   - Pose ID used
   - Generation round number (0 for original, 1-3 for retries)
   - Environment (studio/street)

## Evaluation Criteria

The reviewer checks seven dimensions. Each dimension can trigger a downgrade or block A-grade approval.

### 1. Identity Consistency

**Compare candidate against model references and identity_lock.**

Check:
- Face geometry matches: face shape, jaw line, chin, forehead proportions
- Eye color, shape, spacing, and expression match the lock
- Nose bridge, tip shape, and nostril width match
- Lip fullness, shape, and mouth width match
- Eyebrow color, thickness, and arch match
- Hair color (exact shade), length, texture, and style match
- Skin tone and undertone match
- Body proportions match: height impression, build, shoulder width, limb length
- Expression stays within the allowed range specified in the lock
- Distinctive markers listed in identity_lock are all present

**For angle-specific shots**: apply the corresponding angle_notes from identity_lock.

**Common identity failures**:
- Face changed (different person, altered features)
- Hair color shifted (blonde → brown, short → long)
- Wrong age impression (young adult → mature, teenager → adult)
- Body proportions changed (slim → curvy, tall → petite)
- Expression out of range (neutral lock → big smile, calm → theatrical)
- Skin tone or makeup drastically different

**Grade impact**:
- Major identity change (different face, wrong hair color/length): **C**
- Moderate drift (eye color slightly off, expression too exaggerated): **B**
- Minor natural variation (slight expression shift within range): **A acceptable**

### 2. Product Accuracy

**Compare candidate against product references and product_lock.**

Check:
- Color matches exactly (shade, saturation, undertone)
- Silhouette and fit character match (fitted/loose/oversized/etc.)
- Length is correct (measure against body landmarks: knee/mid-calf/ankle)
- Construction details match zone by zone:
  - Neckline/collar type and depth
  - Sleeve/leg length and cut
  - Closure type, count, placement (buttons/zipper/ties)
  - Waist treatment (elastic/belt/fitted seam)
  - Hem type and finishing
  - Pocket presence, type, and placement
- Fabric texture and drape behavior match (knit/woven, fluid/stiff, sheen level)
- Pattern matches if present: type, scale, density, color palette, orientation
- Embellishments match if present: type, motif, placement, scale
- Hardware and trims match: button count/style, zipper type, trim details
- All distinctive features from product_lock are visible and accurate

**Natural folds and drape are allowed** as long as they don't alter the core attributes.

**Common product failures**:
- Wrong color (blue → green, light gray → dark gray)
- Wrong length (knee-length → mid-calf, cropped → full-length)
- Missing or wrong construction detail (V-neck → round neck, short sleeves → long sleeves)
- Pattern wrong (stripe direction, print scale, missing motif)
- Wrong fabric texture (knit → woven, matte → shiny)
- Buttons wrong count or placement
- For sets: one piece missing, merged into dress, or recolored

**Grade impact**:
- Critical product error (wrong color, wrong length, missing piece in set): **C**
- Moderate error (neckline depth off, button count wrong, hem style wrong): **B**
- Minor natural variation (fold placement, slight drape difference): **A acceptable**

### 3. Styling Compliance

**Compare candidate against styling references and styling_lock.**

Check:
- All supporting garments present and correct (type, color, fit)
- Footwear matches: type, color, material, style details
- Accessories match the supplied list: jewelry, bags, belts, hats, etc.
- Items in removal_list are completely removed with natural repair
- Items in never_add_list are absent
- No invented or substituted items

**Common styling failures**:
- Supporting garment wrong color or type
- Shoes changed (black boots → white sneakers, heels → flats)
- Removed item (handbag) still visible or poorly repaired
- Added item not in references (jewelry, scarf, bag not supplied)
- For outerwear-as-primary: underlayer wrong or missing

**Grade impact**:
- Major styling error (wrong shoes, added unsupplied accessory, failed removal): **C**
- Moderate error (supporting garment color slightly off, accessory detail wrong): **B**
- Minor acceptable variation: **A acceptable**

### 4. Realism and Photography Quality

**Check technical photographic realism.**

Check:
- Skin has natural texture and visible pores (not waxy or over-smoothed)
- Hair looks real (individual strands, natural shine, not plastic)
- Hands and fingers anatomically correct (correct joint count, natural pose)
- Fabric behaves realistically (gravity, folds, drape, surface texture visible)
- Lighting is coherent and matches the environment lock (studio/street)
- Perspective is natural (no wide-angle distortion, no unnaturally stretched limbs)
- Shadows are plausible and consistent with light source
- No AI artifacts (halo edges, blurred boundaries, repeated patterns, malformed details)
- Background matches environment specification (seamless studio / clean street)

**For studio shots**: must match high-key-minimal-studio.md (soft diffused light, subtle shadow, 70-85mm perspective, f/5.6-f/8 depth, restrained tonality).

**For street shots**: natural daylight, clean modern city street, no prominent clutter/signs/vehicles/pedestrians.

**Common realism failures**:
- Plastic or waxy skin
- Malformed hands (extra/missing fingers, wrong joints)
- Fabric looks fake (over-smoothed, no texture, wrong drape)
- Wrong lighting (harsh flash in studio shot, dramatic rim light when not specified)
- AI artifacts (halo, blurred edges, repeated texture)
- Wrong background (busy street in studio shot, furniture in seamless studio)

**Grade impact**:
- Major realism failure (malformed anatomy, plastic materials, wrong environment): **C**
- Moderate issue (skin over-smoothed, lighting slightly off, minor artifacts): **B**
- Minor natural imperfection: **A acceptable**

### 5. Format and Output Compliance

**Check technical output specifications.**

Check:
- Single portrait 3:4 image (approximately 1536×2048px or correct ratio)
- Contains exactly one full-body model in one scene
- Not a collage, grid, multi-panel layout, comparison, split-screen, or repeated model
- No borders, frames, labels, captions, arrows, UI marks
- No watermarks, logos, brand names, or text overlays
- No reference thumbnail insets

**Common format failures**:
- Multiple people in frame
- Side-by-side comparison or before/after layout
- Grid or contact sheet
- Text, watermark, or logo visible
- Wrong aspect ratio (square, horizontal, or extreme vertical)
- Cropped body (only upper body when full body was required)

**Grade impact**:
- Format violation (multi-panel, text overlay, wrong ratio): **C**
- Moderate issue (slight crop, small unwanted element): **B**

### 6. Shot Purpose and Coverage

**Check whether the shot fulfills its assigned purpose.**

For each shot ID, verify:
- **Full body shots**: entire body visible from head to feet, no critical parts cropped
- **Half body shots**: chest/waist to head, product focus clear
- **Detail shots**: close-up of the specified product feature (collar, cuff, hem, fabric, etc.)
- **Front shots**: model facing camera, front construction visible
- **Side shots**: appropriate angle (45-degree or profile), side silhouette clear
- **Back shots**: back construction visible, hair not covering critical details
- **Street shots**: natural movement or action, product still dominant

**Pose compatibility**: the selected pose must not hide defining features. For example:
- Folded arms should not cover a chest print or neckline detail
- Hand in pocket pose used only when pocket exists in product
- Adjusting hem pose should not lift the hem and change perceived length

**Common coverage failures**:
- Full body shot but feet cropped out
- Detail shot too far away, feature not clear
- Back shot but hair covers the back construction
- Side shot but body twisted so front construction is hidden
- Pose hides a distinctive feature (folded arms cover print, hand covers closure)

**Grade impact**:
- Coverage failure (feet cropped in full body, wrong angle, feature hidden): **C**
- Moderate issue (feature partially obscured, slightly wrong framing): **B**

### 7. Consistency Across Set

**For retry rounds and later shots in the job, check consistency with already-approved images.**

Check:
- Same model identity (face, hair, body) as prior approved shots
- Same product color and construction as prior approved shots
- Same styling (supporting garments, shoes) as prior approved shots
- Natural expression variation allowed, but identity must remain locked

**This dimension only applies when comparing against approved shots in `final/`.**

**Common consistency failures**:
- Model face changed between shots (different person)
- Product color shifted (light blue in shot 1 → darker blue in shot 5)
- Shoes changed (boots in early shots → sneakers in later shots)
- Hair length or color changed mid-set

**Grade impact**:
- Major inconsistency (different face, different product): **C**
- Moderate drift (color shade slightly off, styling detail changed): **B**

---

## Grading System

### Grade A: Approved

**Criteria**: All seven dimensions pass. The image accurately represents the source references and locks, maintains photographic realism, meets format requirements, fulfills its shot purpose, and is consistent with the set.

**Minor acceptable variations**:
- Natural expression shift within the locked range
- Pose-created fold and drape differences that don't alter garment construction
- Slight lighting variation within the environment style lock
- Natural body weight shift or subtle posture change

**Action**: Move the image to `final/` with shot ID as filename. Record success in manifest.

---

### Grade B: Minor Issues

**Criteria**: One or two dimensions have moderate issues that reduce quality but don't invalidate the image. The core identity, product, and styling are recognizable, but there are noticeable deviations.

**Examples of B-grade issues**:
- Eye color slightly off (light brown instead of hazel-green)
- Neckline depth 2cm off from reference
- Supporting garment color shifted one shade (light gray → medium gray)
- Skin slightly over-smoothed but not fully plastic
- Slight format issue (minor crop, small unwanted element)
- Pose partially obscures a non-critical detail

**Repair instruction format**:
```
Grade: B
Issues detected:
1. [Dimension]: [specific issue] - observed: [what's wrong], expected: [what it should be]
2. [Dimension]: [specific issue] - observed: [what's wrong], expected: [what it should be]

Targeted repair:
- [Specific constraint to add for regeneration]
- [Specific constraint to add for regeneration]
```

**Action**: Regenerate with the targeted repair instructions added as supplementary constraints. All three lock blocks remain unchanged.

---

### Grade C: Major Issues

**Criteria**: One or more dimensions have critical failures that make the image unusable. The identity, product, or styling is significantly wrong, or the image has major realism/format violations.

**Examples of C-grade issues**:
- Wrong face (different person)
- Wrong hair color or length (blonde → brown, short → long)
- Wrong product color (blue → green)
- Wrong product length (knee → mid-calf)
- Missing piece in a set
- Malformed anatomy (extra fingers, wrong joints)
- Format violation (collage, text overlay, wrong ratio)
- Coverage failure (feet cropped in full body shot, critical feature hidden)

**Repair instruction format**:
```
Grade: C
Critical failures:
1. [Dimension]: [critical issue] - observed: [what's wrong], expected: [what it should be]
2. [Dimension]: [critical issue] - observed: [what's wrong], expected: [what it should be]

Targeted repair:
- [Specific constraint emphasizing the failed lock element]
- [Specific constraint emphasizing the failed lock element]
- [Additional negative constraint to prevent the failure mode]
```

**Action**: Regenerate with the targeted repair instructions. If this was round 3 (the third retry), place the image and review in `human-review/` and continue with remaining shots.

---

## Integration into Workflow

### After Each Generation

1. Generator produces candidate image for shot N
2. Invoke `$taobao-lookbook-reviewer` with:
   - All labeled source images
   - The three detailed lock blocks from manifest
   - The candidate image
   - Shot metadata (ID, coverage, pose_id, round, environment)
   - Path to `final/` directory (for consistency check against approved shots)

3. Reviewer returns:
   ```json
   {
     "grade": "A" | "B" | "C",
     "issues": [
       {
         "dimension": "identity_consistency" | "product_accuracy" | "styling_compliance" | "realism_quality" | "format_compliance" | "shot_coverage" | "set_consistency",
         "severity": "minor" | "moderate" | "critical",
         "observed": "[what is wrong]",
         "expected": "[what it should be]"
       }
     ],
     "targeted_repair": "[specific instructions for regeneration]",
     "approval_action": "move_to_final" | "regenerate_with_repair" | "escalate_to_human_review"
   }
   ```

4. Generator executes the action:
   - **A**: move to `final/`, proceed to next shot
   - **B** or **C**: regenerate with repair instruction, increment round counter
   - **C at round 3**: move to `human-review/`, proceed to next shot

### Reviewer Independence

- The reviewer does NOT see the generator's self-assessment or confidence score
- The reviewer does NOT know which round this is until told explicitly in metadata
- The reviewer evaluates only against sources and locks, not against the generator's intent
- The reviewer's targeted repair is the ONLY input for the next retry; the generator does not "remember" what it tried before

This independence prevents confirmation bias and ensures objective evaluation.

---

## Calibration and Consistency

The reviewer is calibrated to:

- **Prioritize identity and product accuracy** over minor styling or realism variations
- **Enforce hard locks strictly**: color, length, construction, face, hair are non-negotiable
- **Allow natural variation**: expression, folds, lighting subtlety, pose weight shift
- **Be pragmatic on realism**: real-world fashion photography has retouching; the standard is "realistic for a professional lookbook," not "unedited documentary"
- **Escalate consistently**: same failure type always gets the same grade (e.g., wrong product color is always C)

The reviewer does NOT:

- Provide subjective aesthetic opinions ("this pose is more elegant")
- Compare to external fashion trends or competitor lookbooks
- Suggest creative alternatives unless the current approach is failing repeatedly
- Grade based on personal preference; only based on source truth and locks

---

## User Override

The user cannot override the reviewer's grade during the automatic workflow. However:

- After the full job completes, the user can inspect `human-review/` and manually decide whether to accept a B/C image or regenerate it with adjusted locks
- If the user disagrees with consistent C-grading on a particular feature, they should adjust the corresponding lock in the manifest and rerun the job
- The reviewer's feedback in `human-review/` serves as diagnostic information for lock refinement

---

## Example Review

**Candidate**: ST-FRONT-01, round 0

**Grade**: B

**Issues**:
1. **identity_consistency** (moderate): Eye color observed as dark brown, expected hazel-green per identity_lock
2. **product_accuracy** (moderate): Skirt length observed at mid-calf, expected at knee per product_lock

**Targeted repair**:
- Emphasize in generation: "Eyes must be hazel-green with visible green undertone, not dark brown"
- Emphasize in generation: "Skirt hem must fall at knee level, approximately at the center of the kneecap, not mid-calf or below knee"

**Action**: regenerate_with_repair

---

This specification ensures consistent, objective quality control across all 16 shots without requiring user intervention during the workflow.
