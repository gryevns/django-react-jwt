import { QueryClient, QueryClientProvider } from 'react-query';
import Session from './context/session';
import Example from './pages/Example';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Session>
        <Example />
      </Session>
    </QueryClientProvider>
  );
}

export default App;
