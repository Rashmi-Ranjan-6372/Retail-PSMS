import {
  Box,
  Grid,
  GridItem,
  Text,
  Heading,
  Flex,
} from "@chakra-ui/react";

const Card = ({ title, value }) => {
  return (
    <Box
      p={5}
      borderRadius="lg"
      boxShadow="md"
      bg="white"
      _dark={{ bg: "gray.700" }}
    >
      <Text fontSize="sm" color="gray.500">
        {title}
      </Text>
      <Heading size="md">{value}</Heading>
    </Box>
  );
};

const Dashboard = () => {
  return (
    <Box p={5}>
      {/* Header */}
      <Flex justify="space-between" mb={5}>
        <Heading size="lg">Dashboard</Heading>
        <Text>Welcome back, John! 👋</Text>
      </Flex>

      {/* Cards */}
      <Grid templateColumns="repeat(4, 1fr)" gap={5}>
        <GridItem>
          <Card title="Total Sales" value="₹25,000" />
        </GridItem>

        <GridItem>
          <Card title="Today's Revenue" value="₹5,000" />
        </GridItem>

        <GridItem>
          <Card title="Customers" value="120" />
        </GridItem>

        <GridItem>
          <Card title="Stock Items" value="350" />
        </GridItem>
      </Grid>
    </Box>
  );
};

export default Dashboard;