import { Box, Text, Heading, Flex, SimpleGrid } from "@chakra-ui/react";

import { dashboard } from "../../styles/components/layout";

const DashboardCard = ({ title, value }) => {
  return (
    <Box sx={dashboard.statCard}>
      <Text sx={dashboard.statTitle}>{title}</Text>

      <Heading sx={dashboard.statValue}>{value}</Heading>
    </Box>
  );
};

const Dashboard = () => {
  return (
    <Box sx={dashboard.dashboardWrapper}>
      <Flex sx={dashboard.dashboardHeader}>
        <Box>
          <Heading sx={dashboard.dashboardTitle}>Dashboard</Heading>

          <Text sx={dashboard.dashboardSubtitle}>Welcome back 👋</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default Dashboard;
