export const downloadFile = (data, filename, filetype) => {
  const blob = new Blob([data], { type: filetype });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
