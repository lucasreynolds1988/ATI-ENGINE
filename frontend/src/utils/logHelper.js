export function appendLog(logArray, line, max = 200) {
  const newLog = [...logArray, line];
  if (newLog.length > max) newLog.shift();
  return newLog;
}
