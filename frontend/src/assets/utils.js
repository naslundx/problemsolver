const send = async (method, url, action = null, data = null) => {
  let response = await fetch(`/api/${url}`, {
  // let response = await fetch(`http://127.0.0.1:5000/api/${url}`, {
    method,
    ...(data && { body: JSON.stringify(data) }),
  });
  let json = await response.json();
  return json;
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export { send, sleep };
