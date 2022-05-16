console.log('Work!')

getToken.addEventListener('submit', function (e) {
  e.preventDefault()
  const formData = new FormData(getToken)
  console.log(formData)
  const result = fetch('http://127.0.0.1:8000/token', {
    method: 'POST',
    body: formData,
  })
    .then((r) => r.json())
    .then((r) => {
      console.log(r)
      localStorage.setItem('token', r.access_token)
      fetch('http://127.0.0.1:8000/notes', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then((r) => r.json())
        .then((r) => console.log(r))
    })
    .catch((e) => console.log(e))
})
