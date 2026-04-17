import React, { useState, useEffect } from 'react';
import { 
  ChakraProvider, createSystem, defaultConfig, 
  Box, Flex, Heading, Spacer, Text, Container 
} from '@chakra-ui/react';
import StudentDashboard from './components/StudentDashboard';
import Login from './components/Login'; 


const system = createSystem(defaultConfig);

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // 1. ONE function to handle both Login and Register success
  const handleAuthSuccess = (authData) => {
    // Save to local storage for persistence
    localStorage.setItem('accessToken', authData.token);
    localStorage.setItem('userRole', authData.role);
    localStorage.setItem('username', authData.username);

    // Update state to trigger re-render
    setIsAuthenticated(true);
    setUser({ 
      username: authData.username, 
      role: authData.role 
    });
  };

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    const role = localStorage.getItem('userRole');
    const username = localStorage.getItem('username');

    if (token) {
      setIsAuthenticated(true);
      setUser({ username, role });
    }
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <ChakraProvider value={system}>
      <Box bg="blue.700" px={4} py={3} color="white">
        <Flex minWidth="max-content" alignItems="center" gap="2">
          <Heading size="md">IPS Manager</Heading>
          <Spacer />
          {isAuthenticated ? (
            <Flex align="center" gap={4}>
              <Text fontSize="sm" fontWeight="bold">
                {user?.username} | {user?.role} Portal
              </Text>
              <Text 
                fontSize="sm" 
                cursor="pointer" 
                textDecoration="underline" 
                onClick={handleLogout}
              >
                Logout
              </Text>
            </Flex>
          ) : (
            <Text fontSize="sm">Please Login</Text>
          )}
        </Flex>
      </Box>

      <Container maxW="container.xl" py={10}>
        {isAuthenticated ? (
          /* Show Dashboard if logged in */
          <StudentDashboard />
        ) : (
          /* Pass our new handler to the Login component */
          <Login onAuthSuccess={handleAuthSuccess} />
        )}
      </Container>
    </ChakraProvider>
  );
}

export default App;