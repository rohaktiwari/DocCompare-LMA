import axios, { AxiosError } from 'axios';

// In production, this would be an env var
export const API_BASE_URL = 'http://localhost:8000/api';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (resp) => resp,
  (error: AxiosError) => {
    const status = error.response?.status ?? 500;
    const message = (error.response?.data as any)?.detail ?? error.message;
    return Promise.reject(new ApiError(message, status));
  }
);

export const getReportUrl = (dealName: string) => `${API_BASE_URL.replace('/api','')}/api/report/${encodeURIComponent(dealName)}`;

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

