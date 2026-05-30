import {
  Box,
  Grid,
  GridItem,
  Text,
  Heading,
  Flex,
  SimpleGrid,
} from "@chakra-ui/react";

const DashboardCard = ({ title, value }) => {
  return (
    <Box
      p={6}
      borderRadius="xl"
      boxShadow="sm"
      border="1px solid"
      borderColor="gray.100"
    >
      <Text fontSize="sm" color="gray.500" mb={2}>
        {title}
      </Text>

      <Heading size="lg" color="gray.700">
        {value}
      </Heading>
    </Box>
  );
};

const Dashboard = () => {
  return (
    <Box w="100%" minH="calc(100vh - 70px)" bg="gray.50" px={6} py={4}>
      {/* Header */}
      <Flex justify="space-between" align="center" mb={8}>
        <Box>
          <Heading size="lg" color="gray.700">
            Dashboard
          </Heading>

          <Text color="gray.500">Welcome back 👋</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default Dashboard;
