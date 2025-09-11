const send = async (method, url, data = null) => {
  const server_url = `/api/${url}`;
  let response = await fetch(server_url, {
    method,
    ...(data && { body: JSON.stringify(data) }),
  });
  let json = await response.json();
  return json;
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function isEmpty(obj) {
  for (const prop in obj) {
    if (Object.hasOwn(obj, prop)) {
      return false;
    }
  }

  return true;
}

export { send, sleep, isEmpty };
