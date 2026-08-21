# Legacy .ppt → .pptx Conversion (Windows)

When receiving a legacy `.ppt` file (pre-2007 OLE Compound Document format), `python-pptx` and `markitdown` cannot read it directly. Use PowerShell COM automation on Windows with PowerPoint installed:

```powershell
$pptApp = New-Object -ComObject PowerPoint.Application
$ppt = $pptApp.Presentations.Open('C:\path\to\file.ppt', 1, 0, 0)
$ppt.SaveAs('C:\path\to\output.pptx', 24)
$ppt.Close()
$pptApp.Quit()
```

## Enum Value Reference

| Enum | Numeric Value |
|------|---------------|
| msoFalse | 0 |
| msoTrue | 1 |
| ppSaveAsOpenXMLPresentation | 24 |

## Known Pitfalls

1. **Don't use .NET enum type names** (e.g. `[Microsoft.Office.Interop.PowerPoint.MsoTriState]::msoFalse`) — PowerShell type resolution fails in headless/non-interactive sessions. Always use raw numeric values.

2. **Visible property may throw** — setting `$pptApp.Visible = 0` can error on headless sessions. The error is non-fatal; conversion still succeeds. Just let it fail silently.

3. **`catppt` and `olefile` produce garbled CJK output** — for Chinese/Japanese/Korean content, these tools decode incorrectly. PowerShell COM conversion is the reliable path on Windows.

4. **File size check** — after conversion, verify the `.pptx` file exists and has reasonable size (>100KB for a real presentation). Zero-byte output means PowerPoint COM failed silently.

## After Conversion

Once you have `.pptx`, use standard tools:
- `python -m markitdown output.pptx` for quick text extraction
- `python-pptx` for programmatic slide-by-slide extraction
- Skill `powerpoint` workflows for editing/creation
