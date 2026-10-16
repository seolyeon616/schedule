# MANYEON FILM01 영상 자동 정리 스크립트
# - 다운로드 폴더의 Flow 영상(mp4)을 파일 이름 키워드로 #1~#10에 배정해서
#   바탕화면\MANYEON_FILM01\01_video 에 "복사"합니다. (원본은 그대로 둠)
# - 같은 컷이 여러 개면 가장 최근 파일을 본편으로, 나머지는 _후보 폴더로.
# - 어디에도 안 맞는 파일은 _미분류 폴더로.
# 실행: 이 파일을 우클릭 → "PowerShell에서 실행"

$src  = Join-Path $env:USERPROFILE "Downloads"
$root = Join-Path ([Environment]::GetFolderPath("Desktop")) "MANYEON_FILM01"
$vid  = Join-Path $root "01_video"
foreach ($d in @($vid, "$vid\_후보", "$vid\_미분류", "$root\02_audio", "$root\03_logo", "$root\04_export")) {
  New-Item -ItemType Directory -Force -Path $d | Out-Null
}

# 순서가 중요합니다: 위에서부터 먼저 맞는 컷으로 배정
$rules = @(
  @{ n="10_ripple-end";     k="ripple|black_(glossy_)?surface|onto_(a_)?black|end_title" },
  @{ n="02_into-droplet";   k="through|into_(the_)?(water_)?droplet|moving_through" },
  @{ n="03_glacier-drop";   k="melt|trapped|caustic|glacier_ice" },
  @{ n="08_serum-drop";     k="dropper|pipette|fingertip|serum_drop|drop_of_serum" },
  @{ n="07_woman-window";   k="woman|lady|girl|eyes|portrait|face" },
  @{ n="09_hero-bottle";    k="bottle|hero|product" },
  @{ n="06_city-window";    k="rain|window|glass|city|neon" },
  @{ n="05_fern-dew";       k="fern|dew|leaf|forest|moss" },
  @{ n="04_waterfall-dive"; k="waterfall|drone|fpv" },
  @{ n="01_drop-hook";      k="droplet|drop" }
)

$files = Get-ChildItem -Path $src -Filter *.mp4 | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
$buckets = @{}
$unsorted = @()
foreach ($f in $files) {
  $name = $f.Name.ToLower()
  $hit = $null
  foreach ($r in $rules) { if ($name -match $r.k) { $hit = $r.n; break } }
  if ($hit) { if (-not $buckets[$hit]) { $buckets[$hit] = @() }; $buckets[$hit] += $f }
  else { $unsorted += $f }
}

$report = @()
foreach ($r in ($rules | Sort-Object { $_.n })) {
  $list = $buckets[$r.n] | Sort-Object LastWriteTime -Descending
  if (-not $list) { $report += [pscustomobject]@{ 컷=$r.n; 본편="(없음 - 직접 넣어주세요)"; 후보=0 }; continue }
  Copy-Item $list[0].FullName (Join-Path $vid ($r.n + ".mp4")) -Force
  $i = 1
  foreach ($c in ($list | Select-Object -Skip 1)) {
    Copy-Item $c.FullName (Join-Path "$vid\_후보" ("{0}_후보{1}.mp4" -f $r.n, $i)) -Force; $i++
  }
  $report += [pscustomobject]@{ 컷=$r.n; 본편=$list[0].Name; 후보=($list.Count - 1) }
}
foreach ($u in $unsorted) { Copy-Item $u.FullName "$vid\_미분류\" -Force }

$report | Format-Table -AutoSize
"미분류: $($unsorted.Count)개  →  $vid\_미분류"
"정리 위치: $root"
"※ 원본은 다운로드 폴더에 그대로 있습니다. 표를 캡처해서 Claude에게 보내주면 잘못 배정된 컷을 바로잡아 드립니다."
Start-Process $root
Read-Host "엔터를 누르면 창이 닫힙니다"
