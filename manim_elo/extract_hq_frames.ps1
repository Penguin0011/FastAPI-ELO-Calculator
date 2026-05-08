# Extract 1 frame per second from all 1080p60 renders for inspection
$base = "C:\Users\iyerm\Documents\GitHub\FastAPI-ELO-Calculator\manim_elo\media"
$outBase = "$base\hq_frames"

$videoFolders = Get-ChildItem "$base\videos" -Directory

foreach ($folder in $videoFolders) {
    $quality = Join-Path $folder.FullName "1080p60"
    if (-not (Test-Path $quality)) { continue }

    $videos = Get-ChildItem $quality -Filter "*.mp4" | Where-Object { $_.DirectoryName -notmatch "partial" }

    foreach ($vid in $videos) {
        $name = $vid.BaseName
        $outDir = "$outBase\$name"

        if (Test-Path $outDir) {
            $existing = Get-ChildItem $outDir -Filter "*.png" -ErrorAction SilentlyContinue
            if ($existing.Count -gt 0) {
                Write-Host "SKIP (exists): $name"
                continue
            }
        }

        New-Item -ItemType Directory -Force -Path $outDir | Out-Null
        ffmpeg -i $vid.FullName -vf "fps=1" "$outDir\frame_%04d.png" -y 2>&1 | Out-Null
        $count = (Get-ChildItem $outDir -Filter "*.png").Count
        Write-Host "OK: $name ($count frames)"
    }
}

Write-Host "`nDone extracting all 1080p frames."
