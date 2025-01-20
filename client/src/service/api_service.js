import axios from "axios";

const API_BASE_URL = "http://localhost:5000";

export const fetchTelegramData = async (channel) => {
  const response = await axios.post(`${API_BASE_URL}/fetch`, { channel });
  return response.data;
};

export const normalizeTelegramData = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/normalize`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export const getNormalizedData = async (filePath) => {
  const response = await axios.get(`${API_BASE_URL}/data`, {
    params: { file_path: filePath },
  });
  return response.data;
};
