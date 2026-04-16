import React, { useState, useEffect } from 'react';
import { 
  ChakraProvider, createSystem, defaultConfig, 
  Box, Flex, Heading, Spacer, Text, Container 
} from '@chakra-ui/react';
import StudentDashboard from './components/StudentDashboard';
import Login from './components/Login'; // Make sure you have this component

const system = createSystem(defaultConfig);

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  // Check if a user is already logged in when the app starts
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
      {/* Navigation Bar - Only show logout if authenticated */}
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

      {/* Main Content Toggle */}
      <Container maxW="container.xl" py={10}>
        {isAuthenticated ? (
          <StudentDashboard />
        ) : (
          <Login onLoginSuccess={(userData) => {
            setIsAuthenticated(true);
            setUser(userData);
          }} />
        )}
      </Container>
    </ChakraProvider>
  );
}

export default App;