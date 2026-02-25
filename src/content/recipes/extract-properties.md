---
title: "Extract Model Properties Recipe"
description: "Step-by-step guide to extracting metadata and properties from CAD models using APS Model Derivative API"
difficulty: "intermediate"
estimatedTime: "15 minutes"
prerequisites: ["Model uploaded and translated in APS", "Valid APS access token", "Basic API knowledge"]
apis: ["Model Derivative v2", "Authentication v2"]
keywords: ["APS", "properties", "metadata", "extraction", "BIM", "CAD", "Model Derivative"]
raps_commands: ["raps translate properties", "raps translate metadata", "raps translate manifest"]
raps_version: ">=4.14.0"
aps_apis:
  model_derivative: "v2"
  authentication: "v2"
last_verified: "February 2026"
---

# Extract Model Properties Recipe

**Guide to extracting metadata, properties, and model structure from CAD files using RAPS CLI**

---

## Goal

Extract structured data from CAD models (BIM properties, geometry info, material data, etc.) for analysis, reporting, or integration with other systems.

**What you'll achieve:**
- List model views/viewables from a translated file
- Navigate the object tree hierarchy
- Extract element properties (doors, windows, walls, etc.)
- Query specific properties by object ID

---

## Prerequisites

### Required Tools
- **RAPS CLI** v4.14.0+ installed
- **Autodesk Developer Account** with app credentials
- **CAD file** already uploaded and translated in APS (see [Upload-Translate recipe](./upload-translate-view.md))

### Required OAuth Scopes
```
data:read viewables:read
```

### Key Concept: URN and GUID

Property extraction requires two identifiers:
- **URN** - The base64-encoded identifier of the uploaded file
- **GUID** - The identifier of a specific model view (obtained from metadata)

---

## The Manual Way (Complex API Navigation)

<details>
<summary>Click to see manual property extraction</summary>

```javascript
const axios = require('axios');

// 1. Get manifest to confirm translation is complete
async function getManifest(token, urn) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/manifest`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 2. Get metadata (list of views/viewables)
async function getMetadata(token, urn) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 3. Get object tree for a specific view
async function getObjectTree(token, urn, guid) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata/${guid}`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 4. Get properties for a specific view (paginated)
async function getProperties(token, urn, guid) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata/${guid}/properties`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// Main workflow: manifest → metadata → tree → properties
async function extractProperties(token, urn) {
  const manifest = await getManifest(token, urn);
  if (manifest.status !== 'success') throw new Error('Translation not complete');

  const metadata = await getMetadata(token, urn);
  const viewGuid = metadata.data.metadata[0].guid; // first view

  const tree = await getObjectTree(token, urn, viewGuid);
  const properties = await getProperties(token, urn, viewGuid);

  return { metadata, tree, properties };
}
```

**Manual process requires navigating manifest, finding GUIDs, handling pagination...**

</details>

---

## The RAPS Way

### Step 1: Verify Translation is Complete

Before extracting properties, confirm the file has been translated:

```bash
# Check translation status
raps translate status "$URN"

# Or view full manifest
raps translate manifest "$URN"
```

Expected status: `success`

### Step 2: List Model Views (Metadata)

Get available views/viewables from the translated model:

```bash
# List all model views
raps translate metadata "$URN"
```

**Example output:**
```
┌──────────────────────────────────────┬──────────┬──────┐
│ GUID                                 │ Name     │ Role │
├──────────────────────────────────────┼──────────┼──────┤
│ 12345678-abcd-1234-5678-abcdef123456 │ 3D View  │ 3d   │
│ 87654321-dcba-4321-8765-fedcba654321 │ Floor 1  │ 2d   │
└──────────────────────────────────────┴──────────┴──────┘
```

Note the **GUID** of the view you want to explore.

### Step 3: View Object Tree

Navigate the model's hierarchical structure:

```bash
# Get the object tree for a specific view
raps translate tree "$URN" "12345678-abcd-1234-5678-abcdef123456"
```

This shows the parent-child hierarchy of model elements.

### Step 4: Extract Properties

Get detailed properties for all elements in a view:

```bash
# Get all properties for a view
raps translate properties "$URN" "12345678-abcd-1234-5678-abcdef123456"
```

**Example output:**
```
┌────────┬─────────────────────┬──────────────────┬──────────┐
│ Object │ Name                │ Category         │ Material │
├────────┼─────────────────────┼──────────────────┼──────────┤
│ 101    │ Interior Wall       │ Walls            │ Concrete │
│ 102    │ Entry Door          │ Doors            │ Wood     │
│ 103    │ Office Window       │ Windows          │ Glass    │
└────────┴─────────────────────┴──────────────────┴──────────┘
```

### Step 5: Query Specific Properties

Filter properties for specific objects:

```bash
# Get properties for specific object IDs
raps translate query-properties "$URN" "12345678-abcd-1234-5678-abcdef123456" \
  --filter "101,102,103"

# Limit to specific property fields
raps translate query-properties "$URN" "12345678-abcd-1234-5678-abcdef123456" \
  --filter "101,102" \
  --fields "Name,Area,Volume,Material"
```

---

## Working with Different Regions

If your data is stored in a non-US region:

```bash
# Specify region for metadata
raps translate metadata "$URN" --region EMEA

# Specify region for properties
raps translate properties "$URN" "$GUID" --region EMEA

# Available regions: US, EMEA, AUS, CAN, DEU, IND, JPN, GBR
```

---

## Output Formats

Control how results are displayed:

```bash
# Table format (default, human-readable)
raps translate properties "$URN" "$GUID" --output table

# JSON format (machine-readable)
raps translate properties "$URN" "$GUID" --output json

# Save JSON to file
raps translate properties "$URN" "$GUID" --output json > properties.json
```

---

## Complete Workflow Example

End-to-end script for property extraction:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration
BUCKET="my-project-bucket"
FILE="building.rvt"

# 1. Authenticate
raps auth test

# 2. Upload file
raps object upload "$BUCKET" "$FILE"

# 3. Build URN
URN=$(echo -n "urn:adsk.objects:os.object:$BUCKET:$FILE" | base64 | tr '+/' '-_' | tr -d '=')

# 4. Translate and wait
raps translate start "$URN" --format svf2 --wait

# 5. Get model views
echo "Available views:"
raps translate metadata "$URN"

# 6. Get GUID of first 3D view (you'd parse this from metadata output)
GUID="12345678-abcd-1234-5678-abcdef123456"

# 7. Extract object tree
echo "Object tree:"
raps translate tree "$URN" "$GUID"

# 8. Extract all properties
echo "Properties:"
raps translate properties "$URN" "$GUID"

# 9. Query specific objects
echo "Specific objects:"
raps translate query-properties "$URN" "$GUID" --filter "101,102,103"
```

---

## Post-Processing with External Tools

### Python Analysis

```python
import json
import subprocess

# Extract properties as JSON
result = subprocess.run(
    ["raps", "translate", "properties", URN, GUID, "--output", "json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)

# Analyze with pandas
import pandas as pd
df = pd.json_normalize(data)
print(df.describe())
```

### Pipe to jq

```bash
# Extract specific fields with jq
raps translate properties "$URN" "$GUID" --output json | jq '.[] | {name, category, area}'

# Count elements by category
raps translate properties "$URN" "$GUID" --output json | jq 'group_by(.category) | map({category: .[0].category, count: length})'
```

---

## Troubleshooting

### "No metadata found"

**Cause:** Model needs to be translated first
```bash
# Check if translation is complete
raps translate status "$URN"

# If not translated, start translation
raps translate start "$URN" --format svf2 --wait
```

### "Invalid GUID"

**Cause:** Using wrong view GUID
```bash
# List all available views to find correct GUID
raps translate metadata "$URN"
```

### "Empty properties"

**Cause:** Some model formats have limited property support
```bash
# Check what's in the manifest
raps translate manifest "$URN"

# List available derivatives
raps translate derivatives "$URN"
```

---

## Properties by File Type

| File Format | Typical Properties Available |
|-------------|------------------------------|
| **RVT (Revit)** | Categories, materials, levels, rooms, parameters, types |
| **DWG (AutoCAD)** | Layers, blocks, attributes, dimensions |
| **IPT/IAM (Inventor)** | Parts, assemblies, materials, mass properties |
| **IFC** | IfcWall, IfcDoor, classifications, material sets |
| **NWD (Navisworks)** | Clash groups, object properties, transform data |

---

*Last verified: February 2026 | RAPS v4.14.0 | Model Derivative API v2*
*Property extraction works with all major BIM and CAD formats supported by APS.*
