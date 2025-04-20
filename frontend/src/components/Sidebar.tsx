import React from 'react';
import {
  Box,
  VStack,
  Icon,
  Text,
  Link,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiMessageSquare, FiBarChart2 } from 'react-icons/fi';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const NavItem: React.FC<{
  icon: any;
  children: React.ReactNode;
  to: string;
}> = ({ icon, children, to }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  const activeBg = useColorModeValue('blue.50', 'blue.900');
  const hoverBg = useColorModeValue('gray.100', 'gray.700');

  return (
    <Link
      as={RouterLink}
      to={to}
      style={{ textDecoration: 'none' }}
      _focus={{ boxShadow: 'none' }}
    >
      <Box
        display="flex"
        alignItems="center"
        p={3}
        borderRadius="lg"
        bg={isActive ? activeBg : 'transparent'}
        color={isActive ? 'blue.500' : undefined}
        _hover={{
          bg: isActive ? activeBg : hoverBg,
        }}
      >
        <Icon as={icon} fontSize="xl" />
        <Text ml={4} fontWeight={isActive ? 'medium' : 'normal'}>
          {children}
        </Text>
      </Box>
    </Link>
  );
};

const Sidebar: React.FC = () => {
  const bg = useColorModeValue('white', 'gray.800');

  return (
    <Box
      as="aside"
      w={64}
      h="100vh"
      bg={bg}
      borderRightWidth={1}
      position="sticky"
      top={0}
    >
      <VStack p={4} spacing={2} align="stretch">
        <NavItem icon={FiMessageSquare} to="/">
          Chat
        </NavItem>
        <NavItem icon={FiBarChart2} to="/analysis">
          Data Analysis
        </NavItem>
      </VStack>
    </Box>
  );
};

export default Sidebar; 