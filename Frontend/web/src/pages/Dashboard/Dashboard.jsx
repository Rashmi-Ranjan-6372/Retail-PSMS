import { Box, Text, Heading, Flex, SimpleGrid } from "@chakra-ui/react";

import dashboard from "../../styles/components/dashboard";

const DashboardCard = ({ title, value }) => {
  return (
    <Box sx={dashboard.dashboardCard}>
      <Text sx={dashboard.cardTitle}>{title}</Text>

      <Heading sx={dashboard.cardValue}>{value}</Heading>
    </Box>
  );
};

const Dashboard = () => {
  return (
    <Box sx={dashboard.dashboardWrapper}>
      <Flex sx={dashboard.dashboardHeader}>
        <Box sx={dashboard.dashboardTitleWrapper}>
          <Heading sx={dashboard.dashboardTitle}>Dashboard</Heading>

          <Text sx={dashboard.dashboardSubtitle}>Welcome back 👋</Text>
        </Box>
      </Flex>
    </Box>
  );
};

export default Dashboard;
