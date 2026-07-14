import { Box, Flex, Text, IconButton } from "@chakra-ui/react";

import { CloseIcon } from "@chakra-ui/icons";

import {
  successAlert,
  errorAlert,
  warningAlert,
  infoAlert,
  alertTitle,
  alertDescription,
} from "../../../styles/components/alerts";

const variants = {
  success: successAlert,
  error: errorAlert,
  warning: warningAlert,
  info: infoAlert,
};

const ToastAlert = ({
  status = "success",
  title,
  description,
  onClose,
  sx = {},
  ...props
}) => {
  return (
    <Flex
      justify="space-between"
      align="flex-start"
      sx={{
        ...(variants[status] || successAlert),
        ...sx,
      }}
      {...props}
    >
      <Box flex="1">
        {title && <Text sx={alertTitle}>{title}</Text>}

        {description && <Text sx={alertDescription}>{description}</Text>}
      </Box>

      {onClose && (
        <IconButton
          aria-label="Close"
          icon={<CloseIcon boxSize={3} />}
          size="sm"
          variant="ghost"
          onClick={onClose}
        />
      )}
    </Flex>
  );
};

export default ToastAlert;
