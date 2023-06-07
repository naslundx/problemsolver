async function send(method, url, action = null, data = null) {
  let response = await fetch(`http://localhost:5000/${url}`, {
    method,
    ...(data && { body: JSON.stringify(data) }),
  });
  let json = await response.json();
  console.log(json);
  return json;
}

export { send };
