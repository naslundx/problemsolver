async function send(method, url, action = null, data = null) {
  let response = await fetch(`/api/${url}`, {
    method,
    ...(data && { body: JSON.stringify(data) }),
  });
  let json = await response.json();
  console.log(json);
  return json;
}

export { send };
