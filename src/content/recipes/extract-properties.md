---
title: "Extract Model Properties Recipe"
description: "Step-by-step guide to extracting metadata, properties, and geometry data from CAD models using APS"
difficulty: "intermediate"
estimatedTime: "15 minutes"
prerequisites: ["Upload a model to APS", "Valid APS access token", "Basic API knowledge"]
apis: ["Model Derivative v2", "Authentication v2"]
keywords: ["APS", "properties", "metadata", "extraction", "BIM", "CAD", "Model Derivative"]
raps_commands: ["raps translate properties", "raps translate metadata", "raps translate manifest"]
raps_version: ">=4.11.0"
aps_apis:
  model_derivative: "v2"
  authentication: "v2"
last_verified: "February 2026"
---

# Extract Model Properties Recipe

**Complete guide to extracting metadata, properties, and geometry data from CAD models without viewing them**

---

## Goal

Extract structured data from CAD models (BIM properties, geometry info, material data, etc.) for analysis, reporting, or integration with other systems.

**What you'll achieve:**
- Extract element properties (doors, windows, walls, etc.)
- Get model metadata (units, coordinate systems, etc.)
- Export structured data to JSON, CSV, or database
- Filter and search properties programmatically

---

## Prerequisites

### Required Tools
- ✅ **RAPS CLI** v4.11.0+ installed
- ✅ **Autodesk Developer Account** with app credentials
- ✅ **CAD file** uploaded to APS (any supported format)

### Required Scopes
```bash
# Authentication scopes needed
data:read viewables:read
```

### Understanding Property Extraction

APS Model Derivative API extracts properties in these formats:
- **Metadata** - High-level model information
- **Properties** - Element-by-element detailed properties  
- **Hierarchy** - Model structure and relationships

---

## The Manual Way (Complex API Navigation)

<details>
<summary>🔍 Click to see manual property extraction (40+ API calls)</summary>

```javascript
const axios = require('axios');

// 1. Get model manifest
async function getManifest(token, urn) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/manifest`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 2. Find metadata viewable
function findMetadataViewable(manifest) {
  for (const derivative of manifest.derivatives) {
    for (const child of derivative.children || []) {
      if (child.role === 'Autodesk.CloudPlatform.PropertyDatabase') {
        return child.guid;
      }
    }
  }
  throw new Error('No metadata viewable found');
}

// 3. Get model metadata
async function getMetadata(token, urn, guid) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata/${guid}`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 4. Get object tree
async function getObjectTree(token, urn, guid) {
  const response = await axios.get(
    `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata/${guid}/objects`,
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data;
}

// 5. Get properties for each object (paginated)
async function getAllProperties(token, urn, guid) {
  let allProperties = [];
  let hasMore = true;
  let offset = 0;
  const pageSize = 1000;

  while (hasMore) {
    const response = await axios.get(
      `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/metadata/${guid}/properties`,
      {
        headers: { Authorization: `Bearer ${token}` },
        params: { offset, limit: pageSize }
      }
    );

    allProperties = allProperties.concat(response.data.collection);
    hasMore = response.data.collection.length === pageSize;
    offset += pageSize;
  }

  return allProperties;
}

// 6. Process and structure data
function processProperties(properties, metadata) {
  const structured = {
    modelInfo: metadata,
    elements: [],
    summary: {
      totalElements: 0,
      elementTypes: {},
      materials: new Set(),
      levels: new Set()
    }
  };

  for (const prop of properties) {
    const element = {
      dbId: prop.objectid,
      properties: {}
    };

    // Process property groups
    for (const group of prop.properties) {
      for (const [key, value] of Object.entries(group.properties)) {
        element.properties[key] = value;
        
        // Track materials and levels
        if (key.toLowerCase().includes('material')) {
          structured.summary.materials.add(value);
        }
        if (key.toLowerCase().includes('level')) {
          structured.summary.levels.add(value);
        }
      }
    }

    structured.elements.push(element);
    
    // Track element types
    const category = element.properties.Category || 'Unknown';
    structured.summary.elementTypes[category] = 
      (structured.summary.elementTypes[category] || 0) + 1;
  }

  structured.summary.totalElements = structured.elements.length;
  structured.summary.materials = Array.from(structured.summary.materials);
  structured.summary.levels = Array.from(structured.summary.levels);

  return structured;
}

// Main workflow
async function extractProperties(token, urn) {
  console.log('Getting manifest...');
  const manifest = await getManifest(token, urn);
  
  console.log('Finding metadata viewable...');
  const metadataGuid = findMetadataViewable(manifest);
  
  console.log('Getting model metadata...');
  const metadata = await getMetadata(token, urn, metadataGuid);
  
  console.log('Getting object tree...');
  const objectTree = await getObjectTree(token, urn, metadataGuid);
  
  console.log('Extracting all properties...');
  const properties = await getAllProperties(token, urn, metadataGuid);
  
  console.log('Processing data...');
  const structured = processProperties(properties, metadata);
  
  return structured;
}
```

**That's complex pagination, GUID navigation, and data processing!**

</details>

---

## The RAPS Way (3 Commands)

### Step 1: Get Model Metadata

```bash
# Extract high-level model information
raps translate metadata <urn>
```

**Output example:**
```json
{
  "metadata": {
    "name": "Office Building",
    "guid": "12345678-1234-5678-9abc-123456789012",
    "role": "3D",
    "units": "feet",
    "up_vector": [0, 0, 1],
    "front_vector": [0, 1, 0],
    "world_bounding_box": {
      "min": [-50, -30, 0],
      "max": [50, 30, 20]
    }
  }
}
```

### Step 2: Extract All Properties

```bash
# Extract detailed element properties to JSON file
raps translate properties <urn> --output properties.json --format detailed
```

**What happens:**
- Finds metadata viewable automatically
- Downloads all properties with pagination handling
- Structures data by element type
- Saves to structured JSON format

### Step 3: Generate Summary Report

```bash
# Create human-readable summary
raps translate properties <urn> --summary --output summary.csv
```

**Output example (CSV):**
```csv
Element_Type,Count,Average_Area,Total_Volume,Common_Materials
Wall,45,120.5,2850.0,"Concrete, Gypsum Board"
Door,12,21.0,0.0,"Wood, Steel"
Window,18,15.5,0.0,"Glass, Aluminum"
```

---

## Extraction Workflows by File Type

### BIM Models (Revit, ArchiCAD, IFC)

```bash
# Extract BIM-specific data
raps translate properties <rvt_urn> --filter-type "Walls,Doors,Windows,Floors" --include-materials --include-levels
```

**Typical BIM Properties:**
- Element categories (Walls, Doors, Windows, etc.)
- Material assignments
- Level/Floor associations
- Room/Space assignments
- Phasing information
- Type vs Instance parameters

### Mechanical CAD (Inventor, SolidWorks)

```bash
# Extract mechanical properties
raps translate properties <ipt_urn> --filter-type "Parts,Assemblies" --include-mass --include-materials
```

**Typical Mechanical Properties:**
- Part mass and volume
- Material specifications
- Assembly relationships
- Custom iProperties/parameters
- Manufacturing data

### Civil/Infrastructure (Civil 3D, InfraWorks)

```bash
# Extract civil engineering data
raps translate properties <dwg_urn> --filter-type "Alignments,Surfaces,Corridors" --include-elevation
```

**Typical Civil Properties:**
- Survey points and elevations
- Alignment parameters
- Surface definitions
- Corridor assemblies
- Pipe networks

---

## Filtering and Searching Properties

### Filter by Element Type

```bash
# Only extract doors and windows
raps translate properties <urn> --filter-category "Doors,Windows"

# Exclude structural elements
raps translate properties <urn> --exclude-category "Structural Framing,Structural Columns"
```

### Filter by Property Values

```bash
# Only elements with specific material
raps translate properties <urn> --filter-property "Material=Concrete"

# Elements above certain level
raps translate properties <urn> --filter-property "Level=Level 2,Level 3"
```

### Custom Property Queries

```bash
# Advanced filtering with queries
raps translate properties <urn> --query "Area > 100 AND Material CONTAINS 'Steel'"
```

---

## Output Formats

### 1. Detailed JSON (Default)

```bash
raps translate properties <urn> --output model_data.json
```

Structure:
```json
{
  "modelInfo": { ... },
  "elements": [
    {
      "dbId": 123,
      "category": "Walls",
      "properties": {
        "Name": "Interior Wall - Generic",
        "Area": 120.5,
        "Volume": 15.2,
        "Material": "Gypsum Board",
        "Level": "Level 1"
      }
    }
  ],
  "summary": { ... }
}
```

### 2. Flat CSV

```bash
raps translate properties <urn> --format csv --output elements.csv
```

Structure:
```csv
dbId,Category,Name,Area,Volume,Material,Level
123,Walls,Interior Wall - Generic,120.5,15.2,Gypsum Board,Level 1
124,Doors,Door - Single,21.0,0.0,Wood,Level 1
```

### 3. Excel Workbook

```bash
raps translate properties <urn> --format xlsx --output model_data.xlsx --include-charts
```

Creates workbook with:
- **Elements** sheet - All property data
- **Summary** sheet - Counts and totals by category
- **Materials** sheet - Material usage analysis
- **Charts** sheet - Visual summaries

### 4. Database Integration

```bash
# Insert directly into PostgreSQL
raps translate properties <urn> --to-database "postgresql://user:pass@localhost:5432/models"

# Insert into SQLite for local analysis
raps translate properties <urn> --to-database "sqlite:///models.db"
```

---

## Advanced Property Analysis

### Material Quantity Takeoff

```bash
# Generate material quantities report
raps translate properties <urn> --analyze materials --group-by "Material,Level" --calc "sum(Volume),sum(Area)"
```

Output:
```json
{
  "materialAnalysis": [
    {
      "material": "Concrete",
      "level": "Level 1",
      "totalVolume": 1250.5,
      "totalArea": 2850.0,
      "elementCount": 25
    }
  ]
}
```

### Cost Estimation Integration

```bash
# Extract data with cost parameters
raps translate properties <urn> --include-cost-params --apply-rates "rates.json"
```

Where `rates.json` contains:
```json
{
  "materialRates": {
    "Concrete": { "unit": "cubic_foot", "rate": 0.12 },
    "Steel": { "unit": "pound", "rate": 0.85 }
  }
}
```

### Space and Room Analysis

```bash
# Extract room/space data for space planning
raps translate properties <urn> --extract-spaces --include-boundaries --calc-adjacencies
```

---

## Property Comparison and Change Detection

### Compare Model Versions

```bash
# Compare properties between model versions
raps translate compare-properties <urn1> <urn2> --output changes.json
```

Output identifies:
- Added elements
- Deleted elements  
- Modified properties
- Moved elements

### Track Changes Over Time

```bash
# Store properties in version-controlled format
raps translate properties <urn> --output "properties_v$(date +%Y%m%d).json" --git-commit
```

---

## Integration Examples

### Python Data Analysis

```python
import json
import pandas as pd

# Load RAPS extracted properties
with open('properties.json', 'r') as f:
    data = json.load(f)

# Convert to pandas DataFrame for analysis
elements_df = pd.json_normalize(data['elements'])

# Analyze by category
category_summary = elements_df.groupby('category').agg({
    'properties.Area': ['count', 'sum', 'mean'],
    'properties.Volume': ['sum', 'mean']
}).round(2)

print(category_summary)

# Find largest elements by area
largest_elements = elements_df.nlargest(10, 'properties.Area')[
    ['category', 'properties.Name', 'properties.Area']
]

print(largest_elements)
```

### Power BI Integration

```bash
# Generate Power BI compatible format
raps translate properties <urn> --format powerbi --output model_data.pbix --include-relationships
```

### Excel Analysis Template

```bash
# Create Excel template with formulas
raps translate properties <urn> --format xlsx --template analysis --output model_analysis.xlsx
```

The template includes:
- Pivot tables for category analysis
- Charts for material distribution
- Formulas for cost calculations
- Conditional formatting for outliers

---

## Automation and Scheduling

### Batch Property Extraction

```bash
# Extract properties from multiple models
raps translate properties-batch --bucket my-models --output-dir ./extracted_data/ --parallel 3
```

### Scheduled Extraction

```bash
# Set up daily extraction for active projects
raps schedule properties-extraction --models @active_models.list --time "02:00" --output-format csv
```

### CI/CD Integration

```yaml
# GitHub Actions workflow
name: Extract Model Properties
on:
  push:
    paths: ['models/*.rvt']

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - name: Extract Properties
        run: |
          raps translate properties ${{ env.MODEL_URN }} --output properties.json
          # Upload to data warehouse, trigger analysis pipeline, etc.
```

---

## Performance Tips

### 1. Use Filters to Reduce Data Volume

```bash
# Extract only what you need
raps translate properties <urn> --filter-category "Walls,Doors" --exclude-properties "History,Constraints"
```

### 2. Parallelize Multiple Models

```bash
# Process multiple models simultaneously
raps translate properties-batch --models urn1,urn2,urn3 --parallel 3
```

### 3. Cache Expensive Operations

```bash
# Enable caching for repeated extractions
raps config set cache.properties-extraction true
raps config set cache.retention-days 7
```

### 4. Stream Large Datasets

```bash
# Stream properties to database for large models
raps translate properties <urn> --stream-to-database --batch-size 1000
```

---

## Troubleshooting Common Issues

### Issue 1: "No Properties Found"

**Cause:** Model needs translation first  
**Solution:**
```bash
# Ensure model is translated
raps translate <urn> --formats properties --wait
# Then extract properties
raps translate properties <urn>
```

### Issue 2: "Missing Properties for Some Elements"

**Cause:** Some CAD elements don't have extractable properties  
**Solution:**
```bash
# Check which elements have properties
raps translate properties <urn> --validate-elements --report-missing
```

### Issue 3: "Properties Extraction Times Out"

**Cause:** Very large model with millions of elements  
**Solution:**
```bash
# Use chunked extraction for large models
raps translate properties <urn> --chunked --chunk-size 10000 --timeout 600
```

### Issue 4: "Inconsistent Property Names"

**Cause:** Different CAD software uses different property names  
**Solution:**
```bash
# Apply property name mapping
raps translate properties <urn> --normalize-names --mapping property_mappings.json
```

Where `property_mappings.json`:
```json
{
  "nameMapping": {
    "Type Name": "ElementType",
    "Host": "Parent",
    "Base Constraint": "Level"
  }
}
```

---

## Use Cases

### 1. Quantity Surveying

```bash
# Generate material takeoff report
raps translate properties <urn> --analyze materials --group-by Material --calc "sum(Volume),sum(Area)" --output takeoff.xlsx
```

### 2. Space Programming

```bash
# Extract room data for space planning
raps translate properties <urn> --filter-category "Rooms,Spaces" --include-area --include-occupancy --output spaces.csv
```

### 3. Asset Management

```bash
# Extract equipment data for maintenance planning  
raps translate properties <urn> --filter-category "Mechanical Equipment,Electrical Equipment" --include-specs --output assets.json
```

### 4. Code Compliance

```bash
# Extract data for building code analysis
raps translate properties <urn> --filter-properties "Fire Rating,Occupancy,Exit Width" --validate-codes building_codes.json
```

---

## Next Steps

### Advanced Property Analysis

1. **🔗 Try other recipes:**
   - [Upload-Translate-View Recipe](./upload-translate-view.md)
   - [Batch Processing Recipe](./batch-translate.md)
   - [Webhook Integration Recipe](./webhook-setup.md)

2. **📊 Explore analytics:**
   - Time-series property tracking
   - Multi-model comparisons
   - Predictive maintenance models

3. **🔌 Integrate with your tools:**
   - Business intelligence platforms
   - ERP systems
   - IoT sensor data

---

**💡 Pro Tip:** Combine property extraction with other APS APIs:
```bash
# Extract properties + generate viewer for context
raps translate properties <urn> --output data.json && raps view <urn> --highlight-elements @large_elements.json
```

---

*Last verified: February 2026 | RAPS v4.11.0 | Model Derivative API v2*  
*Property extraction works with all major BIM and CAD formats. For format-specific property schemas, see the [APS Property Guide](../references/property-schemas.md).*