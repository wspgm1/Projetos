document.getElementById('login').addEventListener('submit', async (event) => {
  event.preventDefault();
  const result = document.getElementById('result');
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username: username.value, password: password.value})
  });
  const data = await response.json();
  if (!response.ok) { result.textContent = data.detail || 'Falha no login'; return; }
  localStorage.setItem('access_token', data.access_token);
  const me = await fetch('http://localhost:8000/auth/me', {headers: {Authorization: `Bearer ${data.access_token}`}});
  result.textContent = JSON.stringify(await me.json(), null, 2);
});
