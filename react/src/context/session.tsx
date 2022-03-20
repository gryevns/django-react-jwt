import axios, { AxiosInstance } from 'axios';
import { createContext, ReactNode } from 'react';
import { useClient } from 'react-axios-http-jwt';
import LoginForm from '../pages/Login';

const BASE_URL = process.env.REACT_APP_BASE_URL;
const CLIENT_TIMEOUT = process.env.REACT_APP_CLIENT_TIMEOUT;

const config = {
  baseURL: BASE_URL,
  timeout: CLIENT_TIMEOUT ? parseInt(CLIENT_TIMEOUT) : 5000,
  withCredentials: true,
};

const _client = axios.create(config);

interface SessionInterface {
  isAuthenticated?: boolean;
  isLoading: boolean;
  axios: AxiosInstance;
  login: (data: any) => Promise<void>;
  logout: () => Promise<void>;
}

export const SessionContext = createContext<SessionInterface>({
  isAuthenticated: false,
  isLoading: false,
  axios: axios.create(config),
  login: (data: any) => Promise.resolve(),
  logout: () => Promise.resolve(),
});

const onLogin = async (data: any): Promise<string> => {
  const response = await _client.post('/api/token/', data);
  return response.data.access;
};

const onLogout = async (): Promise<void> => {
  await _client.delete('/api/token/clear/');
};

const onRefresh = async (): Promise<string> => {
  const response = await _client.post(`/api/token/refresh/`);
  return response.data.access;
};

const Session = ({ children }: { children: ReactNode }) => {
  const client = useClient(config, onLogin, onLogout, onRefresh);

  const value = {
    isAuthenticated: client.isAuthenticated,
    isLoading: client.isLoading,
    axios: client.axios,
    login: client.login,
    logout: client.logout,
  };

  if (client.isLoading) {
    return null;
  }

  if (!client.isAuthenticated) {
    const onSubmit = async (event: any) => {
      const username = event.target.username.value;
      const password = event.target.password.value;
      event.preventDefault();
      try {
        await client.login({ username, password });
      } catch (error) {
        // TODO error handling
        console.error(error);
      }
    };
    return <LoginForm onSubmit={onSubmit} />;
  }

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
};

export default Session;
