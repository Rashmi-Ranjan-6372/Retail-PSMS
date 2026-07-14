import { Box, Flex, Text, Icon } from "@chakra-ui/react";

import {
  infoAlert,
  alertTitle,
  alertDescription,
} from "../../../styles/components/alerts";

const NotificationAlert = ({ icon, title, message, sx = {}, ...props }) => {
  return (
    <Flex
      align="flex-start"
      gap={3}
      sx={{
        ...infoAlert,
        ...sx,
      }}
      {...props}
    >
      {icon && <Icon as={icon} boxSize={5} mt="2px" />}

      <Box flex="1">
        {title && <Text sx={alertTitle}>{title}</Text>}

        <Text sx={alertDescription}>{message}</Text>
      </Box>
    </Flex>
  );
};

export default NotificationAlert;
