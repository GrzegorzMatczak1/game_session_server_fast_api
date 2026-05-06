<?php
// Call the FastAPI health endpoint
$ch = curl_init("http://localhost:8000/api/health");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$error = curl_error($ch);
curl_close($ch);

$data = $response ? json_decode($response, true) : null;
$connected = $data && $data['status'] === 'ok';
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Browser Game</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Browser Game</h1>

  <div class="status <?= $connected ? 'ok' : 'fail' ?>">
    <?php if ($connected): ?>
      ✅ Backend connected — <?= htmlspecialchars($data['message']) ?>
    <?php else: ?>
      ❌ Backend not reachable — is FastAPI running on port 8000?
    <?php endif; ?>
  </div>
</body>
</html>