import axios from 'axios';

// In production, this would be an env var
const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeDeal = async (sampleDealId?: string, dealText?: string) => {
  const response = await api.post('/analyze/', {
    sample_deal_id: sampleDealId,
    deal_text: dealText,
    template_id: "LMA_Leveraged_2023.txt"
  });
  return response.data;
};

export const getSamples = async () => {
  const response = await api.get('/analyze/samples');
  return response.data.samples;
};

export const getPortfolio = async () => {
  const response = await api.get('/portfolio/');
  return response.data;
};

export const getVersions = async (baseName: string) => {
  const response = await api.get(`/amendments/${baseName}/versions`);
  return response.data.versions;
};

export const compareVersions = async (v1: string, v2: string) => {
  const response = await api.get(`/amendments/compare`, { params: { v1, v2 } });
  return response.data;
};

