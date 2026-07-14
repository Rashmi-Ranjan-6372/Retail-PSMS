import { Box, Heading, Text } from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";

import {
  emptyState,
  emptyStateIcon,
  emptyStateTitle,
  emptyStateDescription,
  emptyStateActions,
} from "../../../styles/components/emptyState";

import { emptyStateCard } from "../../../styles/components/cards";

const EmptyState = ({
  title = "No Data Found",
  description = "There is nothing to display at the moment.",
  icon = <SearchIcon boxSize={10} />,
  action = null,
}) => {
  return (
    <Box sx={emptyState}>
      <Box sx={emptyStateCard}>
        <Box sx={emptyStateIcon}>{icon}</Box>

        <Heading as="h3" sx={emptyStateTitle}>
          {title}
        </Heading>

        <Text sx={emptyStateDescription}>{description}</Text>

        {action && <Box sx={emptyStateActions}>{action}</Box>}
      </Box>
    </Box>
  );
};

export default EmptyState;
