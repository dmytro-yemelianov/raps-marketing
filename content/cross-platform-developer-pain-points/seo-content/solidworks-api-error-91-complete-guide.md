# SOLIDWORKS API Error 91: Object Variable or With Block Not Set - Complete Fix Guide

## Quick Solution
**Error 91** occurs when your VBA/macro code tries to use an object that hasn't been properly initialized. This is the #1 most common SOLIDWORKS API error.

## Why This Error Happens

### Common Causes
1. **Uninitialized objects** - Using objects before setting them
2. **Failed API calls** - Methods returning Nothing/null
3. **Disposed objects** - Using objects after they've been released
4. **Incorrect type casting** - Casting to wrong interface types

## Complete Fix Solutions

### Fix 1: Always Check Object References
```vba
Dim swModel As SldWorks.ModelDoc2
Set swModel = swApp.ActiveDoc

' ALWAYS check before use
If Not swModel Is Nothing Then
    ' Safe to use swModel
    swModel.Save3 swSaveAsOptions_Silent, 0, 0
Else
    MsgBox "No active document open"
End If
```

### Fix 2: Handle Selection Manager Properly
```vba
Dim swSelMgr As SldWorks.SelectionMgr
Set swSelMgr = swModel.SelectionManager

' Common Error 91 trigger
If Not swSelMgr Is Nothing Then
    Dim swFeat As SldWorks.Feature
    Set swFeat = swSelMgr.GetSelectedObject6(1, -1)
    
    ' Must check again!
    If Not swFeat Is Nothing Then
        Debug.Print swFeat.Name
    End If
End If
```

### Fix 3: Feature Traversal Safety
```vba
Dim swFeat As SldWorks.Feature
Set swFeat = swModel.FirstFeature

While Not swFeat Is Nothing
    ' Process feature
    Debug.Print swFeat.Name
    
    ' Get next feature BEFORE processing
    Set swFeat = swFeat.GetNextFeature
Wend
```

## Platform-Specific Issues

### SOLIDWORKS Version Differences
- **2021 SP2+**: VBA 7.1 changes object handling
- **2020 and earlier**: Different null checking behavior
- **2019**: SelectionManager changes cause Error 91

### Interop DLL Conflicts
Error 91 often appears with version mismatches:
```
Error CS1705 Assembly uses 'SolidWorks.Interop.swpublished, 
Version=26.0.1.1' with higher version
```

**Solution**: Rebuild with matching interop DLLs for your SOLIDWORKS version.

## Advanced Debugging Techniques

### Enable Error Handling
```vba
On Error GoTo ErrorHandler

' Your code here
Dim swModel As SldWorks.ModelDoc2
Set swModel = swApp.ActiveDoc
swModel.Save3 swSaveAsOptions_Silent, 0, 0

Exit Sub

ErrorHandler:
    If Err.Number = 91 Then
        MsgBox "Object not initialized. Check if document is open."
    Else
        MsgBox "Error " & Err.Number & ": " & Err.Description
    End If
```

### Use Debug.Assert
```vba
Set swModel = swApp.ActiveDoc
Debug.Assert Not swModel Is Nothing ' Stops here if Nothing
```

## Common Scenarios and Solutions

### Scenario 1: Saving Documents
**Problem**: Error 91 when saving
```vba
' WRONG
swModel.Save3 swSaveAsOptions_Silent, 0, 0
```

**Solution**:
```vba
' RIGHT
If Not swModel Is Nothing Then
    Dim errors As Long
    Dim warnings As Long
    Dim success As Boolean
    success = swModel.Save3(swSaveAsOptions_Silent, errors, warnings)
    If Not success Then
        MsgBox "Save failed. Errors: " & errors
    End If
End If
```

### Scenario 2: Getting Configuration
**Problem**: Error 91 accessing configuration
```vba
' WRONG
Dim configName As String
configName = swModel.GetActiveConfiguration.Name
```

**Solution**:
```vba
' RIGHT
Dim swConfig As SldWorks.Configuration
Set swConfig = swModel.GetActiveConfiguration
If Not swConfig Is Nothing Then
    configName = swConfig.Name
End If
```

### Scenario 3: Component Selection in Assembly
**Problem**: Error 91 when selecting components
```vba
' WRONG
Dim swComp As SldWorks.Component2
Set swComp = swSelMgr.GetSelectedObject6(1, -1)
swComp.Select4 False, Nothing, False
```

**Solution**:
```vba
' RIGHT
Dim swComp As SldWorks.Component2
Set swComp = swSelMgr.GetSelectedObject6(1, -1)
If Not swComp Is Nothing Then
    swComp.Select4 False, Nothing, False
End If
```

## Prevention Best Practices

### 1. Initialize Everything
```vba
Dim swApp As SldWorks.SldWorks
Dim swModel As SldWorks.ModelDoc2
Dim swFeat As SldWorks.Feature

' Initialize application first
Set swApp = Application.SldWorks
If swApp Is Nothing Then
    Set swApp = CreateObject("SldWorks.Application")
End If

' Then get model
Set swModel = swApp.ActiveDoc
```

### 2. Use Early Binding
```vba
' BETTER: Early binding with type checking
Dim swApp As SldWorks.SldWorks

' AVOID: Late binding
Dim swApp As Object
```

### 3. Release Objects Properly
```vba
' Clean up when done
Set swFeat = Nothing
Set swModel = Nothing
Set swApp = Nothing
```

## Related Errors
- **Error 13**: Type mismatch (often occurs with Error 91)
- **Error 438**: Object doesn't support property/method
- **Error 424**: Object required

## Why SOLIDWORKS API Documentation Doesn't Help

As one developer noted:
> "Those error codes, warnings and return value? They do nothing. The method always returns true even when it fails, and the warnings and errors are always zero, even when the file didn't save."

This is why community resources and tools like RAPS are essential for SOLIDWORKS development.

## Tools That Can Help

### RAPS CLI
While RAPS primarily targets Autodesk APS, the same error handling patterns apply:
- Automatic null checking
- Retry logic for failed operations
- Clear error messages

### Community Resources
- CADSharp's 23 common VBA errors guide
- SOLIDWORKS API forum (requires login)
- GitHub examples with proper error handling

## SEO Keywords Covered
- solidworks api error 91
- object variable not set solidworks
- with block variable not set vba
- solidworks macro error 91
- solidworks vba object not initialized
- error 91 solidworks api fix
- solidworks interop error handling

---

*This guide addresses the most searched SOLIDWORKS API error. For more CAD API solutions, explore our cross-platform developer tools.*