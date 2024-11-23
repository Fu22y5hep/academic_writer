import { getToken } from './token';

export const getAuthHeaders = async () => {
  const token = await getToken();
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};
