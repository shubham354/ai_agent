import React from 'react';
import {
  Box,
  Flex,
  Heading,
  Button,
  useColorMode,
  IconButton,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiSun, FiMoon, FiLogOut } from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const { logout } = useAuth();
  const bg = useColorModeValue('white', 'gray.800');

  return (
    <Box
      as="nav"
      bg={bg}
      px={4}
      py={2}
      shadow="sm"
      position="sticky"
      top={0}
      zIndex={1}
    >
      <Flex justify="space-between" align="center" maxW="container.xl" mx="auto">
        <Heading size="md">AI Agent</Heading>
        <Flex gap={2}>
          <IconButton
            aria-label="Toggle color mode"
            icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
            onClick={toggleColorMode}
            variant="ghost"
          />
          <Button
            leftIcon={<FiLogOut />}
            variant="ghost"
            onClick={logout}
          >
            Logout
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navbar; 