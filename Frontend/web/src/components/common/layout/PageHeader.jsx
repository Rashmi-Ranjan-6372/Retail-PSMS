import { Box, Flex, Heading, Text } from "@chakra-ui/react";
import dashboard from "../../../styles/components/layout/dashboard";

const PageHeader = ({ title, subtitle, children, actions, mb = 8 }) => {
  return (
    <Flex
      sx={dashboard.dashboardHeader}
      mb={mb}
      justify="space-between"
      align="center"
      wrap="wrap"
      gap={4}
    >
      <Box>
        <Heading sx={dashboard.dashboardTitle}>{title}</Heading>

        {subtitle && <Text sx={dashboard.dashboardSubtitle}>{subtitle}</Text>}
      </Box>

      {(actions || children) && (
        <Flex gap={3} align="center">
          {actions}
          {children}
        </Flex>
      )}
    </Flex>
  );
};

export default PageHeader;
