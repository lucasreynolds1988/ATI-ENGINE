export function parseQueryParams(url) {
  const query = {};
  const urlObj = new URL(url, window.location.origin);
  urlObj.searchParams.forEach((value, key) => {
    query[key] = value;
  });
  return query;
}
